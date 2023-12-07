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
