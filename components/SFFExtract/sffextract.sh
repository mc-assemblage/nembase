#!/bin/bash
. ./functions.sh


sfffile=$( getinput "sfffile")
namelist=$( getinput "namelist")
output=$( getoutput "output")


sfffile -o $output -i $namelist $sfffile


