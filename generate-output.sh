#!/bin/bash 

if [[ $1 == "" ]] || [[ $2 == "" ]] || [[ $3 == "" ]]; then
	echo "Usage: $0 <player_max> <min_pop> <max_pop>"
	exit
fi

player_max=$1
min_pop_i=$2
max_pop_i=$(($3 - 1))
max_pop_j=$3



for n in $(seq 1 $player_max); do
	for i in $(seq $min_pop_i $max_pop_i); do
		min_pop_j=$((i + 1))
		for j in $(seq $min_pop_j $max_pop_j); do
			if [[ ! -f "output/$n.75.$i.$j.pdf" ]]; then
				echo "Generating $n.75.$i.$j.pdf"
				./stack-game.py graph $n 75 $i $j
			fi
		done
	done
done
