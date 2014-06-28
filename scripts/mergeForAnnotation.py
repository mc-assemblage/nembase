from fasta import fasta_itr, FastaRecord
from nembasedb.create_snapshot import NCBITranscriptomeRunData
from nembasedb.sraxmlparser import SRARun
from optparse import OptionParser
import cPickle as pickle
import csv
import os
import os.path
import subprocess
import sys
import zipfile


usage = "usage: %prog [options] <snapshot.pkl> <orglist.txt> <nembase_dir> <outputdir> <tmp_dir>"
parser = OptionParser(usage=usage)


def writeSeq(rec, readsetfh):
	"""Write a sequence to the output file. If the sequence is greater than 28000bp (max 
		read length in mira, split the sequence into overlapping smaller sequences."""
	if len(rec.sequence) > 28000:
		for i in range(0, len(rec.sequence), 26000):
			tmprec = FastaRecord(rec.header + "_%s" % i, rec.sequence[i:i+26500])
			readsetfh.write(str(tmprec) + "\n")
	else:
		readsetfh.write(str(rec) + "\n")


def addESTs(readsetfh, orgname, nembasedir, outlog):
	"""Add a set of ESTs to our readset."""
	estset = os.path.join(nembasedir, "est", "_outputCtgSet_%s" % orgname, "output")
	if not os.path.exists(estset):
		outlog.write("ESTs for %s not found \n" % orgname)
		return
	index = 1
	for rec in fasta_itr(estset):
		rec.header = "Contig_EST_%s" % index
		writeSeq(rec, readsetfh)
		index += 1
		
def addIllumina(readsetfh, orgname, rundata, nembasedir, outlog):
	"""Add Illumina experiments to our readset."""
	index = 1
	for exp in rundata.expsIllumina:
		trinsetsingle = os.path.join(nembasedir, "illumina", "_trinityASM_%s" % exp, \
			"assemblydir", "single", "Trinity.fasta")
		trinsetpaired = os.path.join(nembasedir, "illumina", "_trinityASM_%s" % exp, \
			"assemblydir", "paired", "Trinity.fasta")
		oasset = os.path.join(nembasedir, "illumina", "_oasesASM_%s" % exp, \
			"assemblydir", "transcripts.fa")
		if not (os.path.exists(trinsetsingle) and os.path.exists(trinsetpaired) and \
			os.path.exists(oasset)):
			print "Warning: Experiment %s not found for %s" % (exp, orgname)
			outlog.write("Warning: Experiment %s not found for %s\n" % (exp, orgname))
			continue
		elif os.stat(trinsetsingle)[6] == 0 and os.stat(trinsetpaired)[6] == 0:
			print "Trinity assembly empty, using Oases"
			for rec in fasta_itr(oasset):
				rec.header = "Contig_Illumina_%s" % index
				writeSeq(rec, readsetfh)
				index += 1
		else:
			for rec in fasta_itr(trinsetsingle):
				rec.header = "Contig_Illumina_%s" % index
				writeSeq(rec, readsetfh)
				index += 1
			for rec in fasta_itr(trinsetpaired):
				rec.header = "Contig_Illumina_%s" % index
				writeSeq(rec, readsetfh)
				index += 1
	
	
def add454(readsetfh, orgname, rundata, nembasedir, outlog):
	"""Add 454 experiments to our readset."""
	index = 1
	for exp in rundata.exps454:
		cap3contigs = os.path.join(nembasedir, "454", "_cap3Asm_%s" % exp, "assemblydir", \
			"output.cap.contigs")
		cap3singlets = os.path.join(nembasedir, "454", "_cap3Asm_%s" % exp, "assemblydir", \
			"output.cap.singlets")
		if not (os.path.exists(cap3contigs) and os.path.exists(cap3singlets)):
			print "Warning: Experiment %s not found for %s" % (exp, orgname)
			outlog.write("Warning: Experiment %s not found for %s\n" % (exp, orgname))
			continue
		for rec in fasta_itr(cap3contigs):
			rec.header = "Contig_454_%s" % index
			writeSeq(rec, readsetfh)
			index += 1
		for rec in fasta_itr(cap3singlets):
			rec.header = "Contig_454_%s" % index
			writeSeq(rec, readsetfh)
			index += 1
			
	
