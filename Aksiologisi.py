import torch
from transformers import AutoProcessor, Idefics3ForConditionalGeneration
from peft import PeftModel
from PIL import Image
import os
import pandas as pd
from tqdm import tqdm
import glob
from google.colab import drive

# --- 1. Συνδέσεις & Διαδρομές ---
drive.mount('/content/drive')
drive_path = '/content/drive/MyDrive/Telecom_Project/'
test_dir = '/content/test_images/'

adapter_path = os.path.join(drive_path, 'trained_smolvlm_STRONG')
# Χρησιμοποιούμε το παλιό CSV σου ως "Λυσάρι" (εκεί που πήρε 1%)
truth_csv_path = os.path.join(drive_path, 'evaluation_results.csv')
# Εδώ θα σωθούν τα νέα, καλά αποτελέσματα
output_csv = os.path.join(drive_path, 'evaluation_results_STRONG.csv')

# --- 2. Φόρτωση του Λυσαριού ---
if not os.path.exists(truth_csv_path):
    raise FileNotFoundError(f"❌ Δεν βρέθηκε το αρχείο {truth_csv_path} στο Drive σου.")
    
df_truth = pd.read_csv(truth_csv_path)
print(f"📊 Φορτώθηκε το λυσάρι με τις απαντήσεις για {len(df_truth)} εικόνες.")

# --- 3. Φόρτωση Μοντέλου σε GPU ---
print("🔮 Φόρτωση του AI στην Κάρτα Γραφικών...")
processor = AutoProcessor.from_pretrained(adapter_path)
base_model = Idefics3ForConditionalGeneration.from_pretrained(
    "HuggingFaceTB/SmolVLM-256M-Instruct", torch_dtype=torch.bfloat16, device_map="auto"
)
model = PeftModel.from_pretrained(base_model, adapter_path)
model.eval() 
print("✅ Μοντέλο Έτοιμο!\n")

results = []

# --- 4. Η Διαδικασία Αξιολόγησης (Loop) ---
print("🚀 Ξεκινάει η αυτόματη αξιολόγηση...")

for index, row in tqdm(df_truth.iterrows(), total=len(df_truth)):
    img_name = row['Filename']
    true_mod = str(row['True_Modulation']).strip()
    
    # Ψάχνουμε να βρούμε την εικόνα (ακόμα κι αν είναι μέσα σε υποφάκελο)
    search = glob.glob(os.path.join(test_dir, '**', img_name), recursive=True)
    if not search:
        continue 
    img_path = search[0]
    
    # Ερώτηση στο AI
    try:
        image = Image.open(img_path).convert("RGB")
    except:
        continue
        
    messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "Identify the modulation and impairments in this constellation diagram."}]}]
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[image], return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    with torch.no_grad(): 
        generated_ids = model.generate(**inputs, max_new_tokens=60)
    
    generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    ai_answer = generated_texts.split("Assistant:")[-1].strip() if "Assistant:" in generated_texts else generated_texts
    
    # Έλεγχος αν η σωστή διαμόρφωση υπάρχει μέσα στην απάντηση
    is_correct = 1 if true_mod.lower() in ai_answer.lower() else 0
    
    # Αποθήκευση αποτελεσμάτων
    results.append({
        "Filename": img_name,
        "True_Modulation": true_mod,
        "AI_Full_Answer": ai_answer,
        "Correct_Modulation": is_correct,
        "True_SNR": row.get('True_SNR', 'N/A'),
        "SNR_Category": row.get('SNR_Category', 'N/A')
    })

# --- 5. Δημιουργία Στατιστικών και Αποθήκευση ---
df_results = pd.DataFrame(results)
if not results:
    print("❌ Σφάλμα: Δεν βρέθηκαν οι εικόνες. Έλεγξε το unzip.")
else:
    total_acc = df_results["Correct_Modulation"].mean() * 100
    print("\n" + "="*40)
    print(f"🎯 ΣΥΝΟΛΙΚΗ ΑΚΡΙΒΕΙΑ ΝΕΟΥ ΜΟΝΤΕΛΟΥ: {total_acc:.2f}%")
    print("="*40)
    
    if 'SNR_Category' in df_results.columns and df_results['SNR_Category'].iloc[0] != 'N/A':
        snr_acc = df_results.groupby("SNR_Category")["Correct_Modulation"].mean() * 100
        print("📊 Ακρίβεια ανά επίπεδο SNR (Robustness):")
        print(snr_acc.to_string())
        print("="*40)

    df_results.to_csv(output_csv, index=False)
    print(f"\n💾 Τα αναλυτικά αποτελέσματα σώθηκαν στο Drive σου: {output_csv}")