. ./functions.sh


arrayfiles=$( getarrayfiles "array")
vectorfile=$( getinput "vectortrimming")
assemblydir=$( getoutput "assemblydir")
largeproject=$( getparameter "large")
cpus=$( getparameter "cpu")


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


runAssembly -o $assemblydir$vsparam$lrgparam -cpu $cpus -cdna -m -nobig $arrayfiles


