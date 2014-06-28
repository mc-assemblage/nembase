from nembasedb.create_snapshot import NCBITranscriptomeRunData
from nembasedb.sraxmlparser import SRARun
from optparse import OptionParser
import cPickle as pickle
import os
import os.path
import sys
import zipfile


usage = "usage: %prog [options] <snapshot.pkl> <nembase_dir> <outputdir>"
parser = OptionParser(usage=usage)


def getOrganismListByPlatforms(platformstr, snapshot):
	"""Return a list of organisms that have data in each of the platforms in 
		platformstr."""
	platformlist = platformstr.split(',')
	if platformstr == "No Data":
		platformlist = []
	platformlist.sort()
	orglist = []
	for org in snapshot.keys():
		if platformstr == 'Genome' and \
			snapshot[org].genomeData:
			orglist.append(org)
			continue
		elif snapshot[org].genomeData:
			continue
		tmp_platforms = []
		if len(snapshot[org].accessionsEST) > 0:
			tmp_platforms.append('ESTs')
		if len(snapshot[org].expsIllumina) > 0:
			tmp_platforms.append('Illumina')
		if len(snapshot[org].exps454) > 0:
			tmp_platforms.append('454')
		tmp_platforms.sort()
		if tmp_platforms == platformlist:
			orglist.append(org)
	return orglist
	
	
def extractFileToDir(archive, f, ofilename):
	"""Extract a file with name f to ofilename."""
	zfile = zipfile.ZipFile(archive)
	for name in zfile.namelist():
  		(dirname, filename) = os.path.split(name)
  		if filename == f:
  			fn = open(ofilename, 'w')
  			fn.write(zfile.read(name))
  			fn.close()


def prepareESTsOnly(nembasedir, baseoutputdir):
	"""Prepare EST datasets for annotation."""
	filteredList = getOrganismListByPlatforms('ESTs', snapshot)
	for org in filteredList:
		orgname = org.replace(" ", "_")
		estarchive = os.path.join(nembasedir, "est", "_zipCtgSetEST_%s" % orgname, "archive")
		outputdir = os.path.join(baseoutputdir, orgname)
		if not os.path.isdir(outputdir):
			try:
				os.mkdir(outputdir)
			except:
				print "Error creating directory %s" % outputdir
				raise
		if not os.path.exists(estarchive):
			print "Warning: zip archive %s does not exist" % estarchive
			continue
		outputfile = os.path.join(outputdir, "contigs.fa")
		if os.path.exists(outputfile):
			continue
		extractFileToDir(estarchive, "output", outputfile)
		


def prepareForAnnotation(snapshot, nembasedir, baseoutputdir):
	"""Prepare the EST, 454 and Illumina data for annotation."""
	prepareESTsOnly(nembasedir, baseoutputdir)


if __name__ == "__main__":
	(options, args) = parser.parse_args()
	if len(args) < 3:
		parser.print_help()
		sys.exit(2)
	snapshot = pickle.load(open(args[0], 'rb'))
	prepareForAnnotation(snapshot, args[1], args[2])


