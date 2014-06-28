from anduril import constants
from fasta import fasta_itr
import anduril.main
import csv
import re


def getNames(cf, is_regexp):
	"""Return a list of names to extract."""
	delimiter = cf.get_parameter('delimiter', 'string')
	if delimiter == 'tab':
		delimiter = '\t'
	reader = csv.reader(open(cf.get_input('namelist'), 'rb'), delimiter=delimiter, \
		quoting=csv.QUOTE_NONE)
	names = []
	for row in reader:
		if not len(row) > 0:
			continue
		elif is_regexp:
			regexp = None
			try:
				regexp = re.compile(row[0])
			except Exception, e:
				cf.write_log("Failed to compile regular expression %s" % row[0])
				return constants.PARAMETER_ERROR
			names.append(regexp)
		else:
			names.append(row[0])
	return names, constants.OK


def getFromFastaByName(cf):
	"""Print records where names match their header. If partial is true, check for 
		partial matches. names can also be a list of compiled regular expressions (or 
		objects that have a findall method)."""
	names, status = getNames(cf, cf.get_parameter('regexp', 'boolean'))
	if not status == constants.OK:
		return status
	fastafile = cf.get_input('fastafile')
	outputfile = open(cf.get_output('outputfile'), 'w')
	partial = cf.get_parameter('partial', 'boolean')
	negate = cf.get_parameter('negate', 'boolean')
	for rec in fasta_itr(fastafile):
		found = False
		for name in names:
			if hasattr(name, 'findall'):
				matches = name.findall(rec.header)
				if len(matches) > 0:
					found = True; break
			elif partial and rec.header.find(name) >= 0 or \
				rec.header == name:
				found = True; break
		if not negate and found or \
			negate and not found:
			outputfile.write(str(rec) + "\n")	
	outputfile.close()
	return constants.OK
anduril.main(getFromFastaByName)
	
	
