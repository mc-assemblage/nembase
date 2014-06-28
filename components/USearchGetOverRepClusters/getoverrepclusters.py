from anduril import constants
from fasta import fasta_itr
from fastq import FastqParser
import anduril.main
import csv


def getOverRepClusters(cf):
	"""Identify over represented clusters in a fastqfile and write the cluster seed 
		to a file."""
	fastqfile = cf.get_input('fastqfile')
	resultsuc = cf.get_input('resultsuc')
	resultsfa = cf.get_input('resultsfa')
	percRep = cf.get_parameter('percRep', 'float')
	output = cf.get_output('resultsfa')
	totalSeqs = 0
	fqp = FastqParser()
	for rec in fqp.parse(open(fastqfile, 'rb')):
		totalSeqs += 1
	clusterCounts = {}
	reader = csv.reader(open(resultsuc, 'rb'), quoting=csv.QUOTE_NONE, delimiter='\t')
	for row in reader:
		if row[0] == 'H':
			if not clusterCounts.has_key(row[-1]):
				clusterCounts[row[-1]] = 0
			clusterCounts[row[-1]] += 1
	outfh = open(output, 'wb')
	for rec in fasta_itr(resultsfa):
		if not clusterCounts.has_key(rec.header):
			continue
		clusterRep = (float(clusterCounts[rec.header]) / float(totalSeqs)) * 100
		if clusterRep >= percRep:
			outfh.write(str(rec) + '\n')
	outfh.close()
	return constants.OK
anduril.main(getOverRepClusters)


