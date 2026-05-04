clc; clear; close all;

% Φτιάχνουμε τον φάκελο 'my_dataset'
if ~exist('my_dataset', 'dir')
    mkdir('my_dataset'); 
end

% Δημιουργία του αρχείου Labels
csv_fileID = fopen('dataset_labels.csv', 'w');
fprintf(csv_fileID, 'Image_Name,Modulation,Phase_Noise,IQ_Imbalance,Interference,SNR_Range\n');

% --- Ορισμός Παραμέτρων βάσει Εκφώνησης ---
mod_families = {'ASK', 'BPSK', 'QPSK', 'HQAM', 'HQAM', 'HQAM', 'QAM', 'QAM', 'QAM', 'QAM', 'QAM', 'APSK', 'APSK', 'APSK', 'APSK'};
M_values     = [8,     2,      4,      4,      16,     64,     16,    32,    64,    128,   256,   16,     32,     64,     128];

snr_levels = [5, 15, 25];         % Low (5dB), Medium (15dB), High (25dB)
phase_noises = [0, 0.08];         % 0 = Όχι, 0.08 = Ναι
iq_imbalances = [0, 0.15];        % 0 = Όχι, 0.15 = Ναι
jammings = [0, 0.2];              % 0 = Όχι, 0.2 = Ναι

num_symbols = 1024;
image_counter = 1;

disp('Ξεκινάει η παραγωγή του Dataset. Παρακαλώ περιμένετε...');

% --- Βρόχοι (Loops) Παραγωγής ---
for m_idx = 1:length(mod_families)
    mod_fam = mod_families{m_idx};
    M = M_values(m_idx);
    
    for snr = snr_levels
        for pn = phase_noises
            for iq = iq_imbalances
                for jam = jammings
                    for i=1:10000
                    
                        % 1. Παραγωγή Σήματος
                        [rx_sig, ~] = generate_impaired_signal(mod_fam, M, num_symbols, snr, pn, iq, 5, jam);
                        
                        % 2. Ονομασία και Αποθήκευση Εικόνας
                        img_name = sprintf('img_%05d_%s_%s_%s_%s_%s.png', image_counter, mod_label, pn_label, iq_label, jam_label, snr_label);
                        
                        % ΕΔΩ ΕΙΝΑΙ Η ΔΙΟΡΘΩΣΗ: Αποθήκευση στον φάκελο 'my_dataset'
                        filepath = fullfile('my_dataset', img_name);
                        
                        fig = figure('Visible', 'off');
                        scatter(real(rx_sig), imag(rx_sig), 8, 'b', 'filled');
                        axis square; axis off;
                        xlim([-2.5 2.5]); ylim([-2.5 2.5]);
                        exportgraphics(fig, filepath, 'Resolution', 64);
                        close(fig);
                        
                        % 3. Δημιουργία Ετικετών (Labels)
                        if strcmp(mod_fam, 'BPSK') || strcmp(mod_fam, 'QPSK')
                            mod_label = mod_fam;
                        else
                            mod_label = sprintf('%d-%s', M, mod_fam);
                        end
                        
                        pn_label  = mat2str(pn > 0);   
                        iq_label  = mat2str(iq > 0);
                        jam_label = mat2str(jam > 0);
                        
                        if snr <= 10
                            snr_label = 'Low';
                        elseif snr <= 20
                            snr_label = 'Medium';
                        else
                            snr_label = 'High'; 
                        end
                        
                        % 4. Εγγραφή στο CSV
                        fprintf(csv_fileID, '%s,%s,%s,%s,%s,%s\n', img_name, mod_label, pn_label, iq_label, jam_label, snr_label);
                        
                        image_counter = image_counter + 1;
                    end
                end
            end
        end
    end
end

fclose(csv_fileID);
disp('Το Dataset ολοκληρώθηκε με επιτυχία!');