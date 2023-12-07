#!/opt/homebrew/bin/python3

from q1 import z_algorithm

import os

DELIM = '$'

def test_1():
  s = 'rohanrorohrohanrorohan'
  exp = [0, 0, 0, 0, 0, 2, 0, 3, 0, 0, 10, 0, 0, 0, 0, 2, 0, 5, 0, 0, 0, 0]
  act = z_algorithm(s)
  assert exp == act, f'exp: {exp}\nact:{act}'

def test_2():
  ex_dir = 'examples'
  qa_pairs = [
    ('ex_0', 'exsol_0'),
    ('ex_1', 'exsol_1'),
    ('ex_2', 'exsol_2'),
  ]

  for q, a in qa_pairs:
    fn = f'{ex_dir}/{q}'
    with open(f'{ex_dir}/{q}', 'r') as f: text, ptrn, *_ = f.read().split('\n')
    with open(f'{ex_dir}/{a}', 'r') as f: exp = [int(x) for x in f.read().split('\n') if x]

    s = ptrn + DELIM + text
    z_array = z_algorithm(s)
    act = []
    for i, x in enumerate(z_array):
      if x == len(ptrn):
        # zero-based indexing
        j = i-len(ptrn)-1
        act.append(j+1)  # converting to one-based indexing

    assert exp == act, f'exp: {exp}\nact:{act}'


if __name__ == '__main__':
  test_1()
  test_2()
