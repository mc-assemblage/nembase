from anduril import constants
import anduril.main
import csv


def colIndexFilter(cf, row):
	"""Filter the columns based on a string containing a list of column indices."""
	collist = cf.get_parameter('collist', 'string')
	if collist == '*':
		return row
	indices = map(int, collist.split(','))
	filtered_row = map(lambda x: row[x], indices)
	return filtered_row


def csvFilter(cf):
	"""Filter a csv file based on a number of criteria."""
	inputcsv = cf.get_input('inputfile')
	outputcsv = cf.get_output('outputfile')
	delimiter = cf.get_parameter('delimiter', 'string')
	if delimiter == 'tab':
		delimiter = '\t'
	commentchar = cf.get_parameter('commentchar', 'string')
	reader = csv.reader(open(inputcsv, 'U'), delimiter=delimiter, quoting=csv.QUOTE_NONE)
	writer = csv.writer(open(outputcsv, 'wb'), delimiter=delimiter, \
		quoting=csv.QUOTE_NONE)
	for row in reader:
		if not commentchar == "" and row[0].startswith(commentchar):
			continue
		row = colIndexFilter(cf, row)
		if len(row) > 0:
			writer.writerow(row)
	return constants.OK
anduril.main(csvFilter)
	

