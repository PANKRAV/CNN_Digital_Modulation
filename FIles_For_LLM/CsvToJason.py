import pandas as pd
import json
import glob
import os

drive_path = '/content/drive/MyDrive/Telecom_Project/'
csv_files = glob.glob(os.path.join(drive_path, 'labels_worker_*.csv'))
output_file = os.path.join(drive_path, 'vqa_dataset.jsonl')

print(f"Επεξεργασία {len(csv_files)} αρχείων...")

# Ανοίγουμε το αρχείο για εγγραφή αμέσως (Streaming) για να σώσουμε τη RAM
with open(output_file, 'w', encoding='utf-8') as f_out:
    count = 0
    for csv_f in csv_files:
        try:
            df = pd.read_csv(csv_f)
            # Καθαρίζουμε τα ονόματα των στηλών
            df.columns = df.columns.str.strip()
            
            for _, row in df.iterrows():
                # --- Πλήρης λογική ανακατασκευής του ονόματος αρχείου ---
                fname_val = str(row['filename'])
                
                pn_lbl  = "true" if float(row['pn']) > 0 else "false"
                iq_lbl  = "true" if float(row['iq']) > 0 else "false"
                jam_lbl = "true" if float(row['jam']) > 0 else "false"
                
                snr_val = float(row['snr'])
                if snr_val < 10:   snr_lbl = f"Low{snr_val:.2f}"
                elif snr_val < 20: snr_lbl = f"Medium{snr_val:.2f}"
                else:              snr_lbl = f"High{snr_val:.2f}"
                
                if not fname_val.startswith('img_'):
                    img_filename = f"img_{int(float(fname_val)):05d}_{row['mod']}_{pn_lbl}_{iq_lbl}_{jam_lbl}_{snr_lbl}.png"
                else:
                    img_filename = fname_val if fname_val.endswith('.png') else fname_val + '.png'

                # --- Δομή για το AI ---
                entry = {
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "image", "url": f"../data/images/{img_filename}"},
                                {"type": "text", "text": "Identify the modulation and impairments in this constellation diagram."}
                            ]
                        },
                        {
                            "role": "assistant",
                            "content": [
                                {"type": "text", "text": f"The modulation is {row['mod']}. SNR: {row['snr']:.2f} dB. Impairments: PN={pn_lbl}, IQ={iq_lbl}, Jamming={jam_lbl}."}
                            ]
                        }
                    ]
                }
                
                # Γράφουμε κατευθείαν στο αρχείο (αδειάζει τη RAM)
                f_out.write(json.dumps(entry) + "\n")
                count += 1
                
        except Exception as e:
            print(f"Σφάλμα στο αρχείο {os.path.basename(csv_f)}: {e}")

print(f"✅ Έτοιμο! Δημιουργήθηκαν {count} γραμμές χωρίς να γεμίσει η RAM.")