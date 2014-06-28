from anduril import constants
from anduril.arrayio import get_array
import anduril.main
import os.path
import subprocess
import sys
import time


def runNewblerWithRetry(cf, params, tries):
	"""Run Newbler with a retry mechanism."""
	contigfile = os.path.join(cf.get_output('assemblydir'), '454AllContigs.fna')
	while True:
		tries = tries - 1
		try:
			subprocess.check_call(['runAssembly'] + params)
			if os.path.exists(contigfile):
				break
			elif tries > 0:
				cf.write_log("Error running assembly, attempts left %s" % tries)
				time.sleep(60)
			else:
				return constants.GENERIC_ERROR
		except subprocess.CalledProcessError:
			if tries > 0:
				cf.write_log("Error running assembly, attempts left %s" % tries)
				time.sleep(60)
			else:
				return constants.GENERIC_ERROR
	return constants.OK


def newbler(cf):
	"""Execute a Newbler assembly."""
	params = ['-o', cf.get_output('assemblydir')]
	vectortrimming = cf.get_input('vectortrimming')
	if vectortrimming \
		and os.path.isfile(vectortrimming) \
		and os.path.getsize(vectortrimming) > 0:
		params += ['-vt', vectortrimming]
	if cf.get_parameter('large', 'boolean'):
		params.append('-large')
	params += ['-cpu', str(cf.get_parameter('threads')), '-cdna', '-m', '-urt', '-force']
	inputfiles = get_array(cf, 'inputfiles')
	for key, inputfile in inputfiles:
		params.append(inputfile)
	cf.write_log("Params: %s" % str(params))
	tries = cf.get_parameter('retries', 'int') + 1
	return runNewblerWithRetry(cf, params, tries)
anduril.main(newbler)
	
	
	