from anduril import constants
from subprocess import call
import anduril.main
import os
import os.path
import subprocess
import sys
import time


def cap3(cf):
	"""Run a CAP3 assembly."""
	outputdir = cf.get_output('assemblydir')
	try:
		cf.write_log("Creating output directory %s." % outputdir)
		os.mkdir(outputdir)
	except OSError, e:
		cf.write_error(str(e))
		return constants.GENERIC_ERROR
	fastafile = cf.get_input('fastafile')
	fastaqualfile = cf.get_input('fastaqualfile')
	cf.write_log("Creating symlinks for fasta and fasta qual files.")
	ln_fastafile = os.path.join(outputdir, os.path.split(fastafile)[1])
	ln_fastaqualfile = ln_fastafile + ".qual"
	try:
		os.symlink(fastafile, ln_fastafile)
		os.symlink(fastaqualfile, ln_fastaqualfile)
	except OSError, e:
		cf.write_error(str(e))
		return constants.GENERIC_ERROR
	cf.write_log("Executing CAP3.")
	cf.write_log("cap3 %s" % ln_fastafile)
	call(["cap3", ln_fastafile])
	return constants.OK
anduril.main(cap3)
	
	
	