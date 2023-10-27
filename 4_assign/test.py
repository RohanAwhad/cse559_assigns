from q1_rohan_awhad import bwt_encode
from q2_rohan_awhad import bwt_decode

# Test 1
def test_q1():
  dir_ = '3_compute_BWT_of_a_string/Debugging' 
  # read s from inputs dir and input_{i}.txt file
  # compare output with outputs dir and output_{i}.txt file
  # use os to list all input files

  for i in range(1, 4):
    with open(f'{dir_}/inputs/input_{i}.txt', 'r') as f:
      s = f.read().strip()
    with open(f'{dir_}/outputs/output_{i}.txt', 'r') as f:
      expected = f.read().strip()
    assert bwt_encode(s) == expected

def test_q2():
  dir_ = '4_compute_original_string_given_BWT/Debugging' 
  # read s from inputs dir and input_{i}.txt file
  # compare output with outputs dir and output_{i}.txt file
  # use os to list all input files

  for i in range(1, 4):
    with open(f'{dir_}/inputs/input_{i}.txt', 'r') as f:
      s = f.read().strip()
    with open(f'{dir_}/outputs/output_{i}.txt', 'r') as f:
      expected = f.read().strip()
    assert bwt_decode(s) == expected
  
