#!/bin/bash
. ./functions.sh


ssaha2out=$( getinput "ssaha2out")
fastqfile=$( getinput "fastqfile")
outputdir=$( getoutput "assemblydir")
basepath=`dirname $outputdir`


if [ -n "$ssaha2out" ] && [ -s "$ssaha2out" ]
then
	echo "SSAHA2 file found" >> $logfile
else
	echo "SSAHA2 file not found" >> $logfile
fi

mira --project=asm --cwd=$basepath --job=denovo,est,accurate,454 454_SETTINGS -CL:qc=no -FN:fqi=$fastqfile


