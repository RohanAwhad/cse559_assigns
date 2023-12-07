"""
[Viterbi Algorithm - 60pt] Implement the Viterbi Algorithm for finding the most likely sequence of hidden states π, where P r(x, π) is maximized.
Input: An observed sequence of symbols x, followed by alphabet Σ, followed by a list of states states, followed by transition matrix T, followed by emission matrix E of an HMM (Σ,states,T,E).
Output: The sequence of hidden states that maximizes P r(x, π).

Note: Assume initial probabilities are equally likely. Remember to compute probabilities in log space to prevent any underflow errors resulting in probabilities of zero.
"""
import os

TESTING = os.getenv("TESTING", False)


def get_matrix(matrix_str):
  matrix_str = matrix_str.strip()
  # Split by newline characters to get rows
  rows = matrix_str.split("\n")

  matrix = {}
  cols = [x.strip() for x in rows[0].strip().split() if x]
  for row in rows[1:]:
    values = row.split()
    state = values[0]
    probabilities = [float(value) for value in values[1:]]
    matrix[state] = dict(zip(cols, probabilities))

  return matrix


def parse_inp(inp_str):
  x, sigma, states, transition_mat_str, emission_mat_str = inp_str.split(
    "\n--------\n"
  )
  obs = list(x)
  states = [x for x in states.split() if x]
  transition_matrix = get_matrix(transition_mat_str)
  emission_matrix = get_matrix(emission_mat_str)

  return (
    obs,
    sigma,
    states,
    transition_matrix,
    emission_matrix,
  )


def viterbi(obs, states, start_p, trans_p, emit_p):
  V = [{}]
  path = {}

  # Initialize base cases (t == 0)
  for state in states:
    V[0][state] = start_p[state] * emit_p[state][obs[0]]
    path[state] = [state]

  # Run Viterbi for t > 0
  for t in range(1, len(obs)):
    V.append({})
    newpath = {}

    for cur_state in states:
      # Check if state is reachable (probability > 0)
      max_prob, prev_st = max(
        (
          V[t - 1][prev_state]
          * trans_p[prev_state][cur_state]
          * emit_p[cur_state][obs[t]],
          prev_state,
        )
        for prev_state in states
        if V[t - 1][prev_state] > 0
      )

      V[t][cur_state] = max_prob
      newpath[cur_state] = path[prev_st] + [cur_state]

    # Don't need to remember old paths
    path = newpath

  max_prob = max(value for value in V[-1].values())

  # Find the most probable state and its backtrack
  most_probable_state = max(V[-1], key=V[-1].get)
  return path[most_probable_state]


def main(inp_str):
  inp = parse_inp(inp_str)
  obs, sigma, states, transition_mat, emission_mat = inp
  start_prob = 1 / len(states)
  start_prob = {state: start_prob for state in states}
  path = viterbi(obs, states, start_prob, transition_mat, emission_mat)
  return "".join(path)


if __name__ == "__main__":
  if TESTING:
    DEBUG_DIR = "1_Viterbi_Algo/Debugging"
    for i in range(1, 4):
      with open(f"{DEBUG_DIR}/inputs/input_{i}.txt") as f:
        sample_inp = f.read().strip()
      act = main(sample_inp)
      with open(f"{DEBUG_DIR}/outputs/output_{i}.txt", "r") as f:
        exp = f.read().strip()
      assert act == exp, f"Failed test {i}. Expected: {exp}, Actual: {act}"

  with open("test_1.txt") as f:
    sample_inp = f.read().strip()
  path = main(sample_inp)
  with open("output_q1_rohan_awhad.txt", "w") as f:
    f.write(path)
