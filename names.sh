#!/bin/bash

cat COMBINED | cut -f1 | sort | uniq > NAMES1

for f in NAMES1 NAMES2 NAMES3; do
  cat $f \
    | perl -ne 'print uc($_)' \
    | perl -pe 's/THE //; s/[.,]//g;' \
    | perl -pe 's/\bUSA\b//;' \
    | perl -pe 's/FOUNDATION/FUND/g;' \
    | perl -pe 's/ INC//g;' \
    | perl -pe 's/&/ AND /g;' \
    | perl -pe 's/[ ]+/ /g;' \
    | perl -pe 's/LUCILLE/LUCILE/g;' \
    | sort \
    | uniq \
    > $f.sort
done

comm -1 NAMES1.sort NAMES2.sort

echo
echo
echo

comm -1 NAMES1.sort NAMES3.sort

