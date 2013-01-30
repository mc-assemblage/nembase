. ./functions.sh


arrayfiles=$( getarrayfiles "array")
vectorfile=$( getinput "vectortrimming")
assemblydir=$( getoutput "assemblydir")


vsparam=""
if [ -n "$vectorfile" ]
then
	vsparam=" -vt $vectorfile"
fi


runAssembly -o $assemblydir$vsparam -cdna -m -nobig $arrayfiles


