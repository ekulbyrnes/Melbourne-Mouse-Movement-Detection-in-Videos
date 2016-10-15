#!/bin/bash
# crappy bash but does the job - there is absolutely no error handling in here

# Extract snippets from a movie. The snippets are fixed size (hardcoded as 4 seconds) and overlap 50%.
# Snippets are only created for certain segments of the movie. These segments are defined via a second
# input file containing start and end markers of the segments. 
# Output files are named {input file path}-{snippet start in seconds}.
# Existing output will be overwritten.
#
# Parameters:
# 1 - name of raw footage to extract snippets from
# 2 - name of a text-based marker file with start & end times in seconds
#
# Example: ./split.sh sample-video-123.mp4 sample-video-123.txt
#
# This marker file needs to have the line format {start in seconds} { end in seconds}, e.g.
# 13 19
# 77 83
# meaning segments of activity starting at seconds 13 and ending at 19, 
# then the 2nd one starting at 77 seconds and ending at 83 seconds.



# get the input file name as the first parameter from the command line
export inputMovie=$1

# get the marker file name as the second parameter from the command line
export inputMarkers=$2

# half the time window size measured in seconds
export delta=2 

echo "Splitting file $inputMovie into active segments, based on markers from $inputMarkers"

cat $inputMarkers | while read line; do
    line=( ${line//,/ } )
    export start=${line[0]}
    export end=${line[1]}
    echo "...splitting active segment from ${start} to ${end}"
    
    export clipStart=$(( $start - $delta ))   
    while (($clipStart < $end)); do
      export duration=$(( 2*$delta ))
      export clipEnd=$(( $clipStart + $duration ))
      echo "...extracting $clipStart for $duration"
      ffmpeg </dev/null -y -loglevel panic -i $inputMovie -ss ${clipStart} -t $duration output/$inputMovie-$clipStart.mp4      
      rc=$?
      if [[ $rc != 0 ]] ; then
	  echo "Darn, ffmpeg failed"
      fi

      export clipStart=$(( $clipStart + $delta ))
  done
done
echo "Done."

