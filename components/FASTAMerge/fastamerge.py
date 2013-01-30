from anduril.args import *
from fasta import fasta_itr


outfh = open(output, 'w')
for fastafile in array:
	for rec in fasta_itr(fastafile):
		outfh.write(str(rec) + "\n")
outfh.close()


