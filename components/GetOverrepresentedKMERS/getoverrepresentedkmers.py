from anduril.args import *
import os
import os.path
import sys


#Find the fastqc output directory in fastqcdir
datafile = None
for f in os.listdir(fastqcdir):
	fullpath = os.path.join(fastqcdir, f)
	if os.path.isdir(fullpath) and f.endswith("_fastqc"):
		datafile = os.path.join(fullpath, "fastqc_data.txt")
		break

datafh = None
if datafile and os.path.exists(datafile):
	datafh = open(datafile)
else:
	write_log("Data file %s is None or does not exist" % datafile)
	sys.exit(2)
	
outfh = open(fastafile, 'w')
isParsing = False; index = 1
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
			outfh.write(">K-mer %s\n%s\n" % (index, parts[0]))
			index += 1
outfh.close()
datafh.close()


