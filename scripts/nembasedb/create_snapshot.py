from optparse import OptionParser
import cPickle as pickle
import csv
import genomedata
import ncbi
import sys


usage = "usage: %prog [options] <Organisms.txt> <snapshot.pkl>"
parser = OptionParser(usage=usage)


class NCBITranscriptomeRunData:
	"""Stores details on data available from NCBI for an organism."""
	def __init__(self, genomeData, accessionsEST, exps454, expsIllumina):
		self.genomeData = genomeData
		self.accessionsEST = accessionsEST
		self.exps454 = exps454
		self.expsIllumina = expsIllumina
		
		
def createSnapshot(organisms):
	"""Return a dictionary of NCBIData objects with the organism as key containing 
		references to all data transcriptomic data available for that organism at a 
		particular time."""
	snapshot = {}
	for organism in organisms:
		print "Creating snapshot of organism %s" % organism
		exps454 = {}
		runs454 = ncbi.getSRARuns(organism, '454')
		for run in runs454:
			if not exps454.has_key(run.exp_accession):
				exps454[run.exp_accession] = []
			exps454[run.exp_accession].append(run)
		expsIllumina = {}
		runsIllumina = ncbi.getSRARuns(organism, 'Illumina')
		for run in runsIllumina:
			if not expsIllumina.has_key(run.exp_accession):
				expsIllumina[run.exp_accession] = []
			expsIllumina[run.exp_accession].append(run)
		genomeData = genomedata.getData(organism)
		accessionsEST = ncbi.getESTAccessions(organism)
		snapshot[organism] = NCBITranscriptomeRunData(genomeData, accessionsEST, exps454, \
			expsIllumina)
	return snapshot


if __name__ == "__main__":
	(options, args) = parser.parse_args()
	if len(args) < 2:
		parser.print_help()
		sys.exit(2)
	reader = csv.reader(open(args[0], 'rb'))
	reader.next()
	organisms = []
	for row in reader:
		if len(row) > 0:
			organisms.append(row[0])
	snapshot = createSnapshot(organisms)
	outfh = open(args[1], 'wb')
	pickle.dump(snapshot, outfh)
	outfh.close()


