from anduril import constants
from sraxmlparser import SRAXMLParser
import anduril.main
import csv


def getRunsByExp(cf):
	"""Write the runs accessions for a given experiment to a file."""
	exp_accession = cf.get_parameter('accession', 'string')
	platform = cf.get_parameter('platform', 'string')
	srafetchxml = cf.get_input('srafetchxml')
	srarunlist = cf.get_output('srarunlist')
	sraxmlparser = SRAXMLParser()
	runs = sraxmlparser.parse(srafetchxml)
	writer = csv.writer(open(srarunlist, 'wb'), quoting=csv.QUOTE_NONE)
	writer.writerow(['NCBISRARunID'])
	index = 0
	for run in runs:
		if platform and \
			not run.platform == platform:
			continue
		elif run.exp_accession == exp_accession:
			writer.writerow([run.accession])
			index += 1
	cf.write_log("GetRunsByExp: wrote %s run accessions" % index)
	return constants.OK
anduril.main(getRunsByExp)


