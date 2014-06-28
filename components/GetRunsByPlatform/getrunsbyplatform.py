from anduril import constants
from sraxmlparser import SRAXMLParser
import anduril.main
import csv


def getRunsByPlatform(cf):
	"""Write the run accessions from a particular platform to a file."""
	platform = cf.get_parameter('platform', 'string')
	if not platform in ['454', 'Illumina']:
		cf.write_error("Unknown sequencing platform %s" % platform)
		return constants.GENERIC_ERROR
	srafetchxml = cf.get_input('srafetchxml')
	srarunlist = cf.get_output('srarunlist')
	sraxmlparser = SRAXMLParser()
	runs = sraxmlparser.parse(srafetchxml)
	writer = csv.writer(open(srarunlist, 'wb'), quoting=csv.QUOTE_NONE)
	writer.writerow(['NCBISRARunID'])
	num_accessions = 0
	for run in runs:
		if run.platform == platform:
			writer.writerow([run.accession])
			num_accessions += 1
	cf.write_log("GetRunsByPlatform: wrote %s run accessions" % num_accessions)
	return constants.OK
anduril.main(getRunsByPlatform)


