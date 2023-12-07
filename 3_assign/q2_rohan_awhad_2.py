import blosum as bl
matrix = bl.BLOSUM(62)

s1 = "WKMDKSYWLFVREKKTDLCM"
s2 = "AIDDKSWAFVRECKTDQTW"

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

gap_opening_penalty = -11
gap_extension_penalty = -1

M = [[0 for i in range(len(s2)+1)] for j in range(len(s1)+1)]
U = [[0 for i in range(len(s2)+1)] for j in range(len(s1)+1)]
L = [[0 for i in range(len(s2)+1)] for j in range(len(s1)+1)]

max_val = (-1, None, None) # (score, i, j)
for i in range(1,len(s1)+1):
  for j in range(1,len(s2)+1):

    U[i][j] = max(M[i-1][j] + gap_opening_penalty, U[i-1][j] + gap_extension_penalty)
    L[i][j] = max(M[i][j-1] + gap_opening_penalty, L[i][j-1] + gap_extension_penalty)

    M[i][j] = max(
      0,
      M[i-1][j-1] + matrix[s1[i-1]][s2[j-1]],
      #U[i-1][j-1] + matrix[s1[i-1]][s2[j-1]],
      #L[i-1][j-1] + matrix[s1[i-1]][s2[j-1]],
      #U[i][j],
      #L[i][j]
      U[i-1][j-1],
      L[i-1][j-1]
    )

    if M[i][j] > max_val[0]:
      max_val = (M[i][j], i, j)

print(max_val[0])
i, j = max_val[1], max_val[2]
s1_aligned = ""
s2_aligned = ""

while M[i][j] != 0:
  if M[i][j] == U[i][j]:
    s1_aligned = s1[i-1] + s1_aligned
    s2_aligned = "-" + s2_aligned
    i -= 1
  elif M[i][j] == L[i][j]:
    s1_aligned = "-" + s1_aligned
    s2_aligned = s2[j-1] + s2_aligned
    j -= 1
  else:
    s1_aligned = s1[i-1] + s1_aligned
    s2_aligned = s2[j-1] + s2_aligned
    i -= 1
    j -= 1

print(s1_aligned)
print(s2_aligned)
  
