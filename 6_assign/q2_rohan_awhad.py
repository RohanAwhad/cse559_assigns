"""
[K-means clustering (soft) via Expectation-Maximization (EM) algorithm - 40 pt] This
approach for K-means clustering uses soft assignment based on what each data point’s responsibility
for each cluster. During the centers-to-clusters step, instead of assigning each data point to a single
center, we need to compute the responsibility for each center. More precisely, given n data points
(Data1 . . . Datan) and k centers (x1 . . . xk), we need to construct a k × n HiddenMatrix, where an
entry HiddenM atrixi,j is j-th data point’s responsibility to be in i-th center. In order to compute
this responsibility, instead of using Newtonian gravitational pull-based formulation, we will use the
partition function from statistical physics:
HiddenM atrixi,j = e−β·d(Dataj ,xi)
∑
allcentersxi e−β·d(Dataj ,xi) ,
where β is the stiffness parameter that refelect the amount of flexibility in soft assignment.
During the clusters-to-centers step, you can use the corresponding row vector of HiddenM atrix for
updating center xi. The corresponding row vector for cetner xi is HiddenM atrixi which is the i-th
row of the matrix. To obtain the new and updated j-th coordinate of xi can be computed using:
xi,j = HiddenM atrixi · Dataj
HiddenM atrixi · −→
1 ,
where Dataj is the n-dimensional vector holding the j-th coordinates of the n points in Data.

> Input: The first line contains two integers k and m where k is the number of clusters, and m is
the number of dimensions for given data points. The second line contains the value for the stiffness
parameter β. Each subsequent line contains ordered m numbers where each representing a coordinate
value for a dimension of a data point in Euclidean space.

> Output: k centers obtained from running soft clustering via EM algorithm – k lines (one for each
center), each containing m coordinate values for the center
"""
import math
import random


def parse_inp(inp_str):
  '''
  Parse the input string into k and data_points

  sample string:
  7 5
  16.5 13.6 3.8 1.4 3.7
  8.9 0.3 7.7 21.1 3.6
  1.9 17.1 4.7 18.1 18.5
  7.9 2.3 6.7 13.7 11.3
  1.7 13.4 10.6 2.7 7.8
  2.1 11.4 2.0 0.7 0.5
  14.9 7.3 12.8 5.9 7.0
  6.2 3.0 6.4 15.3 11.6
  7.3 4.6 19.1 11.7 8.4
  '''

  lines = inp_str.split("\n")
  k, m = map(int, lines[0].split(" "))
  beta = float(lines[1])
  data_points = [list(map(float, line.split(" "))) for line in lines[2:]]
  return k, m, beta, data_points

def distance(point1, point2):
  """
  Calculates the Euclidean distance between two points.

  Args:
  point1 (list of float): The first point.
  point2 (list of float): The second point.

  Returns:
  float: The Euclidean distance between the two points.
  """
  return math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)))


def main(k, beta, data_points):
  """
  Implements the soft k-means clustering using Expectation-Maximization algorithm.

  Args:
  k (int): The number of clusters.
  beta (float): The stiffness parameter for soft assignment.
  data_points (list of list of float): The data points.

  Returns:
  list of list of float: The final centers of the clusters.
  """
  n = len(data_points)

  # Randomly initialize the centers
  centers = random.sample(data_points, k)

  while True:
    # Expectation step: Calculate the Hidden Matrix for responsibilities
    hidden_matrix = []
    for i in range(k):
      row = []
      for j in range(n):
        distance_ij = distance(data_points[j], centers[i])
        hidden_value = math.exp(-beta * distance_ij)
        row.append(hidden_value)
      hidden_matrix.append(row)

    # Normalize the Hidden Matrix row-wise
    row_sums = [sum(hidden_matrix[i]) for i in range(k)]
    hidden_matrix = [[hidden_matrix[i][j] / row_sums[i] for j in range(n)] for i in range(k)]

    # Maximization step: Update the centers
    new_centers = []
    for i in range(k):
      center = []
      for d in range(len(data_points[0])):
        center_d = sum(hidden_matrix[i][j] * data_points[j][d] for j in range(n)) / sum(hidden_matrix[i])
        center.append(center_d)
      new_centers.append(center)

    # Check for convergence (if centers do not change significantly)
    if all(distance(centers[i], new_centers[i]) < 1e-6 for i in range(k)): break
    else: centers = new_centers

  return centers



if __name__ == '__main__':
    # Example usage
    k, m = 3, 2  # 3 clusters, 2 dimensions
    beta = 2.0  # Example stiffness parameter
    data_points = [[1, 2], [1, 4], [1, 0],
                [10, 2], [10, 4], [10, 0],
                [20, 2], [20, 4], [20, 0]]  # Example data points

    # Run EM algorithm for soft k-means clustering
    centers = main(k, beta, data_points)
    print(centers)
