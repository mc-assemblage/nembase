from fasta import fasta_itr
from optparse import OptionParser
import os
import os.path
import sys


usage = "usage: %prog [options] <in_dir> <out_dir>"
parser = OptionParser(usage=usage)


def getSpeciesCode(org):
	"""Return a six letter species code for the organism."""
	if org.startswith("Caenorhabditis_sp"):
		org = org.replace("sp", "").strip()
	genus, species = org.split("_")
	code = genus[:3] + species[:3]
	if len(code) < 6:
		code += (6 - len(code)) * "X"
	return code.upper()


def renameContigs(indir, outdir):
	"""Rename the contigs in indir and write them to outdir."""
	for d in os.listdir(indir):
		code = getSpeciesCode(d)
		os.mkdir(os.path.join(outdir, d))
		infile = os.path.join(indir, d, "contigs.fa")
		outfile = os.path.join(outdir, d, "contigs.fa")
		outfh = open(outfile, 'w')
		index = 1
		for rec in fasta_itr(infile):
			rec.header = code + "_" + str(index)
			index += 1
			outfh.write(str(rec) + "\n")
		outfh.close()


if __name__ == "__main__":
	(options, args) = parser.parse_args()
	if len(args) < 2:
		parser.print_help()
		sys.exit(2)
	renameContigs(args[0], args[1])
	
	
	