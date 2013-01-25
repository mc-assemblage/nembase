#!/bin/bash
. ./functions.sh


srafile=$( getinput "srafile")
sfffile=$( getoutput "sfffile")

sff-dump -Z $srafile > $sfffile


