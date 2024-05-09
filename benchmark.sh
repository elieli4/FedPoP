#!/bin/bash

for n in {50..150..50};
do
	t=$((n*1/3))
	./gen.sh $n $t 0
done
