from anduril.args import *
import os.path


datafile = os.path.join(fastqcdir, "fastqfile_fastqc", "fastqc_data.txt")
datafh = open(datafile)
outfh = open(fastafile, 'w')
isParsing = False
overrepSeq = []; index = 1
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
outfh.close()
datafh.close()


