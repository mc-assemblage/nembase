from anduril.args import *
from xml.etree import ElementTree
import csv


if not platform in ["454", "Illumina"]:
	write_error("Unknown sequencing platform %s" % platform)
	

accessions = []
root = ElementTree.parse(srafetchxml)
for exp_package in root.findall("EXPERIMENT_PACKAGE"):
	if platform == '454' and \
		len(exp_package.findall("EXPERIMENT/PLATFORM/LS454")) > 0:
		runs = exp_package.findall("RUN_SET/RUN")
		accessions += map(lambda x: x.get("accession"), runs)
	elif platform == 'Illumina' and \
		len(exp_package.findall("EXPERIMENT/PLATFORM/ILLUMINA")) > 0:
		runs = exp_package.findall("RUN_SET/RUN")
		accessions += map(lambda x: x.get("accession"), runs)
writer = csv.writer(open(srarunlist, 'wb'), quoting=csv.QUOTE_NONE)
writer.writerow(["NCBISRARunID"])
for accession in accessions:
	writer.writerow([accession])
write_log("GetRunsByPlatform: wrote %s run accessions" % len(accessions))


