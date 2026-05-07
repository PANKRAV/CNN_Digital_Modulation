import sys, os, pathlib
sys.path.append(os.getcwd())
from src.modules.utility import Dir_Reset, get_dirs


mod_families = ['ASK', 'BPSK', 'QPSK', 'HQAM', 'HQAM', 'HQAM', 'QAM', 'QAM', 'QAM', 'QAM', 'QAM', 'APSK', 'APSK', 'APSK', 'APSK']
M_values     = [8,     2,      4,      4,      16,     64,     16,    32,    64,    128,   256,   16,     32,     64,     128]

snr_levels = [5, 15, 25]
phase_noises = [0, 0.08]        
iq_imbalances = [0, 0.15]  
jammings = [0, 0.2];             

num_symbols = 1024
image_counter = 1




def main() -> None :
    for mod_fam in mod_families:
        ...






if __name__ == "__main__":
    main()