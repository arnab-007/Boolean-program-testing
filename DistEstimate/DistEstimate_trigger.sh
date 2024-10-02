#!/bin/bash


gcc Codex9.c
RANDOM_SEED=$RANDOM  # Alternatively, you can use: $(date +%s)

# Call CMSGen with the random seed
./cmsgen/build/cmsgen -s $RANDOM_SEED --samples=600 --samplefile=samples.out input-cnf
python3 DistEstimate.py