from anduril import constants
from anduril.arrayio import get_array
from fastq import FastqParser
from sraxmlparser import SRAXMLParser
import anduril.main
import os.path


def isPaired(srafetchxml, accession):
	"""Check if the run with accession is paired."""
	if accession and \
		srafetchxml and \
		os.path.exists(srafetchxml):
		sraxmlparser = SRAXMLParser()
		runs = sraxmlparser.parse(srafetchxml)
		for run in runs:
			if run.accession.strip() == accession.strip():
				return run.is_paired
	return False


def separatePairsAndSingles(cf):
	"""In an array of runs, separate the paired end reads into two separate files, and 
		the singles into a third."""
	fastqfiles = get_array(cf, 'fastqfiles')
	srafetchxml = cf.get_input('srafetchxml')
	leftfh = open(cf.get_output('left'), 'w')
	rightfh = open(cf.get_output('right'), 'w')
	singlefh = open(cf.get_output('single'), 'w')
	for accession, fastqfile in fastqfiles:
		fqp = FastqParser()
		fastqfh = open(fastqfile, 'U')
		if isPaired(srafetchxml, accession):
			iter = fqp.parse(fastqfh)
			#paired end run
			while True:
				try:
					pe1 = iter.next()
					pe2 = iter.next()
					leftfh.write(str(pe1) + '\n')
					rightfh.write(str(pe2) + '\n')
				except StopIteration:
					break
		else:
			#single end run
			for rec in fqp.parse(fastqfh):
				singlefh.write(str(rec) + '\n')
	leftfh.close()
	rightfh.close()
	singlefh.close()
	return constants.OK
anduril.main(separatePairsAndSingles)


