from anduril import constants
from anduril.arrayio import AndurilOutputArray
import anduril.main
import fnmatch
import os
import os.path
import stat


def findfile_impl(path, pattern):
	"""Recursively walk through path looking for files that match pattern."""
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
			if os.path.isfile(f) and \
				fnmatch.fnmatch(os.path.basename(f), pattern):
				flist.append(f)
	return flist
	
	
def findfile(cf):
	"""Wrapper for the findfile_impl function."""
	basepath = cf.get_input('basepath')
	fpattern = cf.get_parameter('fpattern')
	filesfound = AndurilOutputArray(cf, 'filesfound')
	flist = findfile_impl(basepath, fpattern)
	cf.write_log("Files: %s" % str(flist))
	for i in range(0, len(flist)):
		filesfound.write(str(i), flist[i])
	return constants.OK
anduril.main(findfile)


