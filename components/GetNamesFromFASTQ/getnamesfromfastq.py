from anduril.args import *
from fastq import FastqParser


outfh = open(namelist, 'w')
fqp = FastqParser()

for rec in fqp.parse(open(fastqfile)):
	outfh.write("%s\n" % rec.header[1:])
outfh.close()


