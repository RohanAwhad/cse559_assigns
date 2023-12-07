def lf_mapping(s, i):
  query_char = s[i]
  sorted_s = sorted(s)

  # find out number of occurences of the query_char in s, uptill query_char
  cnt = 0
  for j, char in enumerate(s):
    if char == query_char:
      cnt += 1
    if j == i:
      break

  # find out the index of the query_char in sorted_s
  for j, char in enumerate(sorted_s):
    if char == query_char:
      cnt -= 1
    if cnt == 0:
      break

  return j


if __name__ == '__main__':
  with open("test_1.txt", "r") as f:
    _ = [x.strip() for x in f.read().strip().split('\n') if x.strip()]
    s, i = _[0], int(_[1])
  with open("output_q3_rohan_awhad.txt", "w") as f:
    f.write(str(lf_mapping(s, i)))

