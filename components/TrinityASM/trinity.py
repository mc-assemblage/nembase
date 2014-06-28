from anduril import constants
from subprocess import call
import anduril.main
import os
import os.path
import subprocess
import sys
import time


TRINITY_PATH = "/home/mclarke2/software/trinityrnaseq_r20131110/Trinity.pl"
MAX_COUNT_READS = 100000


def isNonZeroFile(fpath):
	"""Return true if file fpath exists and is non empty."""
	return True if os.path.isfile(fpath) and \
		os.path.getsize(fpath) > 0 else False


def trinity(cf):
	"""Perform a transcriptome assembly of an RNA-Seq fastqfile."""
	inputleft = cf.get_input('inputleft')
	inputright = cf.get_input('inputright')
	inputsingle = cf.get_input('inputsingle')
	outputdir = cf.get_output('assemblydir')
	outputp = os.path.join(outputdir, "paired")
	outputs = os.path.join(outputdir, "single")
	numcpu = str(cf.get_parameter('CPU', 'int'))
	jellymem = cf.get_parameter('jellymem', 'string')
	base_args = ["--seqType", "fq", "--JM", jellymem, "--CPU", numcpu]
	if isNonZeroFile(inputleft) and isNonZeroFile(inputright):
		cf.write_log("Running paired-end assembly")
		args = base_args + ["--left", inputleft, "--right", inputright, "--output", \
			outputp]
		cf.write_log("Args: " + str(args))
		call([TRINITY_PATH] + args)
	elif isNonZeroFile(inputsingle):
		cf.write_log("Running single assembly")
		args = base_args + ["--single", inputsingle, "--output", outputs]
		cf.write_log("Args: " + str(args))
		call([TRINITY_PATH] + args)
	if not os.path.exists(outputp):
		os.makedirs(outputp)
	if not os.path.exists(outputs):
		os.makedirs(outputs)
	if not os.path.exists(os.path.join(outputp, "Trinity.fasta")):
		open(os.path.join(outputp, "Trinity.fasta"), 'a').close()
	if not os.path.exists(os.path.join(outputs, "Trinity.fasta")):
		open(os.path.join(outputs, "Trinity.fasta"), 'a').close()
	return constants.OK
anduril.main(trinity)
	
	
	