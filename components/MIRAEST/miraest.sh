#!/bin/bash
. ./functions.sh


ssaha2out=$( getinput "ssaha2out")
fastafile=$( getinput "fastafile")
fastaqualfile=$( getinput "fastaqualfile")
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

FNOPT="-FN:fai=$fastafile"
if [ -n "$fastaqualfile" ] && [ -s "$fastaqualfile" ]
then
	FNOPT=$FNOPT":fqui=$fastaqualfile"
fi

TMPDIROPT=""
if [ -n $tmpdir ]
then
	TMPDIROPT=" -DI:trt=$tmpdir"
fi

if [ -n "$fastafile" ] && [ -s "$fastafile" ]
then
	mira --project=mira --job=denovo,est,accurate,sanger COMMON_SETTINGS -GE:not=$threads -DI:cwd=$basepath -MI:sonfs=no SANGER_SETTINGS -DP:ure=no -CL:qc=no$SSAHA2OPT $FNOPT -LR:mxti=no -LR:wqf=no -AS:epoq=no
else
	mkdir $outputdir
fi

