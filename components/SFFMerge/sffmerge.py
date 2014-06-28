from anduril import constants
from anduril.arrayio import get_array
import anduril.main
import subprocess


def sffmerge(cf):
	inarray = get_array(cf, 'in_array')
	outputfile = cf.get_output('output')
	params = ['-o', outputfile]
	for key, inputfile in inarray:
		params.append(inputfile)
	try:
		subprocess.check_call(['sfffile'] + params)
	except subprocess.CalledProcessError, e:
		cf.write_log("Error running sfffile.")
		cf.write_log("Error: %s" % str(e))
		return constants.GENERIC_ERROR
	return constants.OK
anduril.main(sffmerge)


