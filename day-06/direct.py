import numpy as np
from collections import Counter

np.set_printoptions(linewidth=999999)

M = np.array(
   [[0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0]]
)

# counts
with open("input.txt", "r+") as f:
    input = np.zeros(9)
    for v, c in Counter(int(n) for n in f.readline().split(",")).most_common():
        input[v] = c

# convert to vector of f_{k, n}s
F0 = np.roll(input[::-1], 1)
F0[3:9] -= F0[1:7]
F0[5:9] += F0[1:5]

# product with matrix
w, C = np.linalg.eig(M)
D = np.diag(w)
Fn = (C @ (D ** 256) @ np.linalg.inv(C)).dot(F0)

# convert back into f_{k, n}
Fn[3:9] += Fn[1:7]
print(round(np.sum(Fn).real))