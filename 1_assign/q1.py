#!/opt/homebrew/bin/python3
import sys
import os
from loguru import logger
logger.remove()
logger.add('logs')
with open('logs', 'a') as f: f.write('\n'+'-'*50+'\n')

DELIM = '$'
OUTPUTS_DIR = 'outputs'
os.makedirs(OUTPUTS_DIR, exist_ok=True)

def z_algorithm(text: str, ptrn: str):
  left = right = 0
  s = ptrn + DELIM + text
  z_array = [0] * len(s)
  logger.debug(s[len(ptrn)+1:])

  for i in range(1, len(s)):
    logger.debug(f'z array: {list(zip(s, z_array))}')
    if i > right:
      #create a new z-box
      left = right = i
      while (right < len(s)) and (s[right] == s[right-left]): right += 1
      right -= 1
      z_array[i] = right - left + 1
      logger.debug(s[left:right+1])
    else:
      # you are in a z-box
      j = z_array[i-left]
      val = z_array[j]
      logger.debug(val+i)
      # check if the value + i is greater than right
      if (val+i) > right:  # TODO (rohan): confirm '>' or '>='
        # shift left to i, and start a search for new right of the z-box
        left = j
        while (right < len(s)) and (s[right] == s[right-left]): right += 1
        right -= 1
        z_array[i] = right - left + 1
      else:
        z_array[i] = val

  logger.debug(f'final z array: {z_array}')
  return z_array


if __name__ == '__main__':
  if len(sys.argv) > 1: fn = sys.argv[1]
  else: raise ValueError('expected filename as an argument. didn\'t recieve anything')

  with open(fn, 'r') as f: text, ptrn, *_ = f.read().split('\n')
  logger.debug(f'text: {text}')
  logger.debug(f'ptrn: {ptrn}')

  z_array = z_algorithm(text, ptrn)
  ans = []
  for i, x in enumerate(z_array):
    if x == len(ptrn):
      # zero-based indexing
      j = i-len(ptrn)-1
      logger.debug(text[j:i-1])
      ans.append(j+1)  # converting to one-based indexing

  with open(f'{OUTPUTS_DIR}/{fn.split("/")[-1]}', 'w') as f: f.write('\n'.join(map(str, ans)))
