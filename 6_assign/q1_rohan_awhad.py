"""
[K-means clustering (hard) via Lloyd Algorithm - 60pt] Implement the Lloyd Algorithm which
uses iterative approach to obtain heuristic-based solutions for K-mean clustering. Recall that Lloyd
algorithm uses two steps: (1) centers-to-clusters and (2) clusters-to-centers iteratively until
convergence. Assume that the algorithm has converged if the centers do not change between iterations.

> Input: The first line contains two integers k and m where k is the number of clusters, and m is the
number of dimensions for given data points. Each subsequent line contains ordered m numbers where
each representing a coordinate value for a dimension of a data point in Euclidean space.

> Output: k centers obtained from running Lloyd algorithm – k lines (one for each center), each con-
taining m coordinate values for the center
"""
import random
import math

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
  k, _ = map(int, lines[0].split(" "))
  data_points = [list(map(float, line.split(" "))) for line in lines[1:]]
  return k, data_points

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

def main(k, data_points):
  """
  Implements the Lloyd algorithm for hard k-means clustering.

  Args:
  k (int): The number of clusters.
  m (int): The number of dimensions for the data points.
  data_points (list of list of float): The data points.

  Returns:
  list of list of float: The final centers of the clusters.
  """
  # Initialize centers randomly
  centers = random.sample(data_points, k)

  while True:
    # Assign each point to the closest center
    clusters = [[] for _ in range(k)]
    for point in data_points:
      distances = [distance(point, center) for center in centers]
      closest_center = min(range(k), key=lambda i: distances[i])
      clusters[closest_center].append(point)

    # Update the centers to be the mean of the points in each cluster
    new_centers = []
    for cluster in clusters:
      if cluster: new_center = [sum(coords) / len(coords) for coords in zip(*cluster)]
      else: new_center = random.choice(data_points)
      new_centers.append(new_center)

    # Check for convergence (if centers do not change)
    if centers == new_centers: break
    else: centers = new_centers

  return centers


def pretty_print(centers):
  ret = ""
  for centroid in centers:
    for i in range(len(centroid)): ret += f'{centroid[i]:.3f} '
    ret += "\n"
  return ret

if __name__ == '__main__':
  with open("test_1.txt") as f: sample_inp = f.read().strip()
  k, data_points = parse_inp(sample_inp)
  centers = main(k, data_points)
  output = pretty_print(centers)
  with open("output_q1_rohan_awhad.txt", "w") as f: f.write(output)
