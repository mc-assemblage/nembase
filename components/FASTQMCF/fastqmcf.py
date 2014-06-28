from anduril import constants
from subprocess import call
import anduril.main
import os
import os.path
import subprocess
import sys
import time


def isNonZeroFile(fpath):
	"""Return true if file fpath exists and is non empty."""
	return True if os.path.isfile(fpath) and \
		os.path.getsize(fpath) > 0 else False


def fastqmcf(cf):
	"""Filter and trim adapter sequences from a fastafile."""
	inputleft = cf.get_input('left')
	inputright = cf.get_input('right')
	inputsingle = cf.get_input('single')
	adapters = cf.get_input('adapters')
	outputleft = cf.get_output('outputleft')
	outputright = cf.get_output('outputright')
	outputsingle = cf.get_output('outputsingle')
	rmduplen = cf.get_parameter('rmDupLength', 'int')
	args = []
	if rmduplen > 0:
		args = ["-D", str(rmduplen)]
	#check if there are paired-end reads
	if isNonZeroFile(inputleft) and isNonZeroFile(inputright):
		cf.write_log("Processing paired-end reads")
		args += ["-o", outputleft, "-o", outputright, adapters, inputleft, inputright]
		call(["fastq-mcf"] + args)
	else:
		#create empty output files
		open(outputleft, 'a').close()
		open(outputright, 'a').close()
	#check if there are single reads
	if isNonZeroFile(inputsingle):
		cf.write_log("Processing single reads")
		args += ["-o", outputsingle, adapters, inputsingle]
		call(["fastq-mcf"] + args)
	else:
		open(outputsingle, 'a').close()
	return constants.OK
anduril.main(fastqmcf)
	
	
	