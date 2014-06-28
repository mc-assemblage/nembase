from anduril import constants
from anduril.arrayio import AndurilOutputArray, get_array
import anduril.main
import csv


def getFromArrayByKey(cf):
	"""Wrapper for the findfile_impl function."""
	commentchar = cf.get_parameter('commentchar', 'string')
	delimiter = cf.get_parameter('delimiter', 'string')
	if delimiter == 'tab':
		delimiter = '\t'
	keycol = cf.get_parameter('keycol', 'int')
	keysfile = cf.get_input('keys')
	reader = csv.reader(open(keysfile, 'U'), delimiter=delimiter, quoting=csv.QUOTE_NONE)
	#read the header
	reader.next()
	keys = []
	for row in reader:
		if not len(row) > 0 or \
			(not commentchar == "" and \
			row[0].startswith(commentchar)):
			continue
		elif keycol > len(row):
			cf.write_error("Index %s out of bounds in row %s" % (keycol, row))
			return constants.GENERIC_ERROR
		else:
			keys.append(row[keycol])
	cf.write_log(str(keys))
	inarray = get_array(cf, 'in_array')
	outarray = AndurilOutputArray(cf, 'out_array')
	for key, value in inarray:
		cf.write_log("Key: %s, Value: %s" % (key, value))
		if key in keys:
			outarray.write(key, value)
	return constants.OK
anduril.main(getFromArrayByKey)


