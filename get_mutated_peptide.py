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

output=[]

for seq_record in SeqIO.parse(sys.argv[1], 'fasta'):
    identifier=seq_record.id
    GENE=identifier.split(".")[0]
    COORD=identifier.split(".")[1]
    wt_aa=COORD[0]
    mutant_aa=COORD[-1]
    sequence=str(seq_record.seq)
    wt_sequence=sequence.replace("Z",str(wt_aa))
    wt_sequence=Seq(wt_sequence)
    mut_sequence=sequence.replace("Z",str(mutant_aa))
    mut_sequence=Seq(mut_sequence)
    wt_header=GENE+".W."+str(COORD)
    mut_header=GENE+".M."+str(COORD)
    record=SeqRecord(wt_sequence, id=wt_header, description="")
    output.append(record)
    record=SeqRecord(mut_sequence,id=mut_header,description="")
    output.append(record)
                    
SeqIO.write(output,sys.argv[2],"fasta")



