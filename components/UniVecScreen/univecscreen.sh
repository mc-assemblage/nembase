#!/bin/bash
. ./functions.sh


fastafile=$( getinput "fastafile")
ssaha2out=$( getoutput "ssaha2out")
mode=$( getparameter "rtype")


echo $fastafile >> $logfile


ssaha2 -output ssaha2 -rtype $mode $fastafile UniVec > $ssaha2out


