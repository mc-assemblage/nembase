from anduril import constants
from anduril.arrayio import get_array
from fasta import fasta_itr
import anduril.main


def fasta_merge(cf):
	"""Merge an array of fastafiles."""
	outfh = open(cf.get_output('output'), 'w')
	fastafiles = get_array(cf, 'fastafiles')
	cf.write_log(str(fastafiles))
	for key, fastafile in fastafiles:
		for rec in fasta_itr(fastafile):
			outfh.write(str(rec) + "\n")
	outfh.close()
	return constants.OK
anduril.main(fasta_merge)


