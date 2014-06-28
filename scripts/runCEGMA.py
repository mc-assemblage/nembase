from optparse import OptionParser
import os
import os.path
import subprocess
import sys


usage = "usage: %prog [options] <NembaseCtgDir> <CegmaOutDir>"
parser = OptionParser(usage=usage)


def runCEGMA(indir, outdir):
	"""Run CEGMA on the NEMBASE transcriptomes in indir."""
	for d in os.listdir(indir):
		if d.startswith('.'):
			continue
		print "Running CEGMA on organism %s" % d
		contigfile = os.path.join(indir, d, 'contigs.fa')
		outputdir = os.path.join(outdir, d)
		os.makedirs(outputdir)
		subprocess.call(['cegma', '-T', '16', '-g', contigfile], cwd=outputdir)


if __name__ == "__main__":
	(options, args) = parser.parse_args()
	if len(args) < 2:
		parser.print_help()
		sys.exit(2)
	runCEGMA(args[0], args[1])
	
	
	