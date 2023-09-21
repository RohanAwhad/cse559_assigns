#!/opt/homebrew/bin/python3

DELIM = '$'

def z_algorithm(text: str, ptrn: str):
  left = right = 0
  s = ptrn + DELIM + text
  z_array = [0] * len(s)
  print(s[len(ptrn)+1:])

  for i in range(1, len(s)):
    print('z array:', list(zip(s, z_array)))
    if i > right:
      #create a new z-box
      left = right = i
      while (right < len(s)) and (s[right] == s[right-left]): right += 1
      right -= 1
      z_array[i] = right - left + 1
      print(s[left:right+1])
    else:
      # you are in a z-box
      j = z_array[i-left]
      val = z_array[j]
      print(val+i)
      # check if the value + i is greater than right
      if (val+i) > right:  # TODO (rohan): confirm '>' or '>='
        # shift left to i, and start a search for new right of the z-box
        left = j
        while (right < len(s)) and (s[right] == s[right-left]): right += 1
        right -= 1
        z_array[i] = right - left + 1
      else:
        z_array[i] = val

  print('final z array:', z_array)
  return z_array


if __name__ == '__main__':
  text = 'ACAGTATCAGTACAG'
  ptrn = 'CAG'
  print('text:', text)
  print('ptrn:', ptrn)

  z_array = z_algorithm(text, ptrn)
  for i, x in enumerate(z_array):
    if x == len(ptrn):
      # zero based indexing
      j = i-len(ptrn)-1
      print(text[j:i-1])
