from anduril import constants
from subprocess import call
import anduril.main
import os
import os.path
import subprocess


def getKFromTrinity(assemblydir):
	"""Get the kmer size from a trinity assembly."""
	kmersize = None
	#try to find the single end assembly first
	sdir = os.path.join(assemblydir, 'single')
	for f in os.listdir(sdir):
		if f.startswith('inchworm.K'):
			kmersize = int(f.split('.')[1][1:])
			return kmersize
	pdir = os.path.join(assemblydir, 'paired')
	for f in os.listdir(pdir):
		if f.startswith('inchworm.K'):
			kmersize = int(f.split('.')[1][1:])
			return kmersize
	return None


def oases(cf):
	"""Perform a transcriptome assembly of an RNA-Seq fastqfile."""
	fastqfile = cf.get_input('fastqfile')
	outputdir = cf.get_output('assemblydir')
	kmersize = cf.get_parameter('kmersize', 'int')
	if cf.get_input('trinitykmersize'):
		trinitydir = cf.get_input('trinitykmersize')
		kmersize = getKFromTrinity(trinitydir)
		if not kmersize:
			cf.write_error("Could not determine kmersize from Trinity directory %s" % \
				trinitydir)
			return constants.INVALID_INPUT
	cf.write_log('Running velveth...')
	call(['velveth', outputdir, str(kmersize), '-fastq', '-short', fastqfile])
	cf.write_log('Running velvetg...')
	call(['velvetg', outputdir, '-read_trkg', 'yes'])
	cf.write_log('Running oases...')
	call(['oases', outputdir])
	return constants.OK
anduril.main(oases)
	
	
	