#!python3

import utils
from config import DEBUG, PROFILE
from print_statements import *
from gibbs_sampling_motif_search import gibbs_sampling
from randomized_motif_search import randomized_motif_search

import sys
import threading
from tqdm import tqdm

SAVE_FN = 'outputs/q3_results.txt'

if __name__ == '__main__':
  with open(sys.argv[1], 'r') as f:
  dna_strings = [x for x in f.read().split('\n') if x]

  k = 15
  r = 100

  # randomized sampling
  if DEBUG == 1: n = [10]
  elif DEBUG > 1: n = [2]
  else: n = [1_000, 10_000, 100_000]
  for i in n:
  best_sets = []
  for _ in tqdm(range(i), desc='Randomized Motif Search'):
    best_sets.append(randomized_motif_search(k, dna_strings))

  # result printing
  best_sets = set(best_sets)
  best_in_1500 = min(best_sets, key=lambda x: x[1])
  for mset in filter(lambda x: x[1] == best_in_1500[1], best_sets):
    print_motif_set(f"Best Motif set in {i:6d} runs:", mset[0])
    print(f'Motif Score: {mset[1]:3d}')
    print(f'Motif Consensus: {utils.get_motif_consensus(mset[0])}')

    # write to a file
    data = f"Best Motif set in {i:6d} runs:\n"
    data += '\n'.join(mset[0]) + '\n'
    data += f'Motif Score: {mset[1]:3d}\n'
    data += f'Motif Consensus: {utils.get_motif_consensus(mset[0])}\n'
    data += ('-'*50) + '\n'
    with open(SAVE_FN, 'a+') as f: f.write(data)


  # gibbs sampling
  n = [1000, 2000, 10000]
  for i in n:
  best_sets = []
  for _ in tqdm(range(i), desc='Gibbs Sampling Motif Search'):
    best_sets.append(gibbs_sampling(k, r, dna_strings))

  # result printing
  best_sets = set(best_sets)
  best_in_1500 = min(best_sets, key=lambda x: x[1])
  for mset in filter(lambda x: x[1] == best_in_1500[1], best_sets):
    print_motif_set(f"Best Motif set in {i:6d} runs:", mset[0])
    print(f'Motif Score: {mset[1]:3d}')
    print(f'Motif Consensus: {utils.get_motif_consensus(mset[0])}')

    # write to a file
    data = f"Best Motif set in {i:6d} runs:\n"
    data += '\n'.join(mset[0]) + '\n'
    data += f'Motif Score: {mset[1]:3d}\n'
    data += f'Motif Consensus: {utils.get_motif_consensus(mset[0])}\n'
    data += ('-'*50) + '\n'
    with open(SAVE_FN, 'a+') as f: f.write(data)
  
