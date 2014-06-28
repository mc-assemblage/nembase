from anduril import constants
import anduril.main
import os
import os.path
import sys


def findDataFile(fastqcdir):
	"""Find the fastqc data file in the output directory in fastqcdir."""
	datafile = None
	for f in os.listdir(fastqcdir):
		fullpath = os.path.join(fastqcdir, f)
		if os.path.isdir(fullpath) and f.endswith("_fastqc"):
			datafile = os.path.join(fullpath, "fastqc_data.txt")
			break
	return datafile
	
	
def parseSequences(datafh, percent_cutoff):
	"""Parse the sequences from a FASTQC output datafile."""
	isParsing = False; sequences = []
	while True:
		line = datafh.readline()
		if not line:
			break
		elif isParsing and line.startswith(">>END_MODULE"):
			break
		elif line.startswith(">>Overrepresented sequences"):
			isParsing = True
		elif line.startswith("#"):
			continue
		elif isParsing:
			parts = line.strip().split("\t")
			if float(parts[2]) >= percent_cutoff:
				sequences.append(parts[0])
	return sequences
	

def getOverrepKmers(cf):
	"""Parse the overrepresented sequences from a FASTQC output directory and write 
		them to a file."""
	datafh = None
	datafile = findDataFile(cf.get_input('fastqcdir'))
	if datafile and os.path.exists(datafile):
		datafh = open(datafile, 'U')
	else:
		cf.write_log("Data file %s is None or does not exist" % datafile)
		return constants.GENERIC_ERROR
	sequences = parseSequences(datafh, cf.get_parameter('percent_cutoff', 'float'))
	index = 1
	outfh = open(cf.get_output('fastafile'), 'w')
	for sequence in sequences:
		outfh.write(">K-mer %s\n%s\n" % (index, sequence))
		index += 1
	datafh.close()
	outfh.close()
	return constants.OK
anduril.main(getOverrepKmers)


