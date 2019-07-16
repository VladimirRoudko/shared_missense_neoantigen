
#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

#install.packages("biomaRt")

#if (!requireNamespace("BiocManager", quietly = TRUE))
#  install.packages("BiocManager")
#BiocManager::install("biomaRt")
#source("https://bioconductor.org/biocLite.R")
#biocLite("biomaRt")

library("biomaRt")

mart <- useMart("ENSEMBL_MART_ENSEMBL",host="dec2016.archive.ensembl.org")
mart = useDataset("hsapiens_gene_ensembl",mart=mart)

seq = getSequence(id=args[1], 
                  type="hgnc_symbol", 
                  seqType="peptide", mart = mart, verbose=FALSE)

exportFASTA(seq, "tmp.txt")



