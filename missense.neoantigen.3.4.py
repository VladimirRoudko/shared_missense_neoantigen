from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Seq import MutableSeq
from Bio.Alphabet import IUPAC
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_protein
import sys
import subprocess
import os
from collections import defaultdict
from subprocess import Popen, PIPE

os.system('mkdir -p netMHC3')
alleles = subprocess.check_output(os.environ["netMHC3"]+' -A | grep "HLA-" | grep -v "#"', shell=True).decode('ascii')
output = open(sys.argv[3],"w")
for allele in alleles.split():
	os.system(os.environ["netMHC3"]+' -a '+allele+' -l '+sys.argv[2]+' '+sys.argv[1]+' > netMHC3/'+allele+'.neoantigens.txt')


my_txtlist = subprocess.check_output('ls netMHC3', shell=True).decode('ascii')


for txt_file in my_txtlist.split():
	my_input = open('netMHC3/'+txt_file,"r")
	for line in my_input:
		sep = line.split()
#		print(sep)
		if len(sep)==7:
			FRAME = sep[0]
			seq = sep[1]
			log = sep[2]
			KD = sep[3]
			ID = sep[5]
			allele = sep[6]
			ID_sep = ID.split(".")
			GENE = ID_sep[0]
			FLAG = ID_sep[1]
			COORD = ID_sep[2]
			if FLAG == "M":
				WT_ID=GENE+".W."+COORD
				if float(KD) <= 500:
					m_string = "netMHC3.4 "+str(ID)+" "+str(allele)+" "+str(seq)+" "+str(KD)+" NA\n"
					COMMAND = "grep '"+WT_ID+"' netMHC3/"+txt_file+" | awk '$1 == "+FRAME+"'"
					string = subprocess.check_output(COMMAND, shell=True).decode('ascii')
					wt_sep = string.split()
					WT_PEPTIDE = wt_sep[1]
					WT_KD = wt_sep[3]			
					w_string = "netMHC3.4 "+str(WT_ID)+" "+str(allele)+" "+str(WT_PEPTIDE)+" "+str(WT_KD)+"  NA\n"
					output.write(m_string)
					output.write(w_string)
	my_input.close()

output.close()

os.system('rm -rf netMHC3')


