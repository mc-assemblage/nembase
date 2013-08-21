from anduril.args import *
import fnmatch
import os
import os.path
import stat


def findfile(path, pattern):
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
	
	
flist = findfile(basepath, fpattern)
write_log("Files: %s" % str(flist))
for i in range(0, len(flist)):
	filesfound.write(str(i), flist[i])


