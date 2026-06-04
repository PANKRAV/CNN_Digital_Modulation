import pandas as pd
import json
import glob
import os

drive_path = '/content/drive/MyDrive/Telecom_Project/'
csv_files = glob.glob(drive_path + 'labels_worker_*.csv')
output_jsonl = drive_path + 'vqa_dataset.jsonl'

dataset_entries = []
print(f"Βρέθηκαν {len(csv_files)} CSV αρχεία. Ξεκινάω τη σύνδεση...")

for f in csv_files:
    try:
        df = pd.read_csv(f)
        for _, row in df.iterrows():
            # 1. Ανακατασκευή του ονόματος της εικόνας (όπως το έκανε το MATLAB)
            pn_label = "true" if row['pn'] > 0 else "false"
            iq_label = "true" if row['iq'] > 0 else "false"
            jam_label = "true" if row['jam'] > 0 else "false"
            
            # Υπολογισμός του SNR Label (Low/Medium/High + τιμή)
            snr_val = float(row['snr'])
            if snr_val < 10: snr_cat = "Low"
            elif snr_val < 20: snr_cat = "Medium"
            else: snr_cat = "High"
            snr_label = f"{snr_cat}{snr_val:.2f}"
            
            # Το τελικό όνομα της εικόνας
            img_filename = f"img_{int(row['id']):05d}_{row['mod']}_{pn_label}_{iq_label}_{jam_label}_{snr_label}.png"
            
            # 2. Δημιουργία της εγγραφής
            prompt = "Identify the modulation and impairments in this constellation diagram."
            answer = f"Modulation: {row['mod']}. SNR: {row['snr']:.2f} dB. Impairments: PN({pn_label}), IQ({iq_label}), Jamming({jam_label})."
            
            entry = {
                "messages": [
                    {
                        "role": "user", 
                        "content": [
                            {"type": "image", "url": f"../data/images/{img_filename}"}, 
                            {"type": "text", "text": prompt}
                        ]
                    },
                    {
                        "role": "assistant", 
                        "content": [{"type": "text", "text": answer}]
                    }
                ]
            }
            dataset_entries.append(entry)
    except Exception as e:
        print(f"Σφάλμα στο αρχείο {f}: {e}")

# Αποθήκευση του αρχείου
if len(dataset_entries) > 0:
    with open(output_jsonl, 'w') as f:
        for item in dataset_entries:
            f.write(json.dumps(item) + "\n")
    print(f"✅ ΕΠΙΤΥΧΙΑ! Δημιουργήθηκε το αρχείο με {len(dataset_entries)} γραμμές.")
else:
    print("❌ ΣΦΑΛΜΑ: Το αρχείο παραμένει άδειο. Ελέγξτε αν τα CSV έχουν δεδομένα.")