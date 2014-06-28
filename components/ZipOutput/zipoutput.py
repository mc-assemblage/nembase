from anduril.args import *
from cStringIO import StringIO
import csv
import fnmatch
import os
import os.path
import stat
import sys
import zipfile
	
	
def isIncluded(f, include_list):
	"""Return True if filename f matches a pattern in include_list."""
	if not include_list:
		return True
	for pattern in include_list:
		if fnmatch.fnmatch(os.path.basename(f), pattern):
			return True
	return False


def getFileList(path, include_list=[]):
	"""Recursively walk through a directory structure beginning at path and return the 
		list of files encountered. If include_list is given, only filenames included 
		in the list (unix file patterns are supported) will be in the returned."""
	def walktree(top=".", depthfirst=True):
		names = os.listdir(top)
		if not depthfirst:
			yield top, names
		for name in names:
			try:
				st = os.lstat(os.path.join(top, name))
			except os.error:
				continue
			if stat.S_ISDIR(st.st_mode):
				for (newtop, children) in walktree(
					os.path.join(top, name), depthfirst):
					yield newtop, children
		if depthfirst:
			yield top, names
	
	flist = []
	for (basepath, children) in walktree(path, False):
		for child in children:
			f = os.path.join(basepath, child)
			if os.path.isfile(f):
				if isIncluded(f, include_list):
					flist.append(f)
	return flist
	
	
def getArchiveName(path, depth):
	"""Remove the first depth number of path elements from path."""
	elements = []
	while True:
		if path == os.path.sep:
			break
		elements.insert(0, os.path.split(path)[1])
		path = os.path.split(path)[0]
	return os.path.sep.join(elements[depth:])
				

def zipoutput(inputfiles, archive, include_list=[], rmPathDepth=0):
	"""Add an array of files and directories to a zip file. archive is the name (and path)
		of the zip file to be created, include_list (if given) is a list of filenames 
		(unix file patterns are supported) that should only be included in the zip file. 
		By default, the full path structure of each file added to the zip file is 
		preserved. rmPathDepth removes n path elements from the beginning of each file 
		path."""
	zfile = zipfile.ZipFile(archive, mode='w', allowZip64=True)
	for path in inputfiles.itervalues():
		write_log("Path: %s" % path)
		if path.endswith("/"):
			path = path[:-1]
		if os.path.isfile(path):
			nfname = getArchiveName(path, rmPathDepth)
			zfile.write(path, nfname)
		else:
			filelist = getFileList(path, include_list)
			write_log("Filelist: %s" % filelist)
			for f in filelist:
				nfname = getArchiveName(f, rmPathDepth)
				write_log("File: %s" % f)
				write_log("ArcName: %s" % nfname)
				zfile.write(f, nfname)
	zfile.close()
	
	
include_list = []
if fn_include:
	reader = csv.reader(open(fn_include, 'U'))
	for row in reader:
		if len(row) > 0:
			include_list.append(row[0])
	write_log("Include list: %s" % include_list)
zipoutput(array, archive, include_list, rmPathDepth)
				
				
