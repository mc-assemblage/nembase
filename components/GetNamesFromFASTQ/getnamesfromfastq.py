from anduril import constants
from fastq import FastqParser
import anduril.main


def getNamesFromFastQ(cf):
	"""Write the headers of a fastqfile to an outputfile."""
	outfh = open(cf.get_output('namelist'), 'w')
	fqp = FastqParser()
	for rec in fqp.parse(open(cf.get_input('fastqfile'), 'U')):
		outfh.write("%s\n" % rec.header)
	outfh.close()
	return constants.OK
anduril.main(getNamesFromFastQ)


