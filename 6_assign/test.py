import q1_rohan_awhad as q1
import q2_rohan_awhad as q2
import numpy as np

def test_q1():
  DEBUG_DIR = "1_k_means_hard/Debugging"
  for i in range(1, 4):
    with open(f"{DEBUG_DIR}/inputs/input_{i}.txt") as f: sample_inp = f.read().strip()
    k, data_points = q1.parse_inp(sample_inp)
    centers = q1.main(k, data_points)
    with open(f"{DEBUG_DIR}/outputs/output_{i}.txt", "r") as f: exp = f.read().strip()
    exp = [list(map(float, line.split())) for line in exp.split("\n")]
    distances = []
    for center in centers:
      dist = [(i, q1.distance(center, exp[i])) for i in range(len(exp))]
      distances.append(min(dist, key=lambda x: x[1]))
    print(np.array(distances)[:, 1])


def test_q2():
  DEBUG_DIR = "2_k_means_soft/Debugging"
  for i in range(1, 4):
    with open(f"{DEBUG_DIR}/inputs/input_{i}.txt") as f: sample_inp = f.read().strip()
    k, m, beta, data_points = q2.parse_inp(sample_inp)
    centers = q2.main(k, m, beta, data_points)
    with open(f"{DEBUG_DIR}/outputs/output_{i}.txt", "r") as f: exp = f.read().strip()
    exp = [list(map(float, line.split())) for line in exp.split("\n")]
    distances = []
    for center in centers:
      dist = [(i, q2.distance(center, exp[i])) for i in range(len(exp))]
      distances.append(min(dist, key=lambda x: x[1]))
    print(np.array(distances))

if __name__ == '__main__':
  print('Testing Q1 ...')
  test_q1()
  print('Testing Q2 ...')
  test_q2()