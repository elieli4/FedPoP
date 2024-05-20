#!/bin/bash

pkill -f part
pkill -f coord

echo "Beginning generate phase"

N=$1
T=$2
M=$3

S=12001
E=$((S+N-1))

for i in `seq $S $E`; do python3 -m part.py $i & done
python3 coord.py localhost 12001 $T $N $M 0 </dev/null

echo "Clearing processes"

pkill -f 'part'
pkill -f 'coord'

