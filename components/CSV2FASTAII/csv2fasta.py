from anduril import constants
import anduril.main
import csv


def csv2Fasta(cf):
	"""Convert a CSV file to a Fasta file."""
	csvfile = cf.get_input('csvfile')
	fastafile = cf.get_output('fastafile')
	delimiter = cf.get_parameter('delimiter', 'string')
	if delimiter == "tab":
		delimiter = '\t'
	quotechar = cf.get_parameter('quotechar', 'string')
	header_col = cf.get_parameter('headercol', 'int')
	sequence_col = cf.get_parameter('sequencecol', 'int')
	
	cf.write_log("csvfile: %s, fastafile: %s" % (csvfile, fastafile))
	cf.write_log("delimiter: '%s', quotechar: '%s', headercol: %s, sequencecol: %s" % (\
		delimiter, quotechar, header_col, sequence_col))
	
	reader = csv.reader(open(csvfile, 'U'), delimiter=delimiter, quotechar=quotechar)
	outfh = open(fastafile, 'w')
	for row in reader:
		header = row[header_col]
		sequence = row[sequence_col]
		outfh.write(">%s\n%s\n" % (header, sequence))
	outfh.close()
	return constants.OK
anduril.main(csv2Fasta)
	
	
