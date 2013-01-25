#!/bin/bash
. ./functions.sh


fastafile=$( getinput "fastafile")
fastaqualfile=$( getinput "fastaqualfile")
fastqfile=$( getoutput "fastqfile")


fasta2fastq $fastafile $fastaqualfile > $fastqfile


