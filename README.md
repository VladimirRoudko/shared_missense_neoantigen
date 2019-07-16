# shared_missense_neoantigen


Pipeline predicts tumor neoantigens (9-mer, 10-mer and 11-mer) and matching normal tissue antigens from missense mutations. It starts with two-column table: GENE<tab>COORD, where 
  GENE - hgnc_symbol and 
  COORD - mutation coordinate in protein sequence in the XPOSY format: X - wt-type aminoacid residue in one-letter code; POS - position in the reference protein sequence; Y - mutant aminoacid residue in one-letter code.

Requirements:
Unix environment, with Bash shell

R version 3.6.0 (2019-04-26); Platform: x86_64-redhat-linux-gnu (64-bit) and libraries:
BiomaRt library, with installed dependencies

Python 2.7.5 and libraries:
Biopython with installed dependencies

Installed and configured NetMHC.3.4, NetMHC.4.0, NetMHC-pan.3.0 and MetMHC-pan.4.0.

Before the run, configure the file config.sh according to the user machine/environment.
