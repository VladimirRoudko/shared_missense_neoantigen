#!/bin/bash
# Version 3.0: fixed several bugs:
# sequence_cleaner.py: getting unique list of IDs from redundand list
# netMHCpan4: getting predictions of KD values.
# main: changed the queue line for pan predictions based on efficiency.


# source config file:
. config.sh

# get protein sequences from BioMart in fasta format:
#echo "Getting protein sequences, biomart ... "
#cat $INPUT_FILE | awk '{print $1}' | sort -u | while read GENE
#do
#Rscript get_protein_fasta.R $GENE
#cat "tmp.txt" >> "protein_sequences.fasta" 
#rm "tmp.txt"
#done
#echo "Getting protein sequences, biomart ... done"

# get long peptides from protein sequences with WT and MT sequences:
# script produces three files:
# missense_peptide_17.fasta - for 9-mer prediction
# missense_peptide_19.fasta - for 10-mer prediction
# missense_peptide_21.fasta - for 11-mer prediction
#echo "Getting peptides from proteins ... "
#$PTN get_peptide_fasta.py "$INPUT_FILE" "protein_sequences.fasta"
#echo "Getting peptides from proteins ... done"

# clean protein sequences from duplicates and save in clear_protein_sequences.fasta:
echo "Removing duplicates ... "
$PTN sequence_cleaner.py "missense_peptide_17.fasta"
$PTN sequence_cleaner.py "missense_peptide_19.fasta"
$PTN sequence_cleaner.py "missense_peptide_21.fasta"
echo "Removing duplicates ... done"

echo "Mutate input peptide sequences ... "
$PTN get_mutated_peptide.py "clear_missense_peptide_17.fasta" "mut_clear_missense_peptide_17.fasta"
$PTN get_mutated_peptide.py "clear_missense_peptide_19.fasta" "mut_clear_missense_peptide_19.fasta"
$PTN get_mutated_peptide.py "clear_missense_peptide_21.fasta" "mut_clear_missense_peptide_21.fasta"

echo "Mutate input peptide sequences ... done"


# predict neoantigens from long peptides using 4 different callers and 3-antigen lengths: 9, 10 and 11mers:
echo "Predicting neoantigens ... "
$PTN missense.neoantigen.3.4.py "mut_clear_missense_peptide_17.fasta" "9" "X9mer.binders.netMHC3.4.txt" &
$PTN missense.neoantigen.4.0.py "mut_clear_missense_peptide_17.fasta" "9" "X9mer.binders.netMHC4.0.txt" &
wait
$PTN missense.neoantigen.3.4.py "mut_clear_missense_peptide_19.fasta" "10" "X10mer.binders.netMHC3.4.txt" &
$PTN missense.neoantigen.4.0.py "mut_clear_missense_peptide_19.fasta" "10" "X10mer.binders.netMHC4.0.txt" &
wait
$PTN missense.neoantigen.3.4.py "mut_clear_missense_peptide_21.fasta" "11" "X11mer.binders.netMHC3.4.txt" &
$PTN missense.neoantigen.4.0.py "mut_clear_missense_peptide_21.fasta" "11" "X11mer.binders.netMHC4.0.txt" &
wait
#$PTN missense.neoantigen.3pan.py "mut_clear_missense_peptide_17.fasta" "9" "X9mer.binders.netMHCpan3.0.txt" &
$PTN missense.neoantigen.4pan.py "mut_clear_missense_peptide_17.fasta" "9" "X9mer.binders.netMHCpan4.0.txt" &
wait
#$PTN missense.neoantigen.3pan.py "mut_clear_missense_peptide_19.fasta" "10" "X10mer.binders.netMHCpan3.0.txt" &
$PTN missense.neoantigen.4pan.py "mut_clear_missense_peptide_19.fasta" "10" "X10mer.binders.netMHCpan4.0.txt" &
wait
#$PTN missense.neoantigen.3pan.py "mut_clear_missense_peptide_21.fasta" "11" "X11mer.binders.netMHCpan3.0.txt" &
$PTN missense.neoantigen.4pan.py "mut_clear_missense_peptide_21.fasta" "11" "X11mer.binders.netMHCpan4.0.txt" &
wait


echo "Predicting neoantigens ... done"
echo "calculation completed"
