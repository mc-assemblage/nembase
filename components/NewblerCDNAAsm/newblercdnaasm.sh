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

cpuparam=""
if [ -n "$cpu" ]
then
	cpuparam=" -cpu $cpu "
fi

runAssembly -o $assemblydir$vsparam$lrgparam$cpuparam -cdna -m -nobig $arrayfiles


