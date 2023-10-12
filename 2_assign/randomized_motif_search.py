#!python3

import config
import utils
from print_statements import *
from config import A, C, T, G, DEBUG

import os
import random
import sys

from collections import Counter
from tqdm import tqdm
from typing import List, Tuple, Dict


def randomized_motif_search(k: int, dna_strings: List[str]) -> Tuple[Tuple[str, ...], int]:
  # make them curr best motifs
  # iterate
  # get profile of motifs
  # generate new set of motifs based on that profile
  # if curr motif score is less than best motif score return best motif
  # else update best motif to curr motif

  # get random motifs from each dna string
  if DEBUG > 0: print(f'len of a dna string: {len(dna_strings[0])}')
  motif_set = []
  for dna in dna_strings:
    end = len(dna) - k
    if DEBUG > 1: print(f'range for selection: [   0, {end:3d}]')
    start_kmer = random.randint(0, end)
    if DEBUG > 1: print(f'selecting start of k-mer to be: {start_kmer}')
    motif_set.append(dna[start_kmer: start_kmer+k])

  if DEBUG > 0: print_motif_set('Initial motif set:', motif_set)

  motif_consensus = utils.get_motif_consensus(motif_set)
  best_set = (tuple(motif_set), utils.get_motif_score(motif_set, motif_consensus))

  cntr = 1
  while True:
    profile_set = utils.get_profile(motif_set)
    if DEBUG > 0: print_profile_set(profile_set)
    motif_set = utils.get_motifs_from_profile(profile_set, dna_strings)
    if DEBUG > 0: print_motif_set('Intermediate motif set:', motif_set)
    motif_consensus = utils.get_motif_consensus(motif_set)
    motif_score = utils.get_motif_score(motif_set, motif_consensus)
    
    if DEBUG > 0: print(f'Completed {cntr:5d} loops')
    cntr += 1

    if motif_score < best_set[1]: best_set = (tuple(motif_set), motif_score) # finding minima
    else: return best_set


def main():
  with open(sys.argv[1], 'r') as f:
    txt = [x for x in f.read().upper().split('\n') if x]

  dna_strings = txt[1:]
  k, t = list(map(int, txt[0].split()))
  if DEBUG > 0:
    print(f'k: {k} | t: {t}')
    print('dna strings:')
    for dna in dna_strings: print(' ', dna)

  assert len(dna_strings) == t, f'number of dna strings {len(dna_strings)} != t ({t})'

  # 1500 runs
  n = 15 if DEBUG > 0 else 1500
  pbar = range(n)
  if DEBUG == 0: pbar = tqdm(pbar, desc='Motif Search', total=n)
  best_sets = set()
  for _ in pbar:
    best_sets.add(randomized_motif_search(k, dna_strings))

  best_in_1500 = min(best_sets, key=lambda x: x[1])
  for mset in filter(lambda x: x[1] == best_in_1500[1], best_sets):
    print_motif_set(f"Best Motif set in {n:4d} runs:", mset[0])
    print(f'Motif Score: {mset[1]:3d}')
    if DEBUG == 0:
      # write to a file
      out_fn = config.OUT_FN_TMPLT.format(
        algo='randomized_motif_search',
        testcase=sys.argv[1].split('/')[-1].split('.')[0].split('_')[-1],
      )
      print(f'Writing the output to "{out_fn}"')
      with open(out_fn, 'w') as f:
        f.write('\n'.join(mset[0]))
        f.write(f'\nMotif Score: {mset[1]:3d}')
      return None
  
if __name__ == '__main__':
  main()
