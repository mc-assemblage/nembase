#!/bin/bash
. ./functions.sh


ssaha2out=$( getinput "ssaha2out")
fastqfile=$( getinput "fastqfile")
outputdir=$( getoutput "mira_assembly")
tmpdir=$( getparameter "tmpdir")
threads=$( getparameter "threads")
basepath=`dirname $outputdir`


SSAHA2OPT=""
if [ -n "$ssaha2out" ] && [ -s "$ssaha2out" ]
then
	vectorin=`python -c "import os.path; print os.path.join('$basepath', 'mira_ssaha2vectorscreen_in.txt')"`
	echo "Creating soft link $vectorin to vector screen file $ssaha2out for mira to read" >> $logfile
	ln -s $ssaha2out $vectorin
	SSAHA2OPT=" -CL:msvs=yes"
fi

TMPDIROPT=""
if [ -n $tmpdir ]
then
	TMPDIROPT=" -DI:trt=$tmpdir"
fi

mira --project=mira --job=denovo,est,accurate,454 COMMON_SETTINGS -GE:not=$threads -DI:cwd=$basepath -MI:sonfs=no$TMPDIROPT 454_SETTINGS -CL:qc=no$SSAHA2OPT -FN:fqi=$fastqfile -LR:mxti=no


