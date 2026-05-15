import torch
from transformers import AutoProcessor, Idefics3ForConditionalGeneration
from peft import PeftModel
from PIL import Image
import random
import os
from IPython.display import display

# --- Διαδρομές ---
base_model_id = "HuggingFaceTB/SmolVLM-256M-Instruct"
adapter_path = '/content/drive/MyDrive/Telecom_Project/trained_smolvlm_final'
image_dir = '/content/images/'

print("Φόρτωση του AI στην Κάρτα Γραφικών (GPU)...")
processor = AutoProcessor.from_pretrained(adapter_path)

# Φόρτωση του μοντέλου κατευθείαν στην GPU (device_map="auto")
base_model = Idefics3ForConditionalGeneration.from_pretrained(
    base_model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto" 
)

# Ενώνουμε τις "γνώσεις" σου (LoRA) με το βασικό μοντέλο
model = PeftModel.from_pretrained(base_model, adapter_path)
print("✅ Το AI είναι έτοιμο!\n")

# --- Επιλογή Τυχαίας Εικόνας ---
all_images = [f for f in os.listdir(image_dir) if f.endswith('.png')]
random_img_name = random.choice(all_images)
img_path = os.path.join(image_dir, random_img_name)

image = Image.open(img_path).convert("RGB")
print("=========================================")
print(f"👉 ΠΡΑΓΜΑΤΙΚΑ ΣΤΟΙΧΕΙΑ: \n{random_img_name}")
print("=========================================")
display(image)

# --- Η Ερώτηση στο AI ---
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "Identify the modulation and impairments in this constellation diagram."}
        ]
    }
]

prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
inputs = processor(text=prompt, images=[image], return_tensors="pt")
# Στέλνουμε τα δεδομένα στην κάρτα γραφικών
inputs = {k: v.to(model.device) for k, v in inputs.items()}

# --- Η Απάντηση του AI ---
print("\nΤο AI σκέφτεται...")
# Με τη GPU αυτό θα πάρει ελάχιστα δευτερόλεπτα!
generated_ids = model.generate(**inputs, max_new_tokens=100)

generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
answer_only = generated_texts.split("Assistant:")[-1].strip() if "Assistant:" in generated_texts else generated_texts

print("\n🤖 ΑΠΑΝΤΗΣΗ ΜΟΝΤΕΛΟΥ:")
print("-----------------------------------------")
print(answer_only)
print("-----------------------------------------")