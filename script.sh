#!/bin/bash

(for name in $(ls data); do
  cat data/${name} | grep "20" | perl -pe "s/^([^\t]*)\t/\1\t${name}\t/"
done) | sort > COMBINED

(
  cat COMBINED;
  echo -e "SENTINEL\tTO\tTO\tw1\tw2\tw3\tcat\t2020\t0"
) | ./script.py
