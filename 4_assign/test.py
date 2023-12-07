from q1_rohan_awhad import bwt_encode
from q2_rohan_awhad import bwt_decode
from q3_rohan_awhad import lf_mapping
from q4_rohan_awhad import bwm_matching_algo

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
  
def test_q3():
  dir_ = '5_compute_LF_mapping/Debugging' 
  # read s from inputs dir and input_{i}.txt file
  # compare output with outputs dir and output_{i}.txt file
  # use os to list all input files

  for i in range(1, 4):
  with open(f'{dir_}/inputs/input_{i}.txt', 'r') as f:
    _ = [x.strip() for x in f.read().strip().split('\n') if x.strip()]
    s, idx = _[0], int(_[1])
  with open(f'{dir_}/outputs/output_{i}.txt', 'r') as f:
    expected = int(f.read().strip())
  assert lf_mapping(s, idx) == expected

def test_q4():
  dir_ = '6_BWM_algo/Debugging'
  # read s from inputs dir and input_{i}.txt file
  # compare output with outputs dir and output_{i}.txt file
  # use os to list all input files

  for i in range(1, 4):
  with open(f'{dir_}/inputs/input_{i}.txt', 'r') as f:
    _ = [x.strip() for x in f.read().strip().split('\n') if x.strip()]
    s, query_strings = _[0], _[1].split(' ')
  with open(f'{dir_}/outputs/output_{i}.txt', 'r') as f:
    expected = [int(x) for x in f.read().strip().split(' ')]
  assert [bwm_matching_algo(s, q) for q in query_strings] == expected

# for each of the above tests, write a function
# for Submissions dir, instead of Debugging dir
# use os to list all input files
def test_q1_submissions():
  dir_ = '3_compute_BWT_of_a_string/Submissions' 
  # read s from inputs dir and input_{i}.txt file
  # compare output with outputs dir and output_{i}.txt file
  # use os to list all input files

  with open(f'{dir_}/testcases/test_1.txt', 'r') as f:
  s = f.read().strip()
  _ = bwt_encode(s)

def test_q2_submissions():
  dir_ = '4_compute_original_string_given_BWT/Submissions' 
  # read s from inputs dir and input_{i}.txt file
  # compare output with outputs dir and output_{i}.txt file
  # use os to list all input files

  with open(f'{dir_}/testcases/test_1.txt', 'r') as f:
  s = f.read().strip()
  _ = bwt_decode(s)

def test_q3_submissions():
  dir_ = '5_compute_LF_mapping/Submissions' 
  # read s from inputs dir and input_{i}.txt file
  # compare output with outputs dir and output_{i}.txt file
  # use os to list all input files

  with open(f'{dir_}/testcases/test_1.txt', 'r') as f:
  _ = [x.strip() for x in f.read().strip().split('\n') if x.strip()]
  s, idx = _[0], int(_[1])

  _ = lf_mapping(s, idx)

def test_q4_submissions():
  dir_ = '6_BWM_algo/Submissions'
  # read s from inputs dir and input_{i}.txt file
  # compare output with outputs dir and output_{i}.txt file
  # use os to list all input files

  with open(f'{dir_}/testcases/test_1.txt', 'r') as f:
  _ = [x.strip() for x in f.read().strip().split('\n') if x.strip()]
  s, query_strings = _[0], _[1].split(' ')
  _ = [bwm_matching_algo(s, q) for q in query_strings]
  

if __name__ == '__main__':
  test_q1()
  test_q2()
  test_q3()
  test_q4()
  test_q1_submissions()
  test_q2_submissions()
  test_q3_submissions()
  test_q4_submissions()
  print('All tests passed')









