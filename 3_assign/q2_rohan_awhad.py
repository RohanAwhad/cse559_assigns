import os
DEBUG = int(os.environ.get('DEBUG', 0))

indices = ["A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V", "B", "Z", "X"]
matrix = [
  [ 4, -1, -2, -2,  0, -1, -1,  0, -2, -1, -1, -1, -1, -2, -1,  1,  0, -3, -2,  0, -2, -1,  0],  
  [-1,  5,  0, -2, -3,  1,  0, -2,  0, -3, -2,  2, -1, -3, -2, -1, -1, -3, -2, -3, -1,  0, -1],  
  [-2,  0,  6,  1, -3,  0,  0,  0,  1, -3, -3,  0, -2, -3, -2,  1,  0, -4, -2, -3,  3,  0, -1],  
  [-2, -2,  1,  6, -3,  0,  2, -1, -1, -3, -4, -1, -3, -3, -1,  0, -1, -4, -3, -3,  4,  1, -1],  
  [ 0, -3, -3, -3,  9, -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1, -3, -3, -2],  
  [-1,  1,  0,  0, -3,  5,  2, -2,  0, -3, -2,  1,  0, -3, -1,  0, -1, -2, -1, -2,  0,  3, -1],  
  [-1,  0,  0,  2, -4,  2,  5, -2,  0, -3, -3,  1, -2, -3, -1,  0, -1, -3, -2, -2,  1,  4, -1],  
  [ 0, -2,  0, -1, -3, -2, -2,  6, -2, -4, -4, -2, -3, -3, -2,  0, -2, -2, -3, -3, -1, -2, -1],  
  [-2,  0,  1, -1, -3,  0,  0, -2,  8, -3, -3, -1, -2, -1, -2, -1, -2, -2,  2, -3,  0,  0, -1],  
  [-1, -3, -3, -3, -1, -3, -3, -4, -3,  4,  2, -3,  1,  0, -3, -2, -1, -3, -1,  3, -3, -3, -1],  
  [-1, -2, -3, -4, -1, -2, -3, -4, -3,  2,  4, -2,  2,  0, -3, -2, -1, -2, -1,  1, -4, -3, -1],  
  [-1,  2,  0, -1, -3,  1,  1, -2, -1, -3, -2,  5, -1, -3, -1,  0, -1, -3, -2, -2,  0,  1, -1],  
  [-1, -1, -2, -3, -1,  0, -2, -3, -2,  1,  2, -1,  5,  0, -2, -1, -1, -1, -1,  1, -3, -1, -1],  
  [-2, -3, -3, -3, -2, -3, -3, -3, -1,  0,  0, -3,  0,  6, -4, -2, -2,  1,  3, -1, -3, -3, -1],  
  [-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4,  7, -1, -1, -4, -3, -2, -2, -1, -2],  
  [ 1, -1,  1,  0, -1,  0,  0,  0, -1, -2, -2,  0, -1, -2, -1,  4,  1, -3, -2, -2,  0,  0,  0],  
  [ 0, -1,  0, -1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -2, -1,  1,  5, -2, -2,  0, -1, -1,  0],  
  [-3, -3, -4, -4, -2, -2, -3, -2, -2, -3, -2, -3, -1,  1, -4, -3, -2, 11,  2, -3, -4, -3, -2],  
  [-2, -2, -2, -3, -2, -1, -2, -3,  2, -1, -1, -2, -1,  3, -3, -2, -2,  2,  7, -1, -3, -2, -1],  
  [ 0, -3, -3, -3, -1, -2, -2, -3, -3,  3,  1, -2,  1, -1, -2, -2,  0, -3, -1,  4, -3, -2, -1],  
  [-2, -1,  3,  4, -3,  0,  1, -1,  0, -3, -4,  0, -3, -3, -2,  0, -1, -4, -3, -3,  4,  1, -1],  
  [-1,  0,   0, 1, -3,  3,  4, -2,  0, -3, -3,  1, -1, -3, -1,  0, -1, -3, -2, -2,  1,  4, -1],  
  [ 0, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2,  0,  0, -2, -1, -1, -1, -1, -1],  
]
# print matrix in a pretty format
if DEBUG:
  print('---')
  for i, x in enumerate(indices):
    for j, y in enumerate(indices):
      print(f'{x}{y}:{matrix[i][j]:3d}', end='  ')
    print()


indices = {x: i for i, x in enumerate(indices)}
def blosum62_value(a, b): return matrix[indices[a]][indices[b]]

