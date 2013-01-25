#!/bin/bash
. ./functions.sh


arrayfiles=$( getarrayfiles "array")
output=$( getoutput "output")


sfffile -o $output $arrayfiles


