#!/usr/bin/env python
# coding: utf-8

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Seq import MutableSeq
from Bio.Alphabet import IUPAC
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_protein
import sys
import subprocess
import os

array_gene=[]
array_wt_aa=[]
array_mutant_aa=[]
array_position_aa=[]
array_coord=[]

for my_record in open(sys.argv[1]):
    my_gene=my_record.strip().split("\t")[0]
    my_mutation_coord=my_record.strip().split("\t")[1]
    my_wt_aa=my_mutation_coord[0]
    my_mutant_aa=my_mutation_coord[-1]
    my_position_aa=my_mutation_coord[1:-1]
    #print(my_gene,my_wt_aa,my_mutant_aa,my_position_aa)
    array_gene.append(my_gene)
    array_wt_aa.append(my_wt_aa)
    array_mutant_aa.append(my_mutant_aa)
    array_position_aa.append(my_position_aa)
    array_coord.append(my_mutation_coord)

output=[]
output_19=[]
output_21=[]
#array_mutpos_aa = list(map(int, array_position_aa[1:len(array_position_aa)]))
numtimes=len(array_gene)

for seq_record in SeqIO.parse(sys.argv[2], 'fasta'):
    identifier=seq_record.id
    sequence=seq_record.seq
    for i in range(0,numtimes): 
        gene=array_gene[i]
	end_side=len(sequence) - 11
        if gene==identifier:
            if len(sequence) > int(array_position_aa[i]) and int(array_position_aa[i]) >= 11 and int(array_position_aa[i]) <= int(end_side):
                if(sequence[int(array_position_aa[i])-1]==array_wt_aa[i]):
                    pre_mutation_17=sequence[int(array_position_aa[i])-9:int(array_position_aa[i])-1]
                    post_mutation_17=sequence[int(array_position_aa[i]):int(array_position_aa[i])+8]
                    wt_sequence_17=pre_mutation_17+"Z"+post_mutation_17
                    #mut_sequence_17=pre_mutation_17+array_mutant_aa[i]+post_mutation_17 
                    wt_header=gene+"."+str(array_coord[i])
                    #mut_header=gene+".M."+str(array_coord[i])
                    record=SeqRecord(wt_sequence_17, id=wt_header, description="")
                    output.append(record)
                    #record=SeqRecord(mut_sequence_17,id=mut_header,description="")
                    #output.append(record)
                    
                    pre_mutation_19=sequence[int(array_position_aa[i])-10:int(array_position_aa[i])-1]
                    post_mutation_19=sequence[int(array_position_aa[i]):int(array_position_aa[i])+9]
                    wt_sequence_19=pre_mutation_19+"Z"+post_mutation_19
                    #mut_sequence_19=pre_mutation_19+array_mutant_aa[i]+post_mutation_19 
                    wt_header_19=gene+"."+str(array_coord[i])
                    #mut_header_19=gene+".M."+str(array_coord[i])
                    record=SeqRecord(wt_sequence_19, id=wt_header_19, description="")
                    output_19.append(record)
                    #record=SeqRecord(mut_sequence_19,id=mut_header_19,description="")
                    #output_19.append(record)
                    
                    pre_mutation_21=sequence[int(array_position_aa[i])-11:int(array_position_aa[i])-1]
                    post_mutation_21=sequence[int(array_position_aa[i]):int(array_position_aa[i])+10]
                    wt_sequence_21=pre_mutation_21+"Z"+post_mutation_21
                    #mut_sequence_21=pre_mutation_21+array_mutant_aa[i]+post_mutation_21 
                    wt_header_21=gene+"."+str(array_coord[i])
                    #mut_header_21=gene+".M."+str(array_coord[i])
                    record=SeqRecord(wt_sequence_21, id=wt_header_21, description="")
                    output_21.append(record)
                    #record=SeqRecord(mut_sequence_21,id=mut_header_21,description="")
                    #output_21.append(record)
                    
SeqIO.write(output,"missense_peptide_17.fasta","fasta")
SeqIO.write(output_19,"missense_peptide_19.fasta", "fasta")
SeqIO.write(output_21,"missense_peptide_21.fasta", "fasta")



