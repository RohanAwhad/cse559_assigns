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

def lloyd_algorithm(k, data_points):
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
      if cluster:
        new_center = [sum(coords) / len(coords) for coords in zip(*cluster)]
      else:
        new_center = random.choice(data_points)
      new_centers.append(new_center)

    # Check for convergence (if centers do not change)
    if centers == new_centers:
      break
    else:
      centers = new_centers

  return centers


# Example usage
k, m = 3, 2  # 3 clusters, 2 dimensions
data_points = [[1, 2], [1, 4], [1, 0],
         [10, 2], [10, 4], [10, 0],
         [20, 2], [20, 4], [20, 0]]  # Example data points

# Run Lloyd's algorithm
centers = lloyd_algorithm(k, data_points)

# pretty print
for centroid in centers:
  for i in range(m): print(centroid[i], end=" ")
  print()
