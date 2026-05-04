clc; clear; close all;

% Παράμετροι Προσομοίωσης SEP
snr_vec = 0:2:24;           % Εύρος SNR από 0 έως 24 dB
M_vec = [16, 64];           % Τάξεις QAM για σύγκριση
phase_noise_std = 0.06;     % Επίπεδο Θορύβου Φάσης (σε ακτίνια)
num_symbols = 50000;        % Αριθμός συμβόλων για αξιόπιστη στατιστική

figure('Name', 'SEP vs SNR', 'NumberTitle', 'off');
hold on; grid on;
colors = ['b', 'r'];
markers = ['o', 's'];

for m_idx = 1:length(M_vec)
    M = M_vec(m_idx);
    sep_sim = zeros(length(snr_vec), 1);
    
    for i = 1:length(snr_vec)
        snr = snr_vec(i);
        
        % 1. Πομπός
        data_tx = randi([0 M-1], num_symbols, 1);
        tx_sig = qammod(data_tx, M, 'UnitAveragePower', true);
        
        % 2. Κανάλι με Phase Noise & AWGN
        phi_noise = phase_noise_std * randn(num_symbols, 1);
        rx_sig = tx_sig .* exp(1j * phi_noise);
        rx_sig = awgn(rx_sig, snr, 'measured');
        
        % 3. Δέκτης
        data_rx = qamdemod(rx_sig, M, 'UnitAveragePower', true);
        
        % 4. Υπολογισμός SEP
        num_errors = sum(data_tx ~= data_rx);
        sep_sim(i) = num_errors / num_symbols;
    end
    
    % Σχεδίαση
    semilogy(snr_vec, sep_sim, ['-' markers(m_idx)], 'Color', colors(m_idx), ...
        'LineWidth', 2, 'DisplayName', sprintf('%d-QAM', M));
end

% Μορφοποίηση Γραφήματος
set(gca, 'YScale', 'log');
ylim([1e-4 1]);
xlabel('Λόγος Σήματος προς Θόρυβο - SNR (dB)');
ylabel('Πιθανότητα Σφάλματος Συμβόλου (SEP)');
title(sprintf('Καμπύλες SEP για QAM με Phase Noise (\\sigma_\\phi = %.2f rad)', phase_noise_std));
legend('Location', 'southwest');