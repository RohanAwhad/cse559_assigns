
def z_arr_to_lps_prime(z_arr):
  lps_prime = [0] * len(z_arr)
  for i, z in enumerate(z_arr):
  if z > 0: lps_prime[i+z-1] = z

  return lps_prime

if __name__ == '__main__':
  print(z_arr_to_lps_prime(
  list(map(int, "0003000"))
  ))
  print(z_arr_to_lps_prime(
  list(map(int, "001001001004000"))
  ))
  print(z_arr_to_lps_prime(
  list(map(int, "00000207000050000"))
  ))
