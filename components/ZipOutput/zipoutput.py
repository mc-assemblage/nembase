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
				

def zipoutput(inputfiles, archive, rootname, include_list, append_index):
	zfile = zipfile.ZipFile(archive, mode="w")
	index = 1
	for path in inputfiles.itervalues():
		write_log("Path: %s" % path)
		if path.endswith("/"):
			path = path[:-1]
		filelist = getFileList(path, include_list)
		write_log("Filelist: %s" % filelist)
		for f in filelist:
			index_str = ""
			if append_index:
				index_str = str(index)
			nfname = os.path.join(rootname, os.path.basename(path) + index_str, \
				f[len(path)+1:])
			zfile.write(f, nfname, zipfile.ZIP_DEFLATED)
		index += 1
	zfile.close()
	
	
include_list = []
if fn_include:
	reader = csv.reader(open(fn_include, 'rb'))
	for row in reader:
		if len(row) > 0:
			include_list.append(row[0])
	write_log("Include list: %s" % include_list)
zipoutput(array, archive, pkgname, include_list, append_index)
				
				
