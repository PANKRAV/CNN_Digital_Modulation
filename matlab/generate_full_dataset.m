mod_families = {'ASK','BPSK','QPSK','HQAM','HQAM','HQAM','QAM','QAM','QAM','QAM','QAM','APSK','APSK','APSK','APSK'};

M_values = [8,2,4,4,16,64,16,32,64,128,256,16,32,64,128];

snr_levels    = [5, 15, 25];
phase_noises  = [0, 0.08];
iq_imbalances = [0, 0.15];
jammings      = [0, 0.2];

num_symbols = 1024;
num_images  = 10;
task = 0;

bool_labels = ["false","true"];



if ~exist('../data/images', 'dir')
    mkdir('../data/images');
end

pool = gcp('nocreate');

if isempty(pool)
    parpool(8);
elseif pool.NumWorkers ~= 8
    delete(pool);
    parpool(8);
end

disp('Generating data')

num_mods = length(mod_families);

parfor m_idx = 1:num_mods
    tic

    csv_lines = strings(24000, 1); idx = 1;

    mod_fam = mod_families{m_idx};
    M       = M_values(m_idx);

    mod_label = sprintf('%d-%s', M, mod_fam);
    
    if m_idx<9
        fprintf('Worker %d -> %s\n', getCurrentTask().ID, mod_label);
    else
        fprintf('Worker %d -> %s New Task\n', getCurrentTask().ID, mod_label);
    end

    for snr = snr_levels
        if snr <= 10
            snr_label = sprintf('Low%d', snr);
        elseif snr <= 20
            snr_label = sprintf('Medium%d', snr);
        else
            snr_label = sprintf('High%d', snr)'; 
        end
        for pn = phase_noises

            pn_label = bool_labels((pn > 0) + 1); %#ok<PFBNS>

            for iq = iq_imbalances

                iq_label = bool_labels((iq > 0) + 1);

                for jam = jammings

                    jam_label = bool_labels((jam > 0) + 1);


                    for i = 1:num_images

                        [rx_sig, ~] = generate_impaired_signal(mod_fam, M, num_symbols, snr, pn, iq, 5, jam);

                        img = render_constellation(rx_sig);

                        img_name = sprintf('img_%05d_%s_%s_%s_%s_%s.png',i, mod_label, pn_label, iq_label,jam_label, snr_label);


                        imwrite(img, fullfile('../data/images', img_name));

                        csv_lines(idx) = sprintf( '%d,%s,%.2f,%.2f,%.2f,%d',i, mod_label, pn, iq, jam, snr);

                        idx = idx + 1;

                    end
                end
            end
        end
    end

    csv_path = fullfile('../data', sprintf('labels_worker_%02d.csv', m_idx));

    fid = fopen(csv_path, 'w');

    fprintf(fid, 'id,mod,pn,iq,jam,snr\n');

    for k = 1:length(csv_lines)
        fprintf(fid, '%s\n', csv_lines(k));
    end

    fprintf('Worker %d -> %s finished in %.2f seconds\n', getCurrentTask().ID, mod_label, toc);
    
    fclose(fid);


end

disp('DONE');