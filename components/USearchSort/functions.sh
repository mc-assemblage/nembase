# Magic separator for log files
slsep='--- SEP h43dsznbF2idt2xH ---';
# Write to log:  echo "Hello World!" >> "$logfile"
logfile=$( grep ^output._log= "$1" | sed s,^output._log=,, )
# Write to error log:  echo "Error!" >> "$errorfile"
errorfile=$( grep ^output._errors= "$1" | sed s,^output._errors=,, )
# save the command file location for internal use
commandfile="$1"

function getparameter {
# Reads parameter from the _command file.
# Usage: var=$( getparameter "parameter_name" )

    param=$( grep ^parameter."$1"= "$commandfile" | sed s,^parameter."$1"=,, | \
    sed -e 's,\\#,#,g' -e 's,\\!,!,g' -e 's,\\:,:,g' -e 's,\\=,=,g' -e 's,^\\ , ,g' )
    echo "$param"
}

function getinput {
# Reads input port from the _command file.
# Usage: var=$( getinput input_name )

    grep ^input."$1"= "$commandfile" | sed s,^input."$1"=,, 
}

function getoutput {
# Reads output port from the _command file.
# Usage: var=$( getoutput output_name )

    grep ^output."$1"= "$commandfile" | sed s,^output."$1"=,, 
}

function getmetadata {
# Reads metadata from the _command file.
# Usage: var=$( getmetadata "metadata_name" )

    grep ^metadata."$1"= "$commandfile" | sed s,^metadata."$1"=,,
}

function gettempdir {
# Create and get the temporary dir path:  
# Usage: tmpdir=$( gettempdir )

    tempdir=$( grep ^output._tempdir= "$commandfile" | sed s,^output._tempdir=,, )
    mkdir -p "$tempdir" 
    echo $tempdir
}

function writelog {
# Writes a string in the log file, and on the stdOut

    echo "$1" 
    echo "$1" >> "$logfile"
}

function writeerror {
# Writes a string in the error file, and on the stdErr

    echo "$1" >&2
    echo "$1" >> "$errorfile"
    echo $slsep >> "$errorfile"
}

function csvcoln {
# Gets a column number from a csv file header
# If column not found, echos 0
# Usage: coln=$( csvcoln path/to/file.csv "ColName" )
# (to extract that column: cut -f $coln path/to/file.csv)

    c=1
    IFS=$'\t'
    for col in $( head -n 1 "$1" | tr -d '\n\r' )
    do if (( $( echo ${col//\"/} | grep -c ^${2}$ ) ))
       then echo $c
            return 0
       fi
       c=$(( $c + 1 ))
    done
    echo 0
    echo "Column $2 not found" 1>&2
    return 1
}
function getarraykeys {
# Gets a list of array keys
# Usage: keys=( $( getarraykeys inputportname ) )

    portpath=$( getinput "$1" )
    portindex=$( getinput "_index_"${1} )
    if [ ! -f "$portindex" ]
    then echo "No array index found in \"$portindex\"" 1>&2
        return 1
    fi
    keyc=$( csvcoln "$portindex" Key )
    if (( $? ))
    then echo "No Key column found" 1>&2
         return 1
    fi
    cut -f $keyc "$portindex" | tail -n +2 | sed -e 's,\r,,' -e 's,^",,' -e 's,"$,,'  
    return 0
}
function getarraykeyindex {
# Gets an index number for a specific key
# Usage: index=( $( getarraykeyindex inputportname key ) )

    portindex=$( getinput "_index_"${1} )
    if [ ! -f "$portindex" ]
    then echo "No array index found in \"$portindex\"" 1>&2
        return 1
    fi
    keyc=$( csvcoln "$portindex" Key )
    if (( $? ))
    then echo "No Key column found" 1>&2
         return 1
    fi
    value=$( cut -f $keyc "$portindex" | tail -n +2 | grep -n ^"${2}"$ | head -n 1 | sed 's,^\([0-9]*\)[:].*,\1,' )
    echo $(( $value - 1 ))
    return 0
}
function getarrayfiles {
# Gets a list of array files
# Usage: files=( $( getarrayfiles inputportname ) )

    portpath=$( getinput "$1" )
    portindex=$( getinput "_index_"${1} )
    if [ ! -f "$portindex" ]
    then echo "No array index found" 1>&2
        return 1
    fi
    keyf=$( csvcoln "$portindex" File )
    if (( $? ))
    then echo "No File column found" 1>&2
         return 1
    fi
    IFS=$'\n'
    files=( $( cut -f $keyf "$portindex" | tail -n +2 | sed -e 's,\r,,' -e 's,^",,' -e 's,"$,,' ) )
    # returns the absolute path to file, even if File content is relative
    for (( i=0;  i<${#files[@]};i++ ))
    do if [ -e "${portpath}/${files[$i]}" ]
       then echo "${portpath}/${files[$i]}"
       else echo "${files[$i]}"
       fi
    done
    return 0
}

function createarrayindex {
# A simple array index creation script
# Usage: createarrayindex outputportname

    portpath=$( getoutput "$1" )
    portindex=$( getoutput "_index_"${1} )
    if [ ! -f "$portindex" ]
    then echo -e '"Key"'"\t"'"File"' > "${portindex}"
    fi
    IFS=$'\n'
    find "$portpath" -mindepth 1 -maxdepth 1 -printf '%P\t%P\n' | sort | grep -v ^_index >> "${portindex}" || return 0
    return 0
}
