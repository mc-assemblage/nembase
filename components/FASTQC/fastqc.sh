#!/bin/bash
. ./functions.sh


kmersize=$( getparameter "kmersize")
threads=$( getparameter "threads")
fastqfile=$( getinput "fastqfile")
fastqcdir=$( getoutput "fastqcdir")


if [ ! -d $fastqcdir ]
then
	mkdir $fastqcdir
fi

threadopt=""
if [ -n "threads" ]
then
	threadopt=" -t $threads "
fi

fastqc$threadopt -o $fastqcdir -f fastq -k $kmersize $fastqfile