def runMiraEST(orgdir, tmpdir):
	"""Assemble a combined dataset using Mira EST."""
	cwd = "-DI:cwd=%s" % orgdir
	fnopt = "-FN:fai=%s" % os.path.join(orgdir, "reads.fa")
	tmpdirparam = "-DI:trt=%s" % tmpdir
	params = ['--project=mira', '--job=denovo,est,accurate,sanger', 'COMMON_SETTINGS', \
		'-GE:not=48', cwd, tmpdirparam, '-SK:mmhr=10', 'SANGER_SETTINGS', '-DP:ure=no', \
		'-CL:qc=no', fnopt, '-LR:mxti=no', '-LR:wqf=no', '-AS:epoq=no']
	print "Running MIRA assembly with params: %s" % str(params)
	subprocess.call(['mira'] + params)
	
	
def getAssembledReads(orgdir):
	"""Return a directory containing the reads that were assembled in the mira assembly."""
	contigreadsfile = os.path.join(orgdir, "mira_assembly", "mira_d_info", \
		"mira_info_contigreadlist.txt")
	csvreader = csv.reader(open(contigreadsfile), delimiter="\t", quoting=csv.QUOTE_NONE)
	asmreads = {}
	for row in csvreader:
		if not len(row) > 0:
			continue
		elif row[0].startswith("#"):
			continue
		asmreads[row[1]] = None
	return asmreads
	
	
def printMIRAContigs(orgdir):
	"""Print the assembled mira contigs to an output file."""
	outputfile = os.path.join(orgdir, "contigs.fa")
	outfh = open(outputfile, 'w')
	miraasm = os.path.join(orgdir, "mira_assembly", "mira_d_results", \
		"mira_out.unpadded.fasta")
	for rec in fasta_itr(miraasm):
		outfh.write(str(rec) + "\n")
	outfh.close()
	
	
def appendUnassembledReads(orgdir, asmreads):
	"""Append the unassembled reads to the final contig file."""
	outputfile = os.path.join(orgdir, "contigs.fa")
	outfh = open(outputfile, 'a')
	readfile = os.path.join(orgdir, "reads.fa")
	for rec in fasta_itr(readfile):
		if asmreads.has_key(rec.header):
			continue
		outfh.write(str(rec) + "\n")
	outfh.close()


def mergeForAnnotation(snapshot, orglistfile, nembasedir, outputdir, tmpdir):
	"""Merge contigs from multiple sources and generate a merged assembly."""
	reader = csv.reader(open(orglistfile), delimiter="\t", quoting=csv.QUOTE_NONE)
	outlog = open('output.log', 'w')
	for row in reader:
		if not len(row) > 0:
			continue
		elif not snapshot.has_key(row[0]):
			print "Warning: organism %s not found" % row[0]
		orgname = row[0].replace(" ", "_")
		orgdir = os.path.join(outputdir, orgname)
		try:
			if not os.path.exists(orgdir):
				print "Creating directory %s" % orgdir
				os.mkdir(orgdir)
		except:
			print "Error creating directory %s" % orgdir
			raise
		#readsetfh = open(os.path.join(orgdir, "reads.fa"), 'w')
		#if len(snapshot[row[0]].accessionsEST) > 0:
		#	addESTs(readsetfh, orgname, nembasedir, outlog)
		#if len(snapshot[row[0]].expsIllumina) > 0:
		#	addIllumina(readsetfh, orgname, snapshot[row[0]], nembasedir, outlog)
		#if len(snapshot[row[0]].exps454) > 0:
		#	add454(readsetfh, orgname, snapshot[row[0]], nembasedir, outlog)
		#readsetfh.close()
		#runMiraEST(orgdir, tmpdir)
		asmreads = getAssembledReads(orgdir)
		printMIRAContigs(orgdir)
		appendUnassembledReads(orgdir, asmreads)
	outlog.close()
		


if __name__ == "__main__":
	(options, args) = parser.parse_args()
	if len(args) < 3:
		parser.print_help()
		sys.exit(2)
	snapshot = pickle.load(open(args[0], 'rb'))
	mergeForAnnotation(snapshot, args[1], args[2], args[3], args[4])
	
	
	
