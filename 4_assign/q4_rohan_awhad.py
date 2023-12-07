from functools import lru_cache

@lru_cache(maxsize=None)
def lf_mapping(s):
  sorted_s = sorted(s)

  l2f = {}
  for i in range(len(s)):
    query_char = s[i]
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

    l2f[i] = j

  return l2f


def bwm_matching_algo(s, query_s):
  l2f = lf_mapping(s)
  last_col = s

  top, bottom = 0, len(s) - 1
  for x in reversed(query_s):
    # find all the instances of x in last_col
    # get their indices in first_col
    # set top to the lowest index
    # and bottom to the highest index

    # find all the instances of x in last_col
    indices = []
    for i, char in enumerate(last_col[top:bottom + 1]):
      if char == x:
        indices.append(top+i)
    if len(indices) == 0: return 0

    # get their indices in first_col
    new_indices = [l2f[i] for i in indices]

    # set top to the lowest index
    # and bottom to the highest index
    top, bottom = min(new_indices), max(new_indices)

    if top > bottom:
      return 0

  return bottom - top + 1


if __name__ == '__main__':
  with open("test_1.txt", "r") as f:
    _ = [x.strip() for x in f.read().strip().split('\n') if x.strip()]
    s, query_strings = _[0], _[1].split(' ')
  with open("output_q4_rohan_awhad.txt", "w") as f:
    ret = [str(bwm_matching_algo(s, q)) for q in query_strings]
    f.write(' '.join(ret))

