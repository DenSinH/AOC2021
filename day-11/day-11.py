import numpy as np

with open("input.txt", "r") as f:
    octopi = np.array([[int(n) for n in line.strip()]for line in f.readlines()], dtype=np.int32)

count = 0
times = 0
while True:
    octopi += 1

    flashed = np.zeros(octopi.shape, dtype=bool)
    while np.count_nonzero(octopi > 9) > 0:
        flashes = octopi > 9
        octopi[flashes] = 0
        padded = np.pad(flashes, pad_width=((1, 1), (1, 1)), constant_values=False)
        flashed = np.logical_or(flashed, flashes)
        for amt0 in range(-1, 2):
            for amt1 in range(-1, 2):
                if amt0 or amt1:
                    rolled = np.roll(np.roll(padded, amt0, axis=0), amt1, axis=1)[1:octopi.shape[0] + 1, 1:octopi.shape[1] + 1]
                    octopi[np.logical_and(np.logical_not(flashed), rolled)] += 1

    octopi[flashed] = 0
    if times < 100:
        count += np.count_nonzero(flashed)

    times += 1
    if times == 100:
        print(count)
    elif np.count_nonzero(flashed) == octopi.size:
        print(times)
        break
