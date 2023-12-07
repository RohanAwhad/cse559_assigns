"""
[Baum-Welch Learning for HMM - 60pt] (OPTIONAL for CSE494) Implement Baum-Welch algorithm to learn the unknown parameters of HMM. You will need soft decoding of both nodes and edges in Viterbi graph (node soft decoding done in the previous problem).
Input: A number of iterations i, followed by an observed sequence of symbols x, followed by alphabet Σ, followed by a list of states states, followed by initial transition matrix T, followed by emissions matrix E.
Output: Transition matrix followed by emission matrix that maximize Pr(x,Π) over all possible Π and parameters (transition and emission matricies).

Note: Assume initial probabilities are equally likely. Remember to compute probabilities in log space to prevent any underflow errors resulting in probabilities of zero.
"""
import os

TESTING = os.getenv("TESTING", False)

import math


def log_sum_exp(a, b):
    """Utility for stable log sum exp calculation."""
    return max(a, b) + math.log1p(math.exp(-abs(a - b)))


def forward_log(obs, states, start_p, trans_p, emit_p):
    fwd = [{}]
    for state in states:
        fwd[0][state] = math.log(start_p[state]) + math.log(emit_p[state][obs[0]])

    for i in range(1, len(obs)):
        fwd.append({})
        for st in states:
            log_prob_sum = -math.inf
            for st_prev in states:
                log_prob = (
                    fwd[i - 1][st_prev]
                    + math.log(trans_p[st_prev][st])
                    + math.log(emit_p[st][obs[i]])
                )
                log_prob_sum = log_sum_exp(log_prob_sum, log_prob)
            fwd[i][st] = log_prob_sum
    return fwd


def backward_log(obs, states, trans_p, emit_p):
    bkw = [{} for _ in range(len(obs))]
    for state in states:
        bkw[-1][state] = 0  # log(1)

    for i in range(len(obs) - 2, -1, -1):
        for st in states:
            log_prob_sum = -math.inf
            for next_st in states:
                log_prob = (
                    math.log(trans_p[st][next_st])
                    + math.log(emit_p[next_st][obs[i + 1]])
                    + bkw[i + 1][next_st]
                )
                log_prob_sum = log_sum_exp(log_prob_sum, log_prob)
            bkw[i][st] = log_prob_sum

    return bkw


def compute_posterior_log(obs, states, start_p, trans_p, emit_p):
    fwd = forward_log(obs, states, start_p, trans_p, emit_p)
    bkw = backward_log(obs, states, trans_p, emit_p)

    posterior = []
    for i in range(len(obs)):
        posterior_i = {}
        norm = -math.inf
        for st in states:
            norm = log_sum_exp(norm, fwd[i][st] + bkw[i][st])
        for st in states:
            posterior_i[st] = math.exp(fwd[i][st] + bkw[i][st] - norm)
        posterior.append(posterior_i)

    return posterior


def baum_welch_log(obs, states, start_p, trans_p, emit_p, iterations):
    for _ in range(iterations):
        fwd = forward_log(obs, states, start_p, trans_p, emit_p)
        bkw = backward_log(obs, states, trans_p, emit_p)

        # E-step: Calculate expected occurrences of transitions and emissions
        gamma = compute_posterior_log(obs, states, start_p, trans_p, emit_p)
        xi = []
        for t in range(len(obs) - 1):
            xi_t = {}
            norm = -math.inf
            for i in states:
                xi_t[i] = {}
                for j in states:
                    log_prob = (
                        fwd[t][i]
                        + math.log(trans_p[i][j])
                        + math.log(emit_p[j][obs[t + 1]])
                        + bkw[t + 1][j]
                    )
                    norm = log_sum_exp(norm, log_prob)
            for i in states:
                for j in states:
                    log_prob = (
                        fwd[t][i]
                        + math.log(trans_p[i][j])
                        + math.log(emit_p[j][obs[t + 1]])
                        + bkw[t + 1][j]
                    )
                    xi_t[i][j] = math.exp(log_prob - norm)
            xi.append(xi_t)

        # M-step: Update model parameters
        # Update transition probabilities
        for i in states:
            for j in states:
                numerator = sum(xi[t][i][j] for t in range(len(obs) - 1))
                denominator = sum(gamma[t][i] for t in range(len(obs) - 1)) + 1e-10
                trans_p[i][j] = numerator / denominator

        # Update emission probabilities
        for st in states:
            for symbol in obs:
                numerator = sum(
                    gamma[t][st] for t in range(len(obs)) if obs[t] == symbol
                )
                denominator = sum(gamma[t][st] for t in range(len(obs))) + 1e-10
                emit_p[st][symbol] = numerator / denominator

    return trans_p, emit_p


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


def main(inp_str):
    inp = parse_inp(inp_str)
    n_iters, obs, sigma, states, transition_mat, emission_mat = inp
    start_prob = 1 / len(states)
    start_prob = {state: start_prob for state in states}
    # Run the Baum-Welch algorithm using log space
    optimized_trans_p, optimized_emit_p = baum_welch_log(
        obs, states, start_prob, transition_mat, emission_mat, n_iters
    )

    # format transition matrix for output
    next_rows = ["\t".join(states)]
    for state in states:
        next_rows.append(
            "\t".join(
                [
                    state,
                ]
                + [f"{optimized_trans_p[state][x]:0.3f}" for x in states]
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
                + [f"{optimized_emit_p[state][x]:0.3f}" for x in sigma]
            )
        )
    ret = "\n".join(next_rows)
    return ret


if __name__ == "__main__":
    if TESTING:
        DEBUG_DIR = "4_BW_Learning_for_HMM/Debugging"
        for i in range(1, 4):
            with open(f"{DEBUG_DIR}/inputs/input_{i}.txt") as f:
                sample_inp = f.read().strip()
            act = main(sample_inp)
            with open(f"{DEBUG_DIR}/outputs/output_{i}.txt", "r") as f:
                exp = f.read().strip()
            try:
                assert act == exp
            except:
                print(f"Failed test {i}. Expected:\n{exp}\nActual:\n{act}")

    with open("test_1.txt") as f:
        sample_inp = f.read().strip()
    path = main(sample_inp)
    with open("output_q4_rohan_awhad.txt", "w") as f:
        f.write(path)
