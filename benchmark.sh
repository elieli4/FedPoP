#!/bin/bash

 rm generate.csv
 echo "FL,n,t,m,tsign_setup,oprf,tsign,verifier">>generate.csv
for n in {10..150..10}; do
	t=$((n*2/3))
	./gen.sh $n $t 0
	sleep 1
	./prove.sh
	sleep 1
done
