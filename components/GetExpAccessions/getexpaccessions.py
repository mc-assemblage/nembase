from anduril import constants
from sraxmlparser import SRAXMLParser
import anduril.main
import csv


def getExpAccessions(cf):
	"""Write the experiment accessions to a file."""
	platform = cf.get_parameter('platform')
	srafetchxml = cf.get_input('srafetchxml')
	sraexplist = cf.get_output('sraexplist')
	sraxmlparser = SRAXMLParser()
	runs = sraxmlparser.parse(srafetchxml)
	writer = csv.writer(open(sraexplist, 'wb'), quoting=csv.QUOTE_NONE)
	writer.writerow(['NCBISRAExpID'])
	accessions = []
	for run in runs:
		if platform and \
			not run.platform == platform:
			continue
		elif not run.exp_accession in accessions:
			writer.writerow([run.exp_accession])
			accessions.append(run.exp_accession)
	cf.write_log("GetExpAccessions: wrote %s experiment accessions" % len(accessions))
	return constants.OK
anduril.main(getExpAccessions)


