import csv


GENOME_ORG_DATAFILE = "/exports/projects/nembase/scripts/genome.data"
GENOME_ORG_DATALIST = []
reader = csv.reader(open(GENOME_ORG_DATAFILE, 'rb'), quoting=csv.QUOTE_NONE, \
	delimiter="\t")
for row in reader:
	GENOME_ORG_DATALIST.append(row[0].strip())


def getData(organism):
	"""Placeholder: Should return gene data when data source is available. Currently 
		returns True if organism has genome data available (but where?)."""
	if organism in GENOME_ORG_DATALIST:
		return True
	return False


