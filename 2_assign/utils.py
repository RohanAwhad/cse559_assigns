import config
from config import A, C, T, G, DEBUG, OPTIMIZE

import numpy as np
from collections import Counter
from typing import List, Dict

if OPTIMIZE: import cy_utils

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


def get_motifs_from_profile(profile_set: List[List[float]], dna_strings: List[str]) -> List[str]:
  
  if OPTIMIZE: return cy_utils.get_motifs_from_profile(dna_strings, *np.array(profile_set))
  
  k = len(profile_set[0])
  motif_set = []
  for dna in dna_strings:
    kmer = _select_kmer(k, dna, profile_set)
    motif_set.append(kmer)

  return motif_set

def _select_kmer(k: int, dna: str, profile_set: List[List[float]]) -> str:
  max_prob = 0.0
  max_start = -1

  if DEBUG > 1:
    print()
    print(dna)

  for start in range(len(dna)-k+1):
    kmer_prob = 1.0
    for i, x in enumerate(dna[start:start+k]):
      kmer_prob *= profile_set[config.CHAR2IDX[x]][i]
      if kmer_prob < max_prob: break

    if DEBUG > 1: print(f'  {dna[start:start+k]} : {kmer_prob:.10f}')
    if max_prob < kmer_prob:
      max_prob = kmer_prob
      max_start = start

  return dna[max_start: max_start+k]



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


