"""
Parameter Estimation via Viterbi Learning - 60pt] Implement Viterbi Learning algorithm to estimate the unknown parameters of HMM to maximize Pr(x,π) over all possible parameter sets.
Input: A number of iterations i, followed by an observed sequence of symbols x, followed by alphabet Σ, followed by a list of states states, followed by initial transition matrix T, followed by emissions matrix E.
Output: Transition matrix followed by emission matrix that maximizes Pr(x,Π) over all Π and parameters (transition and emission matrices).

Note: Assume initial probabilities are equally likely. Remember to compute probabilities in log space to prevent any underflow errors resulting in probabilities of zero.
"""
import os
from collections import defaultdict

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
    n_iters, x, sigma, states, transition_mat_str, emission_mat_str = inp_str.split(
        "\n--------\n"
    )
    n_iters = int(n_iters.strip())
    obs = list(x)
    sigma = [x for x in sigma.strip().split() if x]
    states = [x for x in states.split() if x]
    transition_matrix = get_matrix(transition_mat_str)
    emission_matrix = get_matrix(emission_mat_str)

    return (
        n_iters,
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


def update_transition_matrix(transition_probs, path):
    transition_probs = defaultdict(lambda: defaultdict(int))
    for i in range(len(path) - 1):
        transition_probs[path[i]][path[i + 1]] += 1

    # transition_probs /= transition_probs.sum(axis=1, keepdims=True)
    for x in transition_probs:
        total = sum(transition_probs[x].values())
        for y in transition_probs[x]:
            transition_probs[x][y] /= total

    return transition_probs


def update_emission_matrix(emission_probs, path, obs):
    emission_probs = defaultdict(lambda: defaultdict(int))
    for i in range(len(path)):
        emission_probs[path[i]][obs[i]] += 1

    # emission_probs /= emission_probs.sum(axis=1, keepdims=True)
    for x in emission_probs:
        total = sum(emission_probs[x].values())
        for y in emission_probs[x]:
            emission_probs[x][y] /= total
    return emission_probs


def main(inp_str):
    inp = parse_inp(inp_str)
    n_iters, obs, sigma, states, transition_mat, emission_mat = inp
    start_prob = 1 / len(states)
    start_prob = {state: start_prob for state in states}

    for _ in range(n_iters):
        path = viterbi(obs, states, start_prob, transition_mat, emission_mat)
        transition_mat = update_transition_matrix(transition_mat, path)
        emission_mat = update_emission_matrix(emission_mat, path, obs)

    # format transition matrix for output
    next_rows = ["\t".join(states)]
    for state in states:
        next_rows.append(
            "\t".join(
                [
                    state,
                ]
                + [f"{transition_mat[state][x]:0.3f}" for x in states]
            )
        )

    next_rows.append("--------")
    next_rows.append("\t".join(sigma))
    for state in states:
        next_rows.append(
            "\t".join(
                [
                    state,
                ]
                + [f"{emission_mat[state][x]:0.3f}" for x in sigma]
            )
        )
    return "\n".join(next_rows)


if __name__ == "__main__":
    if TESTING:
        DEBUG_DIR = "2_Parameter_Estimation_via_Viterbi_Learning/Debugging"
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
    with open("output_q2_rohan_awhad.txt", "w") as f:
        f.write(path)
