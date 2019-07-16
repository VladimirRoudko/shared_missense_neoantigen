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

os.system('mkdir -p netMHC4')
alleles = subprocess.check_output(os.environ["netMHC4"]+' -listMHC | grep "HLA-" | grep -v "#"', shell=True).decode('ascii')
output = open(sys.argv[3],"w")

for allele in alleles.split():
	os.system(os.environ["netMHC4"]+' -a "'+allele+'" -f "'+sys.argv[1]+'" -l '+sys.argv[2]+' -s 1 -xls 1 -xlsfile "netMHC4/'+allele+'.neoantigens.xls"')


my_excellist = subprocess.check_output('ls netMHC4', shell=True).decode('ascii')


for excel_file in my_excellist.split():
	my_input = open('netMHC4/'+excel_file,"r")
	my_allele = excel_file.split(".")[0]
	for line in my_input:
		if len(line.split()) > 3:
			try:
				FRAME = line.split()[0]
				KD = line.split()[3]            # $(echo $line | awk '{print $4}')
				SCORE = line.split()[6]
				ID = line.split()[2]
				if ID == "ID":
					continue
				FLAG = ID.split("_")[1]
				GENE = ID.split("_")[0]
				COORD = ID.split("_")[2]                # $(echo $line | awk '{print $3}')
				PEPTIDE = line.split()[1]              # $(echo $line | awk '{print $2}')
				if FLAG == "M":
					WT_ID=GENE+"_W_"+COORD
					if float(KD) <= 500:
						m_string = "netMHC4.0 "+ID+" "+my_allele+" "+PEPTIDE+" "+KD+" "+SCORE+"\n"
						COMMAND = "grep '"+WT_ID+"' netMHC4/"+excel_file+" | awk '$1 == "+FRAME+"'"
						string = subprocess.check_output(COMMAND, shell=True).decode('ascii')
						WT_PEPTIDE = string.split()[1]
						WT_KD = string.split()[3]
						WT_SCORE  = string.split()[6]
						w_string = "netMHC4.0 "+WT_ID+" "+my_allele+" "+WT_PEPTIDE+" "+WT_KD+" "+WT_SCORE+"\n"
						output.write(m_string)
						output.write(w_string)
					if float(SCORE) <= 2:
						m_string = "netMHC4.0 "+ID+" "+my_allele+" "+PEPTIDE+" "+KD+" "+SCORE+"\n"
						COMMAND = "grep '"+WT_ID+"' netMHC4/"+excel_file+" | awk '$1 == "+FRAME+"'"
                                                string = subprocess.check_output(COMMAND, shell=True).decode('ascii')
                                                WT_PEPTIDE = string.split()[1]
                                                WT_KD = string.split()[3]
                                                WT_SCORE  = string.split()[6]
                                                w_string = "netMHC4.0 "+WT_ID+" "+my_allele+" "+WT_PEPTIDE+" "+WT_KD+" "+WT_SCORE+"\n"
                                                output.write(m_string)
                                                output.write(w_string)
			except ValueError:
				continue
	my_input.close()

output.close()

os.system('rm -rf netMHC4')

