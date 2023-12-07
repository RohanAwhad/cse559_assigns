# decoding a bwt encoded string
def bwt_decode(s):
  B = list(s)
  for i in range(1, len(B)):
    B = sorted(B)
    B = [s[j] + B[j] for j in range(len(B))]

  assert len(B[0]) == len(s)
  assert len(B) == len(s)
  for x in B:
    if x[-1] == "$": return x


if __name__ == "__main__":
  with open("test_1.txt", "r") as f: s = f.read().strip()
  with open("output_q2_rohan_awhad.txt", "w") as f: f.write(bwt_decode(s))
