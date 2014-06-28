from anduril import constants
from fastq import FastqParser
from sraxmlparser import SRAXMLParser
import anduril.main
import os.path
import subprocess


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


def sra2fastq(cf):
	inputfile = cf.get_input('srafile')
	srafetchxml = cf.get_input('srafetchxml')
	accession = cf.get_parameter('accession', 'string')
	outputfile = cf.get_output('fastqfile')
	params = []
	if isPaired(srafetchxml, accession):
		cf.write_log('Run is paired end.')
		params.append('--split-spot')
	outfh = open(outputfile + '.tmp', 'wb')
	try:
		params.append('-Z')
		params.append(inputfile)
		subprocess.check_call(['fastq-dump'] + params, stdout=outfh)
	except subprocess.CalledProcessError, e:
		cf.write_log("Error running fastq-dump.")
		cf.write_log("Error: %s" % str(e))
		return constants.GENERIC_ERROR
	finally:
		outfh.close()
	#format the fastq headers
	outfh = open(outputfile, 'wb')
	fqp = FastqParser()
	for rec in fqp.parse(open(outputfile + '.tmp', 'U')):
		rec.header = rec.header.split(' ')[1]
		outfh.write(str(rec) + '\n')
	outfh.close()
	return constants.OK
anduril.main(sra2fastq)


