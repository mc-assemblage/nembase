. ./functions.sh


arrayfiles=$( getarrayfiles "array")
vectorfile=$( getinput "vectortrimming")
assemblydir=$( getoutput "assemblydir")


vsparam=""
if [ -n "$vectorfile" ] && [ -s "$vectorfile" ]
then
	vsparam=" -vt $vectorfile"
fi


runAssembly -o $assemblydir$vsparam -cdna -m -nobig $arrayfiles


