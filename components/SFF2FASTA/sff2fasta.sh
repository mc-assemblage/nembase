#!/bin/bash
. ./functions.sh


sfffile=$( getinput "sfffile")
fastafile=$( getoutput "fastafile")
fastaqualfile=$( getoutput "fastaqualfile")


sffinfo -s $sfffile > $fastafile
sffinfo -q $sfffile > $fastaqualfile


