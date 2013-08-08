. ./functions.sh


arrayfiles=$( getarrayfiles "array")
vectorfile=$( getinput "vectortrimming")
assemblydir=$( getoutput "assemblydir")
largeproject=$( getparameter "large")
threads=$( getparameter "threads")


vsparam=""
if [ -n "$vectorfile" ] && [ -s "$vectorfile" ]
then
	vsparam=" -vt $vectorfile "
fi

lrgparam=""
if [ $largeproject = "true" ]
then
	lrgparam=" -large "
fi


runAssembly -o $assemblydir$vsparam$lrgparam -cpu $threads -cdna -m -nobig $arrayfiles


