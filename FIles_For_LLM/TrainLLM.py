import torch
from datasets import load_dataset
from transformers import (
    AutoProcessor, 
    Idefics3ForConditionalGeneration,
    BitsAndBytesConfig, 
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model
import os
from PIL import Image

# --- 1. Διαδρομές ---
dataset_file = '/content/drive/MyDrive/Telecom_Project/vqa_dataset.jsonl'
output_model_dir = '/content/drive/MyDrive/Telecom_Project/trained_smolvlm_final'

print("Φόρτωση του Dataset...")
dataset = load_dataset('json', data_files=dataset_file, split='train')

# --- 2. Φόρτωση του Processor ---
model_id = "HuggingFaceTB/SmolVLM-256M-Instruct"
processor = AutoProcessor.from_pretrained(model_id)

# --- 3. Ρυθμίσεις 4-bit Quantization (Για να χωράει στη μνήμη) ---
print("Φόρτωση του Μοντέλου...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = Idefics3ForConditionalGeneration.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto"
)
model.config.use_cache = False 

# --- 4. Εφαρμογή LoRA ---
print("Εφαρμογή LoRA...")
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"], 
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# --- 5. Ρυθμίσεις Εκπαίδευσης ---
# Έχουμε βάλει max_steps=500 για καλύτερο generalization
training_args = TrainingArguments(
    output_dir=output_model_dir,
    per_device_train_batch_size=1,   
    gradient_accumulation_steps=8,   
    optim="paged_adamw_8bit",
    learning_rate=2e-4,
    fp16=True,                       
    logging_steps=10,
    max_steps=500,                   
    save_steps=100, # Σώζει ένα checkpoint κάθε 100 steps για ασφάλεια
    remove_unused_columns=False,
    report_to="none"
)

# --- 6. Data Collator (Η συνάρτηση που ενώνει εικόνα και κείμενο) ---
def collate_fn(examples):
    texts = [processor.apply_chat_template(ex["messages"], tokenize=False) for ex in examples]
    
    images = []
    for ex in examples:
        # Παίρνουμε το όνομα του αρχείου από το URL του JSONL
        img_name = ex["messages"][0]["content"][0]["url"].split('/')[-1]
        img_path = f"/content/images/{img_name}"
        
        try:
            img = Image.open(img_path).convert("RGB")
            images.append(img)
        except Exception as e:
            # Αν λείπει κάποια εικόνα, βάζουμε μια μαύρη για να μην κρασάρει το training
            print(f"Σφάλμα φόρτωσης {img_name}: {e}")
            images.append(Image.new('RGB', (224, 224), color='black'))
        
    batch = processor(text=texts, images=images, return_tensors="pt", padding=True)
    
    labels = batch["input_ids"].clone()
    labels[labels == processor.tokenizer.pad_token_id] = -100
    batch["labels"] = labels
    
    return batch

# --- 7. Εκκίνηση Εκπαίδευσης ---
print("Ξεκινάει το Training! (Αυτό θα πάρει περίπου 45-55 λεπτά)")

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=collate_fn,
)

trainer.train()

# --- 8. Αποθήκευση ---
print("Αποθήκευση στο Google Drive...")
trainer.save_model(output_model_dir)
processor.save_pretrained(output_model_dir)
print("✅ ΕΠΙΤΥΧΙΑ! Το μοντέλο εκπαιδεύτηκε και είναι έτοιμο.")