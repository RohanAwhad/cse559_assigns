# calculating burrows-wheeler transform
def bwt_encode(s):
    rotations = [s[i:] + s[:i] for i in range(len(s))]
    rotations.sort()
    ret = "".join([rotation[-1] for rotation in rotations])
    return ret


if __name__ == "__main__":
    with open("test_1.txt", "r") as f: s = f.read().strip()
    with open("output_q1_rohan_awhad.txt", "w") as f: f.write(bwt_encode(s))
