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

indices = {x: i for i, x in enumerate(indices)}
def blosum62_value(a, b): return matrix[indices[a]][indices[b]]

def global_alignment(s1, s2, gap_penalty):
  M = [[0 for j in range(len(s2) + 1)] for i in range(len(s1) + 1)]
  for i in range(len(s1) + 1): M[i][0] = -i * gap_penalty
  for j in range(len(s2) + 1): M[0][j] = -j * gap_penalty

  for i in range(1, len(s1) + 1):
    for j in range(1, len(s2) + 1):
      match = M[i - 1][j - 1] + blosum62_value(s1[i - 1], s2[j - 1])
      delete = M[i - 1][j] - gap_penalty
      insert = M[i][j - 1] - gap_penalty
      M[i][j] = max(match, delete, insert)

  aligned_s1, aligned_s2 = "", ""
  i, j = len(s1), len(s2)
  while i > 0 or j > 0:
    current_score = M[i][j]
    if i > 0 and M[i - 1][j] - gap_penalty == current_score:
      aligned_s1 += s1[i - 1]
      aligned_s2 += '-'
      i -= 1
    elif j > 0 and M[i][j - 1] - gap_penalty == current_score:
      aligned_s1 += '-'
      aligned_s2 += s2[j - 1]
      j -= 1
    else:
      aligned_s1 += s1[i - 1]
      aligned_s2 += s2[j - 1]
      i -= 1
      j -= 1

  return int(M[len(s1)][len(s2)]), aligned_s1[::-1], aligned_s2[::-1]

# read input sequences
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

# calculate global alignment
output = global_alignment(s1, s2, 5)
for x in output: print(x)

# write output
with open('output_q1_rohan_awhad.txt', 'w') as f:
  f.write('\n'.join([str(x) for x in output]))
  f.write('\n')
