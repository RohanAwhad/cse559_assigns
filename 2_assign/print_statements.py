from config import A, C, T, G
from typing import List


def print_profile_set(profile_set: List[List[float]]) -> None:
  print('-'*50)
  print('Profile:')
  print(f'A: {"  ".join([f"{x:.2f}" for x in profile_set[A]])}')
  print(f'C: {"  ".join([f"{x:.2f}" for x in profile_set[C]])}')
  print(f'T: {"  ".join([f"{x:.2f}" for x in profile_set[T]])}')
  print(f'G: {"  ".join([f"{x:.2f}" for x in profile_set[G]])}')


def print_motif_set(title: str, motif_set: List[str]) -> None:
  print('-'*50)
  print(title)
  for motif in motif_set: print(f'  {motif}')

