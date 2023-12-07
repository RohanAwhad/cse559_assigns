def log_sum_exp(a, b):
  """Helper function to compute log(sum(exp(a), exp(b))) safely"""
  return max(a, b) + math.log1p(math.exp(-abs(a - b)))


def log_forward(obs, states, start_p, trans_p, emit_p):
  log_fwd = [{}]
  for state in states:
    log_fwd[0][state] = math.log(start_p[state]) + math.log(emit_p[state][obs[0]])

  for i in range(1, len(obs)):
    log_fwd.append({})
    for st in states:
      log_sum = -math.inf
      for st_prev in states:
        print("log sum", log_sum)
        print(log_fwd[i - 1][st_prev])
        print(trans_p[st_prev][st])
        print(math.log(trans_p[st_prev][st] + 1e-10))
        log_sum = log_sum_exp(
          log_sum,
          log_fwd[i - 1][st_prev] + math.log(trans_p[st_prev][st] + 1e-10),
        )
      log_fwd[i][st] = log_sum + math.log(emit_p[st][obs[i]])

  return log_fwd


def log_backward(obs, states, trans_p, emit_p):
  log_bkw = [{} for _ in range(len(obs))]
  for state in states:
    log_bkw[-1][state] = 0  # log(1)

  for i in range(len(obs) - 2, -1, -1):
    for st in states:
      log_sum = -math.inf
      for next_st in states:
        log_sum = log_sum_exp(
          log_sum,
          math.log(trans_p[st][next_st] + 1e-10)
          + math.log(emit_p[next_st][obs[i + 1]])
          + log_bkw[i + 1][next_st],
        )
      log_bkw[i][st] = log_sum

  return log_bkw


def log_baum_welch(obs, states, start_p, trans_p, emit_p, iterations):
  for _ in range(iterations):
    log_fwd = log_forward(obs, states, start_p, trans_p, emit_p)
    log_bkw = log_backward(obs, states, trans_p, emit_p)

    # E-step: Calculate expected occurrences of transitions and emissions
    log_gamma = [
      {st: log_fwd[t][st] + log_bkw[t][st] for st in states}
      for t in range(len(obs))
    ]
    log_xi = []
    for t in range(len(obs) - 1):
      log_xi_t = {}
      log_norm = -math.inf
      for i in states:
        for j in states:
          log_norm = log_sum_exp(
            log_norm,
            log_fwd[t][i]
            + math.log(trans_p[i][j] + 1e-10)
            + math.log(emit_p[j][obs[t + 1]])
            + log_bkw[t + 1][j],
          )
      for i in states:
        log_xi_t[i] = {}
        for j in states:
          log_xi_t[i][j] = (
            log_fwd[t][i]
            + math.log(trans_p[i][j] + 1e-10)
            + math.log(emit_p[j][obs[t + 1]])
            + log_bkw[t + 1][j]
            - log_norm
          )
      log_xi.append(log_xi_t)

    # M-step: Update model parameters
    # Update transition probabilities
    for i in states:
      for j in states:
        log_numerator = -math.inf
        log_denominator = -math.inf
        for t in range(len(obs) - 1):
          log_numerator = log_sum_exp(log_numerator, log_xi[t][i][j])
          log_denominator = log_sum_exp(log_denominator, log_gamma[t][i])
        print(log_numerator, log_denominator)
        trans_p[i][j] = math.exp(log_numerator - log_denominator)

    # Update emission probabilities
    for st in states:
      for symbol in emit_p[st].keys():
        log_numerator = -math.inf
        log_denominator = -math.inf
        for t in range(len(obs)):
          if obs[t] == symbol:
            log_numerator = log_sum_exp(log_numerator, log_gamma[t][st])
          log_denominator = log_sum_exp(log_denominator, log_gamma[t][st])
        emit_p[st][symbol] = math.exp(log_numerator - log_denominator)

  return trans_p, emit_p
