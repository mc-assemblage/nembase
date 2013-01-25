from anduril.args import *
from fastq import FastqParser


outfh = open(output, 'w')
fqp = FastqParser()
for fastqfile in array:
	for rec in fqp.parse(fastqfile):
		outfh.write(str(rec) + "\n")
outfh.close()


