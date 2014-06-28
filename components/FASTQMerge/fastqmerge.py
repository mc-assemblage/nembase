from anduril import constants
from anduril.arrayio import get_array
from fastq import FastqParser
import anduril.main


def fastq_merge(cf):
	"""Merge an array of fastqfiles."""
	outfh = open(cf.get_output('output'), 'w')
	fastqfiles = get_array(cf, 'in_array')
	cf.write_log(str(fastqfiles))
	fqp = FastqParser()
	for key, fastqfile in fastqfiles:
		for rec in fqp.parse(open(fastqfile, 'U')):
			outfh.write(str(rec) + '\n')
	outfh.close()
	return constants.OK
anduril.main(fastq_merge)


