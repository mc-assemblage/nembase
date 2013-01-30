from anduril.args import *
from itertools import izip
import khmer
import screed


def batchwise(t, size):
	it = iter(t)
	return izip(*[it]*size)
	
def validpair(r0, r1):
	return r0.name[-1] == "1" and \
		r1.name[-1] == "2" and \
		r0.name[0:-1] == r1.name[0:-1]
		
		
batch_size = 1
#if is_paired:
#	batch_size = 2

write_log("making hashtable %s %s %s" % (kmersize, minhashsize, nhashes))
ht = khmer.new_counting_hash(kmersize, minhashsize, nhashes)
write_log('done')

total = 0
discarded = 0

outfp = open(outputfile, 'w')

n = -1
for n, batch in enumerate(batchwise(screed.open(inputfile), batch_size)):
	if n > 0 and n % 100000 == 0:
		write_log("...kept %s of %s, or %s%%" % (total - discarded, total, \
			int(100. - discarded / float(total) * 100.)))

	total += batch_size

	#if args.paired:
	#	if not validpair(batch[0], batch[1]):
	#		print >>sys.stderr, 'Error: Improperly interleaved pairs %s %s' % (batch[0].name, batch[1].name)
	#		sys.exit(-1)

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

if -1 < n:
	write_log("DONE with %s; kept %s of %s or %s%%" % (inputfile, total - discarded, \
		total, int(100. - discarded / float(total) * 100.)))
	write_log("Output in %s" % outputfile)

# Change 0.2 only if you really grok it.  HINT: You don't.
fp_rate = khmer.calc_expected_collisions(ht)
write_log("fp rate estimated to be %1.3f" % fp_rate)

if fp_rate > 0.20:
	write_error("ERROR: the counting hash is too small.")
	write_error("Increase the hashsize/num ht.")


