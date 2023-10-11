#!python3

import config
from print_statements import *
from config import A, C, T, G

import os  # TODO (rohan): give debug levels to print statements
import random
import sys

from collections import Counter
from tqdm import tqdm
from typing import List, Tuple, Dict

DEBUG = int(os.environ.get('DEBUG', 0))


def get_motif_consensus(motif_set: List[str]) -> str:
  ret = []
  for i in range(len(motif_set[0])):
    _tmp = max(
      tuple(Counter([x[i] for x in motif_set]).items()),
      key=lambda x: x[1]
    )
    ret.append(_tmp[0])

  return ''.join(ret)


def get_motif_score(motif_set: List[str], motif_consensus: str) -> int:
  ret = 0
  for i, x in enumerate(motif_consensus):
    for y in motif_set:
      if y[i] != x: ret += 1
    
  return ret

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
    start_kmer = random.randint(0, end)
    if DEBUG > 1: print(f'selecting start of k-mer to be: {start_kmer}')
    motif_set.append(dna[start_kmer: start_kmer+k])

  if DEBUG > 0: print_motif_set('Initial motif set:', motif_set)

  motif_consensus = get_motif_consensus(motif_set)
  best_set = (tuple(motif_set), get_motif_score(motif_set, motif_consensus))

  cntr = 1
  while True:
    profile_set = get_profile(motif_set)
    if DEBUG > 0: print_profile_set(profile_set)
    motif_set = get_motifs_from_profile(profile_set, dna_strings)
    if DEBUG > 0: print_motif_set('Intermediate motif set:', motif_set)
    motif_consensus = get_motif_consensus(motif_set)
    motif_score = get_motif_score(motif_set, motif_consensus)
    
    if DEBUG > 0: print(f'Completed {cntr:5d} loops')
    cntr += 1

    if motif_score < best_set[1]: best_set = (tuple(motif_set), motif_score) # finding minima
    else: return best_set


def get_motifs_from_profile(profile_set: List[List[float]], dna_strings: List[str]) -> List[str]:
  
  k = len(profile_set[0])
  motif_set = []
  for dna in dna_strings:
    max_prob = 0.0
    max_start = -1

    if DEBUG > 1:
      print()
      print(dna)

    for start in range(len(dna)-k+1):
      kmer_prob = 1.0
      for i, x in enumerate(dna[start:start+k]):
        kmer_prob *= profile_set[config.CHAR2IDX[x]][i]

      if DEBUG > 1: print(f'  {dna[start:start+k]} : {kmer_prob:.10f}')
      if max_prob < kmer_prob:
        max_prob = kmer_prob
        max_start = start

    motif_set.append(dna[max_start: max_start+k])

  return motif_set

def get_profile(motif_set: List[str]) -> List[List[float]]:
  
  profile_set: List[List[float]] = [[], [], [], []]
  for i in range(len(motif_set[0])):
    _ = [x[i] for x in motif_set] + list('ATCG')  # for non-zero probs
    _tmp: Dict[str, float] = dict(map(
      lambda x: (x[0], x[1]/len(_)),  # getting probs
      Counter(_).items())
    )

    profile_set[A].append(_tmp['A'])
    profile_set[C].append(_tmp['C'])
    profile_set[T].append(_tmp['T'])
    profile_set[G].append(_tmp['G'])

  return profile_set



def main():
  with open(sys.argv[1], 'r') as f:
    txt = [x for x in f.read().upper().split('\n') if x]

  dna_strings = txt[1:]
  k, t = list(map(int, txt[0].split()))
  if DEBUG > 0:
    print(f'k: {k} | t: {t}')
    print('dna strings:')
    for dna in dna_strings: print(' ', dna)

  assert len(dna_strings) == t

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
    if DEBUG == 0: break
  
if __name__ == '__main__':
  if DEBUG > 1:
    test_set = [
      'TCGGGGGTTTTT',
      'CCGGTGACTTAC',
      'ACGGGGATTTTC',
      'TTGGGGACTTTT',
      'AAGGGGACTTCC',
      'TTGGGGACTTCC',
      'TCGGGGATTCAT',
      'TCGGGGATTCCT',
      'TAGGGGAACTAC',
      'TCGGGTATAACC',
    ]
    print_motif_set('Test motif set:', test_set)
    motif_consensus = get_motif_consensus(test_set)
    print(f'Motif Consesus is {motif_consensus}')
    print(f'Motif score for the above set: {get_motif_score(test_set, motif_consensus)}')
    profile_set = get_profile(test_set)
    print_profile_set(profile_set)
    print()

  main()
