import os

DEBUG = int(os.environ.get('DEBUG', 0))
PROFILE = int(os.environ.get('PROFILE', 0))
SAVE = int(os.environ.get('SAVE', 0))
OPTIMIZE = int(os.environ.get('OPTIMIZE', 0))

# for easier numpy calc & indexing
A, C, T, G = 0, 1, 2, 3
CHAR2IDX = {
  'A': 0,
  'C': 1,
  'T': 2,
  'G': 3
}
IDX2CHAR = dict((y, x) for x, y in CHAR2IDX.items())

os.makedirs('outputs', exist_ok=True)
OUT_FN_TMPLT = 'outputs/{algo}_{testcase}.txt'
