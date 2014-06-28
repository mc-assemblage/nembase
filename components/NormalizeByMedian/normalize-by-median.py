#
# This file contains code adapted from the normalize-by-median.py script, part of the 
# Khmer package.
# http://khmer.readthedocs.org/en/latest/introduction.html
#

from anduril import constants
from itertools import izip
import anduril.main
import khmer
import screed


def batchwise(t, size):
	it = iter(t)
	return izip(*[it]*size)


def validpair(r0, r1):
	return r0.name[-1] == "1" and \
		r1.name[-1] == "2" and \
		r0.name[0:-1] == r1.name[0:-1]
		

def normalizeByMedian_impl(cf, infp, outfp, kmersize, minhashsize, nhashes, cutoff):
	"""Digitally normalize the coverage of a set of input reads."""		
	batch_size = 1

	cf.write_log("making hashtable %s %s %s" % (kmersize, minhashsize, nhashes))
	ht = khmer.new_counting_hash(kmersize, minhashsize, nhashes)
	cf.write_log('done')

	total = 0
	discarded = 0

	n = -1
	for n, batch in enumerate(batchwise(infp, batch_size)):
		if n > 0 and n % 100000 == 0:
			cf.write_log("...kept %s of %s, or %s%%" % (total - discarded, total, \
				int(100. - discarded / float(total) * 100.)))
	
		total += batch_size

		# Emit the batch of reads if any read passes the filter
		# and all reads are longer than K
		passed_filter = False
		passed_length = True
		for record in batch:
			if len(record.sequence) < kmersize:
				passed_length = False
				continue

			seq = record.sequence.replace('N', 'A')
			med, _, _ = ht.get_median_count(seq)
	
			if med < cutoff:
				ht.consume(seq)
				passed_filter = True
			
		# Emit records if any passed
		if passed_length and passed_filter:
			for record in batch:
				if hasattr(record,'accuracy'):
					outfp.write('@%s\n%s\n+\n%s\n' % (record.name, 
													  record.sequence, 
													  record.accuracy))
				else:
					outfp.write('>%s\n%s\n' % (record.name, record.sequence))
		else:
			discarded += batch_size
	return discarded, total, ht, n
			
			
def normalizeByMedian(cf):
	"""Wrapper for the normalizeByMedian_impl function."""
	kmersize = cf.get_parameter('kmersize', 'int')
	minhashsize = cf.get_parameter('minhashsize', 'float')
	nhashes = cf.get_parameter('nhashes', 'int')
	cutoff = cf.get_parameter('cutoff', 'int')
	
	inputfile = cf.get_input('inputfile')
	outputfile = cf.get_output('outputfile')
	infp = screed.open(inputfile)
	outfp = open(outputfile, 'w')
	
	discarded, total, ht, n = normalizeByMedian_impl(cf, infp, outfp, kmersize, \
		minhashsize, nhashes, cutoff)
		
	outfp.close()
	infp.close()

	if -1 < n:
		percent_kept = int(100. - discarded / float(total) * 100.)
		cf.write_log("DONE with %s; kept %s of %s or %s%%" % (inputfile, \
			total - discarded, total, percent_kept))
		cf.write_log("Output in %s" % outputfile)

	# Change 0.2 only if you really grok it.  HINT: You don't.
	fp_rate = khmer.calc_expected_collisions(ht)
	cf.write_log("fp rate estimated to be %1.3f" % fp_rate)

	if fp_rate > 0.20:
		cf.write_error("ERROR: the counting hash is too small.")
		cf.write_error("Increase the hashsize/num ht.")
		return constants.GENERIC_ERROR
	return constants.OK
anduril.main(normalizeByMedian)


