function [rx_sig, tx_sig] = generate_impaired_signal(mod_family, M, num_symbols, snr_db, phase_noise_std, iq_gain_imb, iq_phase_imb, jamming_power)
    % mod_family: 'ASK', 'BPSK', 'QPSK', 'QAM', 'APSK', 'HQAM'
    
    % 1. Παραγωγή Σήματος Ζώνης Βάσης (Baseband)
    switch mod_family
        case 'ASK'
            data = randi([0 M-1], num_symbols, 1);
            tx_sig = pammod(data, M);
            
        case 'BPSK'
            data = randi([0 1], num_symbols, 1);
            tx_sig = pskmod(data, 2);
            
        case 'QPSK'
            data = randi([0 3], num_symbols, 1);
            tx_sig = pskmod(data, 4, pi/4);
            
        case 'QAM'
            data = randi([0 M-1], num_symbols, 1);
            tx_sig = qammod(data, M);
            
        case 'APSK'
            data = randi([0 M-1], num_symbols, 1);
            
            % --- Η ΟΡΙΣΤΙΚΗ ΔΙΟΡΘΩΣΗ ΓΙΑ ΤΟ APSK ---
            % Ορίζουμε τα σημεία ανά δακτύλιο (M_vec) και τις ακτίνες (radii)
            if M == 16
                M_vec = [4, 12];
                radii = [1, 2.73];
            elseif M == 32
                M_vec = [4, 12, 16];
                radii = [1, 2.84, 5.27];
            elseif M == 64
                M_vec = [4, 12, 20, 28];
                radii = [1, 2.2, 3.4, 4.6];
            elseif M == 128
                M_vec = [4, 12, 20, 28, 64];
                radii = [1, 2, 3, 4, 5];
            else
                M_vec = [M/2, M/2]; % Ασφαλής επιλογή ανάγκης
                radii = [1, 2];
            end
            
            try
                % Δοκιμή για νέες εκδόσεις MATLAB
                tx_sig = apskmod(data, M); 
            catch
                % Για την έκδοσή σου: Δίνουμε το διάνυσμα M_vec και τις ακτίνες
                tx_sig = apskmod(data, M_vec, radii); 
            end
            % ---------------------------------------
            
        case 'HQAM'
            if M == 4
                data = randi([0 3], num_symbols, 1);
                tx_sig = pskmod(data, 4, pi/4);
            elseif M == 16
                data_HP = randi([0 3], num_symbols, 1);
                data_LP = randi([0 3], num_symbols, 1);
                tx_sig = 2.5 * pskmod(data_HP, 4, pi/4) + pskmod(data_LP, 4, pi/4);
            elseif M == 64
                data_HP = randi([0 3], num_symbols, 1);
                data_LP = randi([0 15], num_symbols, 1);
                tx_sig = 4 * pskmod(data_HP, 4, pi/4) + qammod(data_LP, 16);
            else
                tx_sig = qammod(randi([0 M-1], num_symbols, 1), M);
            end
            
        otherwise
            error('Άγνωστη διαμόρφωση!');
    end
    
    % 2. Κανονικοποίηση Ενέργειας (Energy Normalization) Es = 1
    tx_sig = tx_sig / sqrt(mean(abs(tx_sig).^2));
    rx_sig = tx_sig;
    
    % 3. Εφαρμογή Phase Noise (Τυχαία διεργασία φάσης)
    if phase_noise_std > 0
        phi_noise = phase_noise_std * randn(num_symbols, 1);
        rx_sig = rx_sig .* exp(1j * phi_noise);
    end
    
    % 4. Εφαρμογή I/Q Imbalance
    if iq_gain_imb ~= 0 || iq_phase_imb ~= 0

    p = (pi/180) * iq_phase_imb;

    I = real(rx_sig);
    Q = imag(rx_sig);

    rx_sig = rx_sig + (1 + iq_gain_imb) * (Q * cos(p) - I * sin(p))*1j;

    end
    
    % 5. Εξωτερική Παρεμβολή (Jamming) - Προσθήκη τόνου
    if jamming_power > 0
        t = (0:num_symbols-1)';
        jammer = sqrt(jamming_power) * exp(1j * 2 * pi * 0.1 * t);
        rx_sig = rx_sig + jammer;
    end
    
    % 6. Εφαρμογή AWGN (Θόρυβος βάσει επιπέδου SNR)
    rx_sig = awgn(rx_sig, snr_db, 'measured');
end