cimport cython

cpdef list get_motifs_from_profile(
  list dna_strings,
  double[:] a_probs,
  double[:] c_probs,
  double[:] t_probs,
  double[:] g_probs,
):
  
  cdef int k
  cdef list motif_set = []
  cdef str kmer
  cdef str dna

  k = len(a_probs)
  cdef int i
  for i in range(len(dna_strings)):
  #for dna in dna_strings:
    dna = dna_strings[i]
    kmer = _select_kmer(
      k,
      dna,
      a_probs,
      c_probs,
      t_probs,
      g_probs,
    )
    motif_set.append(kmer)

  return motif_set


# most slow; cythonizing this on priority
cdef str _select_kmer(
  int k,
  str dna,
  double[:] a_probs,
  double[:] c_probs,
  double[:] t_probs,
  double[:] g_probs,
):
  cdef double max_prob = 0.0
  cdef int max_start = -1

  cdef double kmer_prob
  cdef int start
  cdef int i
  cdef str x
  cdef str s

  cdef str A_s, T_s, C_s, G_s
  A_s = "A"
  C_s = "C"
  T_s = "T"
  G_s = "G"


  for start in range(len(dna)-k+1):
    kmer_prob = 1.0
    s = dna[start: start+k]

    for i in range(k):
      x = s[i]

      if x == A_s: kmer_prob *= a_probs[i]
      elif x == C_s: kmer_prob *= c_probs[i]
      elif x == T_s: kmer_prob *= t_probs[i]
      elif x == G_s: kmer_prob *= g_probs[i]

      if kmer_prob < max_prob: break

    if max_prob < kmer_prob:
      max_prob = kmer_prob
      max_start = start

  return dna[max_start: max_start+k]

