"""
Soft Decoding Problem - 60pt] Instead of finding the most likely hidden path, we want to find the conditional probability Pr(Πi = k | x) that the HMM was in hidden state k when emitting ith symbol (at step i).
Input: An observed sequence of symbols x = x1 ... xn, followed by alphabet Σ, followed by a list of states states, followed by transition matrix T, followed by emission matrix E of an HMM (Σ, states, T, E).
Output: All conditional probabilities P r(Πi = k | x) for each state k and each step i (1 to n)


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


def forward(obs, states, start_p, trans_p, emit_p):
    fwd = [{}]
    for state in states:
        fwd[0][state] = start_p[state] * emit_p[state][obs[0]]

    for i in range(1, len(obs)):
        fwd.append({})
        for st in states:
            fwd[i][st] = sum(
                fwd[i - 1][st_prev] * trans_p[st_prev][st] * emit_p[st][obs[i]]
                for st_prev in states
            )

    return fwd


def backward(obs, states, trans_p, emit_p):
    bkw = [{} for _ in range(len(obs))]
    for state in states:
        bkw[-1][state] = 1

    for i in range(len(obs) - 2, -1, -1):
        for st in states:
            bkw[i][st] = sum(
                trans_p[st][next_st] * emit_p[next_st][obs[i + 1]] * bkw[i + 1][next_st]
                for next_st in states
            )

    return bkw


def compute_posterior(obs, states, start_p, trans_p, emit_p):
    fwd = forward(obs, states, start_p, trans_p, emit_p)
    bkw = backward(obs, states, trans_p, emit_p)

    posterior = []
    for i in range(len(obs)):
        posterior_i = {}
        norm = sum(fwd[i][st] * bkw[i][st] for st in states)
        for st in states:
            posterior_i[st] = (fwd[i][st] * bkw[i][st]) / norm
        posterior.append(posterior_i)

    return posterior


def main(inp_str):
    inp = parse_inp(inp_str)
    obs, sigma, states, transition_mat, emission_mat = inp
    start_prob = 1 / len(states)
    start_prob = {state: start_prob for state in states}
    # Compute posterior probabilities
    posterior_probs = compute_posterior(
        obs, states, start_prob, transition_mat, emission_mat
    )
    posterior_probs_formatted = [[prob[x] for x in states] for prob in posterior_probs]
    rows = [" ".join(states)]
    for x in posterior_probs_formatted:
        rows.append(" ".join([f"{y}" for y in x]))
    return "\n".join(rows)


if __name__ == "__main__":
    if TESTING:
        DEBUG_DIR = "3_Soft_Decoding/Debugging"
        for i in range(1, 4):
            with open(f"{DEBUG_DIR}/inputs/input_{i}.txt") as f:
                sample_inp = f.read().strip()
            act = main(sample_inp)
            with open(f"{DEBUG_DIR}/outputs/output_{i}.txt", "r") as f:
                exp = f.read().strip()
            try:
                assert act == exp
            except:
                print(f"Failed test {i}. Expected: {exp}, Actual: {act}")

    with open("test_1.txt") as f:
        sample_inp = f.read().strip()
    path = main(sample_inp)
    with open("output_q3_rohan_awhad.txt", "w") as f:
        f.write(path)
