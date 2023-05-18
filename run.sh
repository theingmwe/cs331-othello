#!/bin/sh
echo -e "Testing search vs depth\n"
echo "depth,pruning,heuristic,nodes"
for I in 2 4 6 8 10 12 # Depth
do
  for J in 0 1 # Pruning
  do
    for K in 0 1 2 # Heuristic
    do
      NODES=$(python3 GameDriver.py alphabeta alphabeta $K $J $K $J $I $I 0)
      echo "$I,$J,$K,$NODES"
    done
  done
done

echo -e "Testing heuristic quality\n\n"
echo -e "depth,h1,h2,win\n"
for I in 2 4 6 8 # Depth
do
  for J in 0 1 2 # Heuristic
  do
    for K in 0 1 2 # Heuristic 2
    do
      if [ $J -ne $K ]; then
        WIN=$(python3 GameDriver.py alphabeta alphabeta $J 1 $K 1 $I $I 1)
        echo "$I,$J,$K,$WIN"
      fi
    done
  done
done