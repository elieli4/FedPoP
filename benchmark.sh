#!/bin/bash

rm generate.csv
echo "FL,n,t,m,tsign_setup,oprf,tsign,verifier">>generate.csv
for n in {50..50..50};
do
	t=$((n*1/3))
	./gen.sh $n $t 0
	./prove.sh
done
