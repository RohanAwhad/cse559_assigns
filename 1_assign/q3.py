#!/opt/homebrew/bin/python3

def get_lps(s):
  lps = [0]
  j = 0
  for i, x in enumerate(s):
    if i == 0: continue

    if s[j] == s[i]:
      j += 1
      lps.append(j)
    elif j == 0:
      lps.append(0)
    else:
      while (j != 0) and (s[j] != s[i]):
        j = lps[j-1]

      lps.append(j)
    print(f'j: {j} | i: {i} | lps: {lps}')

  return lps

get_lps('atcatct')