def local_alignment_affine_gap(s1, s2, sigma, epsilon):
  M = [[0] * (len(s2)+1) for _ in range(len(s1)+1)]
  X = [[0] * (len(s2)+1) for _ in range(len(s1)+1)]  # extension gap penalties in s1
  Y = [[0] * (len(s2)+1) for _ in range(len(s1)+1)]  # extension gap penalties in s2

  M = [[0 for _ in range(len(s2)+1)] for _ in range(len(s1)+1)]
  X = [[0 for _ in range(len(s2)+1)] for _ in range(len(s1)+1)]
  Y = [[0 for _ in range(len(s2)+1)] for _ in range(len(s1)+1)]

  # instantiating first row and column of X and Y matrices
  # to -2*sigma
  for i in range(1, len(s2)+1):
    X[0][i] = -2*sigma
    Y[0][i] = -2*sigma
  for i in range(1, len(s1)+1):
    X[i][0] = -2*sigma
    Y[i][0] = -2*sigma

  max_val = (0, 0, 0)  # (value, i, j)

  if DEBUG:
    print('Pre Fill:')
    print('---')
    print('X:')
    for i in range(len(s1)+1):
      for j in range(len(s2)+1):
        print(f'{X[i][j]:3d}', end='  ')
      print()

    print('---')
    print('Y:')
    for i in range(len(s1)+1):
      for j in range(len(s2)+1):
        print(f'{Y[i][j]:3d}', end='  ')
      print()

  s1, s2 = s1.upper(), s2.upper()
  if DEBUG: print(s1 + '\n' + s2)
  for i in range(1, len(s1)+1):
    for j in range(1, len(s2)+1):
      if i > 1 and j > 1:
        X[i][j] = max(M[i-1][j] - sigma, X[i-1][j] - epsilon, 0)
        Y[i][j] = max(M[i][j-1] - sigma, Y[i][j-1] - epsilon, 0)

      M[i][j] = max(
        0,
        M[i-1][j-1] + blosum62_value(s1[i-1], s2[j-1]),
        X[i][j],
        Y[i][j]
      )

      if M[i][j] > max_val[0]: max_val = (M[i][j], i, j)

  # print X and Y matrices
  if DEBUG:
    print('---')
    print('X:')
    for i in range(1, len(s1)+1):
      for j in range(1, len(s2)+1):
        print(f'{s1[i-1]}{s2[j-1]}:{X[i][j]:3d}', end='  ')
      print()

    print('---')
    print('Y:')
    for i in range(1, len(s1)+1):
      for j in range(1, len(s2)+1):
        print(f'{s1[i-1]}{s2[j-1]}:{Y[i][j]:3d}', end='  ')
      print()

    print('---')
    print('M:')
    for i in range(1, len(s1)+1):
      for j in range(1, len(s2)+1):
        print(f'{s1[i-1]}{s2[j-1]}:{M[i][j]:3d}', end='  ')
      print()

    print('---')
  
  # Traceback
  u1, u2 = [], []
  i, j = max_val[1], max_val[2]

  #while M[i][j] != 0 and i > 0 and j > 0:
  while M[i][j] != 0:
    #if M[i][j] == (X[i-1][j-1] + blosum62_value(s1[i-1], s2[j-1])):
    if M[i][j] == X[i][j]:
      u1.append(s1[i-1])
      if DEBUG: print(s1[i-1], '-')
      i -= 1
    if M[i][j] == Y[i][j]:
      u2.append(s2[j-1])
      if DEBUG: print('-', s2[j-1])
      j -= 1
    if M[i][j] == (M[i-1][j-1] + blosum62_value(s1[i-1], s2[j-1])):
      u1.append(s1[i-1])
      u2.append(s2[j-1])
      if DEBUG: print(s1[i-1], s2[j-1])
      i -= 1
      j -= 1

    if DEBUG: print('---')


  if DEBUG: print(max_val)
  return max_val[0], ''.join(u1[::-1]), ''.join(u2[::-1])

sigma, epsilon = 11, 1

# read input from file
sequences = []
with open('test_1.txt', 'r') as f:
  _tmp = None
  for x in f.read().split('\n'):
    if not x: continue
    if x.startswith('>'):
      if _tmp is not None: sequences.append(''.join(_tmp))
      _tmp = []
      continue
    _tmp.append(x)

if _tmp is not None and len(_tmp) > 0: sequences.append(''.join(_tmp))
assert len(sequences) == 2, f'Expected 2 sequences, got {len(sequences)}'
s1, s2 = sequences

# calculate local alignment
output = local_alignment_affine_gap(s1, s2, sigma, epsilon)
if DEBUG: print(len(output[1]), len(output[2]))
for x in output: print(x)

# write output to file
with open('output_q2_rohan_awhad.txt', 'w') as f:
  f.write('\n'.join([str(x) for x in output]))
  #f.write('\n')
