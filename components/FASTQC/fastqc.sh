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

fastqc -t $threads -o $fastqcdir -f fastq -k $kmersize $fastqfile


