from anduril.args import *
import subprocess
import sys
import time


def runCommand(cmd, args, cwd=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
	"""Execute a command and return its output."""
	args = (cmd,) + tuple(args)
	popen = subprocess.Popen(args, stdout=stdout, stderr=stderr, cwd=cwd)
	while True:
		chunk = popen.stdout.read(8)
		if not chunk:
			break
		sys.stdout.write(chunk)
		sys.stdout.flush()
	for line in popen.stderr.readlines():
		sys.stderr.write(line)
	return popen.poll()

params = ["-o", assemblydir]

if vectortrimming:
	fh = open(vectortrimming)
	line = fh.readline()
	if line and line.startswith(">"):
		params += ["-vt", vectortrimming]
	fh.close()
	
if large:
	params.append("-large")
params += ["-cpu", str(threads), "-cdna", "-m", "-nobig", "-urt"]


for key, inputfile in array.items():
	params.append(inputfile)

tries = retries + 1

while True:
	tries = tries - 1
	exitcode = runCommand("runAssembly", params)
	if exitcode > 0 and tries > 0:
		print "Error running assembly, attempts left %s" % (tries)
		if not "-force" in params:
			params.append("-force")
		time.sleep(2)
		continue
	else:
		break
	
	
	