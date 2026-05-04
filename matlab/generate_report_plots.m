% --- Καθαρισμός ---
clc; clear; close all;

% Ρυθμίσεις για όμορφα γραφήματα (Font size κλπ)
set(0, 'DefaultAxesFontSize', 12);
set(0, 'DefaultLineLineWidth', 2);

% Δημιουργία φακέλου για τις εικόνες του report
if ~exist('report_plots', 'dir'), mkdir('report_plots'); end

num_symbols = 2000; % Χρησιμοποιούμε αρκετά σύμβολα για να φαίνεται η κατανομή

%% --- PLOT 1: Σύγκριση Ιδανικών Διαμορφώσεων (Θεωρία) ---
figure('Name', 'Ideal Constellations', 'NumberTitle', 'off', 'Position', [100, 100, 1000, 800]);

% 16-QAM
subplot(2,2,1);
[~, tx] = generate_impaired_signal('QAM', 16, num_symbols, 30, 0, 0, 0, 0); % Υψηλό SNR για να φαίνεται ιδανικό
plot(real(tx), imag(tx), 'b.', 'MarkerSize', 10);
title('Ιδανικό 16-QAM'); xlabel('In-phase (I)'); ylabel('Quadrature (Q)');
axis square; grid on; xlim([-1.5 1.5]); ylim([-1.5 1.5]);

% 32-APSK (Δακτύλιοι)
subplot(2,2,2);
[~, tx] = generate_impaired_signal('APSK', 32, num_symbols, 30, 0, 0, 0, 0);
plot(real(tx), imag(tx), 'r.', 'MarkerSize', 10);
title('Ιδανικό 32-APSK'); xlabel('In-phase (I)'); ylabel('Quadrature (Q)');
axis square; grid on; xlim([-1.5 1.5]); ylim([-1.5 1.5]);

% 8-ASK (Μονοδιάστατο)
subplot(2,2,3);
[~, tx] = generate_impaired_signal('ASK', 8, num_symbols, 30, 0, 0, 0, 0);
plot(real(tx), imag(tx), 'g.', 'MarkerSize', 10);
title('Ιδανικό 8-ASK'); xlabel('In-phase (I)'); ylabel('Quadrature (Q)');
axis square; grid on; xlim([-1.5 1.5]); ylim([-0.5 0.5]); % Στενεύουμε το Y

% 16-HQAM (Ιεραρχικό - Clusters)
subplot(2,2,4);
[~, tx] = generate_impaired_signal('HQAM', 16, num_symbols, 30, 0, 0, 0, 0);
plot(real(tx), imag(tx), 'm.', 'MarkerSize', 10);
title('Ιδανικό 16-HQAM'); xlabel('In-phase (I)'); ylabel('Quadrature (Q)');
axis square; grid on; xlim([-2 2]); ylim([-2 2]);

% Αποθήκευση
saveas(gcf, 'report_plots/ideal_constellations.png');


%% --- PLOT 2: Επίδραση Ατελειών σε 64-QAM (Πράξη) ---
figure('Name', 'Impairments Effects', 'NumberTitle', 'off', 'Position', [150, 150, 1000, 800]);
Mod = 'QAM'; M = 64;

% Α. Μόνο Θόρυβος (AWGN)
subplot(2,2,1);
[rx, ~] = generate_impaired_signal(Mod, M, num_symbols, 12, 0, 0, 0, 0); % Χαμηλό SNR (12dB)
plot(real(rx), imag(rx), 'b.', 'MarkerSize', 6);
title('64-QAM με Θόρυβο (SNR=12dB)'); xlabel('I'); ylabel('Q');
axis square; grid on; xlim([-2 2]); ylim([-2 2]);

% Β. Θόρυβος Φάσης (Phase Noise)
subplot(2,2,2);
[rx, ~] = generate_impaired_signal(Mod, M, num_symbols, 30, 0.12, 0, 0, 0); % Υψηλό PN (0.12 rad)
plot(real(rx), imag(rx), 'r.', 'MarkerSize', 6);
title('64-QAM με Θόρυβο Φάσης (\sigma_\phi=0.12 rad)'); xlabel('I'); ylabel('Q');
axis square; grid on; xlim([-2 2]); ylim([-2 2]);

% Γ. I/Q Imbalance (Ανισορροπία)
subplot(2,2,3);
[rx, ~] = generate_impaired_signal(Mod, M, num_symbols, 30, 0, 0.25, 10, 0); % Υψηλό Imbalance
plot(real(rx), imag(rx), 'g.', 'MarkerSize', 6);
title('64-QAM με I/Q Imbalance (Gain=0.25, Phase=10^o)'); xlabel('I'); ylabel('Q');
axis square; grid on; xlim([-2 2]); ylim([-2 2]);

% Δ. Παρεμβολή (Jamming)
subplot(2,2,4);
[rx, ~] = generate_impaired_signal(Mod, M, num_symbols, 25, 0, 0, 0, 0.4); % Jamming Power = 0.4
plot(real(rx), imag(rx), 'm.', 'MarkerSize', 6);
title('64-QAM με Παρεμβολή Jamming'); xlabel('I'); ylabel('Q');
axis square; grid on; xlim([-2 2]); ylim([-2 2]);

% Αποθήκευση
saveas(gcf, 'report_plots/impairments_effects.png');


%% --- PLOT 3: Εστίαση στο HQAM (Clusters) ---
figure('Name', 'HQAM Detail', 'NumberTitle', 'off', 'Position', [200, 200, 600, 500]);
[rx, tx] = generate_impaired_signal('HQAM', 16, num_symbols, 18, 0.05, 0, 0, 0); % Μέτριες ατέλειες

plot(real(rx), imag(rx), 'b.', 'MarkerSize', 8);
hold on;
plot(real(tx), imag(tx), 'ro', 'MarkerSize', 12, 'LineWidth', 2); % Ιδανικά κέντρα με κόκκινο κύκλο
title('16-HQAM: Received (μπλε) vs Ideal (κόκκινο)'); xlabel('I'); ylabel('Q');
axis square; grid on; xlim([-2 2]); ylim([-2 2]);
legend('Λαμβανόμενα Σύμβολα', 'Ιδανικές Θέσεις', 'Location', 'northeastoutside');

% Αποθήκευση
saveas(gcf, 'report_plots/hqam_detail.png');

disp('Τα γραφήματα για την αναφορά δημιουργήθηκαν στον φάκελο report_plots/');
close all; % Κλείνει τα παράθυρα για να μην γεμίσει η οθόνη