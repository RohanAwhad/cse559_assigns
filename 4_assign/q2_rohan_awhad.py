# decoding a bwt encoded string
def bwt_decode(s):
  '''
  B = [s1,s2,s3,...,sn]
  for i = 1..n:
    sort B
    prepend si to B[i]
  return row of B that ends with $
  '''
  B = list(s)
  for i in range(1, len(B)):
    B = sorted(B)
    B = [s[j] + B[j] for j in range(len(B))]

  assert len(B[0]) == len(s)
  assert len(B) == len(s)
  for x in B:
    if x[-1] == '$': return x


if __name__ == '__main__':
  with open("test_1.txt", "r") as f: s = f.read()
  with open("output_q2_rohan_awhad.txt", "w") as f: f.write(bwt_decode(s))
