import torch
from transformers import AutoProcessor, Idefics3ForConditionalGeneration
from peft import PeftModel
from PIL import Image
import os
import re
import pandas as pd
from tqdm import tqdm # Για την μπάρα προόδου!

# --- 1. Ρυθμίσεις και Διαδρομές ---
drive_path = '/content/drive/MyDrive/Telecom_Project/'
test_zip_path = os.path.join(drive_path, 'test_images.zip') # Το zip με το νέο dataset
test_dir = '/content/test_images/'
adapter_path = os.path.join(drive_path, 'trained_smolvlm_final')
output_csv = os.path.join(drive_path, 'evaluation_results.csv')

# Αποσυμπίεση του test set στο Colab (αν δεν υπάρχει ήδη)
if not os.path.exists(test_dir):
    print("Αποσυμπίεση του Test Set...")
    !unzip -q {test_zip_path} -d {test_dir}

# --- 2. Φόρτωση Μοντέλου σε GPU ---
print("Φόρτωση του AI στην Κάρτα Γραφικών...")
processor = AutoProcessor.from_pretrained(adapter_path)
base_model = Idefics3ForConditionalGeneration.from_pretrained(
    "HuggingFaceTB/SmolVLM-256M-Instruct", torch_dtype=torch.bfloat16, device_map="auto"
)
model = PeftModel.from_pretrained(base_model, adapter_path)
model.eval() # Βάζουμε το μοντέλο σε λειτουργία "Testing"
print("✅ Μοντέλο Έτοιμο!\n")

# --- 3. Προετοιμασία λίστας εικόνων ---
all_test_images = [f for f in os.listdir(test_dir) if f.endswith('.png')]
print(f"Βρέθηκαν {len(all_test_images)} εικόνες για αξιολόγηση.\n")

results = []

# --- 4. Η Διαδικασία Αξιολόγησης (Loop) ---
print("Ξεκινάει η αυτόματη αξιολόγηση...")
# Χρησιμοποιούμε το tqdm για να βλέπουμε μπάρα προόδου (π.χ. 10/200)
for img_name in tqdm(all_test_images):
    img_path = os.path.join(test_dir, img_name)
    
    # Α. Εξαγωγή της "Αλήθειας" (Ground Truth) από το όνομα του αρχείου
    # Παράδειγμα: img_00012_16-QAM_true_false_true_Medium15.42.png
    truth_match = re.search(r'img_\d+_([A-Za-z0-9-]+)_(true|false)_(true|false)_(true|false)_([A-Za-z]+)([\d\.]+)\.png', img_name)
    if not truth_match:
        continue # Αν κάποιο αρχείο έχει λάθος όνομα, το προσπερνάμε
    
    true_mod, true_pn, true_iq, true_jam, snr_category, true_snr = truth_match.groups()
    true_snr = float(true_snr)
    
    # Β. Ερώτηση στο AI
    image = Image.open(img_path).convert("RGB")
    messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "Identify the modulation and impairments in this constellation diagram."}]}]
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[image], return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    with torch.no_grad(): # Δεν κάνουμε εκπαίδευση, άρα κλείνουμε τα gradients για ταχύτητα
        generated_ids = model.generate(**inputs, max_new_tokens=100)
    
    generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    ai_answer = generated_texts.split("Assistant:")[-1].strip() if "Assistant:" in generated_texts else generated_texts
    
    # Γ. Εξαγωγή των προβλέψεων του AI από το κείμενό του
    pred_mod_match = re.search(r'modulation is ([A-Za-z0-9-]+)', ai_answer, re.IGNORECASE)
    pred_mod = pred_mod_match.group(1) if pred_mod_match else "Unknown"
    
    # Δ. Αποθήκευση αποτελεσμάτων
    results.append({
        "Filename": img_name,
        "True_Modulation": true_mod,
        "Predicted_Modulation": pred_mod,
        "True_SNR": true_snr,
        "SNR_Category": snr_category,
        "Correct_Modulation": int(true_mod.lower() == pred_mod.lower()), # 1 αν πέτυχε, 0 αν απέτυχε
        "AI_Full_Answer": ai_answer
    })

# --- 5. Δημιουργία Στατιστικών και Αποθήκευση ---
df = pd.DataFrame(results)

# Υπολογισμός Συνολικής Ακρίβειας (Accuracy)
total_acc = df["Correct_Modulation"].mean() * 100

# Υπολογισμός Ακρίβειας ανά SNR Κατηγορία (Robustness to low SNR)
snr_acc = df.groupby("SNR_Category")["Correct_Modulation"].mean() * 100

print("\n" + "="*40)
print(f"🎯 ΣΥΝΟΛΙΚΗ ΑΚΡΙΒΕΙΑ ΜΟΝΤΕΛΟΥ: {total_acc:.2f}%")
print("="*40)
print("📊 Ακρίβεια ανά επίπεδο SNR (Robustness):")
print(snr_acc.to_string())
print("="*40)

# Αποθήκευση στο Google Drive για να το κάνεις διαγράμματα στο Excel
df.to_csv(output_csv, index=False)
print(f"\n💾 Τα αναλυτικά αποτελέσματα σώθηκαν στο Drive σου: {output_csv}")