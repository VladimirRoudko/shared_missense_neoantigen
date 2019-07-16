import sys
import os
from Bio import SeqIO

def sequence_cleaner(fasta_file, min_length=0, por_n=100):
    # Create our hash table to add the sequences
    sequences={}
    flag=0
    seq_flag="@"
    # Using the Biopython fasta parse we can read our fasta input
    for seq_record in SeqIO.parse(fasta_file, "fasta"):
        # Take the current sequence
	sequence = str(seq_record.seq).strip().upper()
	ID = str(seq_record.id).strip().upper()
        # Check if the current sequence is according to the user parameters
        if (len(sequence) >= min_length and
            (float(sequence.count("N"))/float(len(sequence)))*100 <= por_n):
        # If the sequence passed in the test "is it clean?" and it isn't in the
        # hash table, the sequence and its id are going to be in the hash
            if sequence not in sequences:
		if ID not in sequences.values():
                	sequences[sequence] = ID
		else:
			#print(seq_record.id)
			#ID = str(seq_record.id)
			GENE = ID.split(".")[0]
			COORD = ID.split(".")[1]
			#print(GENE, COORD)
			GENE = GENE+"v"+str(flag)
			#print(GENE)
			ID = GENE+"."+COORD
			#seq_record.id = ID
			#print(seq_record.id)
			sequences[sequence] = ID
			flag = flag + 1
       # If it is already in the hash table, we're just gonna concatenate the ID
       # of the current sequence to another one that is already in the hash table
            else:
		if ID not in sequences.values():
			print(ID, sequence)
			sequences[sequence+seq_flag] = ID
			seq_flag=seq_flag+"@"
                else:
			continue


    # Write the clean sequences

    # Create a file in the same directory where you ran this script
    with open("clear_" + fasta_file, "w+") as output_file:
        # Just read the hash table and write on the file as a fasta format
        for sequence in sequences:
            output_file.write(">" + sequences[sequence] + "\n" + sequence + "\n")
    os.system("sed 's/@//g' clear_"+fasta_file+" > tmp")
    os.system("cat tmp > clear_"+fasta_file)
    os.system("rm tmp")
    print("CLEAN!!!\nPlease check clear_" + fasta_file)


userParameters = sys.argv[1:]

try:
    if len(userParameters) == 1:
        sequence_cleaner(userParameters[0])
    elif len(userParameters) == 2:
        sequence_cleaner(userParameters[0], float(userParameters[1]))
    elif len(userParameters) == 3:
        sequence_cleaner(userParameters[0], float(userParameters[1]),
                         float(userParameters[2]))
    else:
        print("There is a problem!")
except:
    print("There is a problem!")
