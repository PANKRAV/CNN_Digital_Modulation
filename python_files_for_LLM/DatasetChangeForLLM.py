import pandas as pd
import json
import os
import random
import glob

# --- 1. Διαδρομές αρχείων ---
csv_path = 'data/data.csv'  
images_dir = 'data/images/' 
output_jsonl = 'data/vqa_dataset.jsonl'

print(f"Διαβάζω το αρχείο {csv_path}...")
df = pd.read_csv(csv_path)

dataset_entries = []
print("Ξεκινάει η δημιουργία του VQA Dataset. Παρακαλώ περιμένετε...")

for index, row in df.iterrows():
    mod = row['Modulation']
    pn = float(row['Phase_Noise'])
    iq = float(row['IQ_Imbalance'])
    jam = float(row['Interference'])
    snr = int(row['SNR_Range'])
    count = int(row['Count'])
    
    # --- Η ΛΥΣΗ ΕΔΩ: Ψάχνουμε με βάση τον ΑΡΙΘΜΟ και τη ΔΙΑΜΟΡΦΩΣΗ ---
    # Παράδειγμα: Ψάχνει για "img_00001_16-QAM_*.png"
    search_pattern = os.path.join(images_dir, f"img_{count:05d}_{mod}_*.png")
    matching_files = glob.glob(search_pattern)
    
    if len(matching_files) > 0:
        image_path = matching_files[0]
    else:
        print(f"Προειδοποίηση: Δεν βρέθηκε η εικόνα για Count={count} και Mod={mod}! Παράβλεψη.")
        continue 
    
    # Μετάφραση σε κείμενο
    pn_text = "Yes, phase noise is present." if pn > 0 else "No, there is no phase noise."
    iq_text = "Yes, there is visible I/Q imbalance." if iq > 0 else "No, there is no I/Q imbalance."
    jam_text = "Yes, external interference is present." if jam > 0 else "No, there is no interference."
    
    # Οι ερωταπαντήσεις
    qa_pairs = [
        {
            "question": "What modulation scheme is shown in this constellation diagram?",
            "answer": f"The modulation scheme is {mod}."
        },
        {
            "question": "Is there phase noise present in this signal?",
            "answer": pn_text
        },
        {
            "question": "Does this signal suffer from I/Q imbalance?",
            "answer": iq_text
        },
        {
            "question": "What is the SNR range of this signal?",
            "answer": f"The SNR is around {snr} dB."
        },
        {
            "question": "Describe all the characteristics and impairments of this constellation diagram.",
            "answer": f"This is a {mod} signal at an SNR of {snr} dB. Phase noise: {'Yes' if pn>0 else 'No'}. I/Q imbalance: {'Yes' if iq>0 else 'No'}."
        }
    ]
    
    for qa in qa_pairs:
        conversation = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "url": image_path},
                        {"type": "text", "text": qa["question"]}
                    ]
                },
                {
                    "role": "assistant",
                    "content": [
                        {"type": "text", "text": qa["answer"]}
                    ]
                }
            ]
        }
        dataset_entries.append(conversation)

# Ανακάτεμα για σωστή εκπαίδευση
print("Ανακάτεμα των δεδομένων (Shuffling)...")
random.shuffle(dataset_entries)

# Αποθήκευση
with open(output_jsonl, 'w', encoding='utf-8') as f:
    for entry in dataset_entries:
        f.write(json.dumps(entry) + '\n')

print(f"ΕΠΙΤΥΧΙΑ! Δημιουργήθηκαν {len(dataset_entries)} συνομιλίες και αποθηκεύτηκαν στο '{output_jsonl}'.")