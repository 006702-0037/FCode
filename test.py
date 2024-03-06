import encode
from random import randint


def rgb_to_xyz(input_rgb):
    linear_rgb = [x / 3294.6 if x <= 10 else ((x / 255 + 0.055) / 1.055) ** 2.4 for x in input_rgb]

    X_D65 = 41.24564 * linear_rgb[0] + 35.75761 * linear_rgb[1] + 18.04375 * linear_rgb[2]
    Y_D65 = 21.26729 * linear_rgb[0] + 71.51522 * linear_rgb[1] + 7.21750 * linear_rgb[2]
    Z_D65 = 1.93339 * linear_rgb[0] + 11.91920 * linear_rgb[1] + 95.03041 * linear_rgb[2]
    return [X_D65, Y_D65, Z_D65]


# wikipedia
def foo(x):
    return x ** (1 / 3) if x > 216 / 24389 else ((x * (841 / 108)) + 4 / 29)


def xyz_to_lab(input_xyz):
    L = 116 * (foo(input_xyz[1] / 100)) - 16
    a = 500 * (foo(input_xyz[0] / 95.0489) - foo(input_xyz[1] / 100))
    b = 200 * (foo(input_xyz[1] / 100) - foo(input_xyz[2] / 108.8840))
    return [L, a, b]


def rgb_to_lab(input_rgb):
    return xyz_to_lab(rgb_to_xyz(input_rgb))


def delta_e(lab1, lab2):
    return ((lab2[0] - lab1[0]) ** 2 + (lab2[1] - lab1[1]) ** 2 + (lab2[2] - lab1[2]) ** 2) ** 0.5


data_pairs = []
with open("delta_e_new.csv", 'r') as delta_file:
    delta_e_data = delta_file.read().splitlines()[1:]
    for i in delta_e_data:
        url, de, max_num, r, g, b = i.split(",")
        data_pairs.append((float(de), int(max_num), [int(r), int(g), int(b)]))


trials_each=1000
def simulate(modifier):
    current = []
    global trials_each
    for k in range(trials_each):

        test_data = data_pairs[randint(0, len(data_pairs) - 1)]
        color_1 = encode.color_seq(randint(1, test_data[1] + 1), test_data[2], (0, 1, 2))[0]
        noise_color = [0, 0, 0]

        while delta_e(rgb_to_lab(color_1), rgb_to_lab(noise_color)) > test_data[0] * modifier:
            noise_color = [randint(0, 255), randint(0, 255), randint(0, 255)]

        best_color = []
        best_delta = 1000
        for i in range(1, test_data[1] + 1):
            code_color = encode.color_seq(i, test_data[2], (0, 1, 2))[0]
            if delta_e(rgb_to_lab(code_color), rgb_to_lab(noise_color)) < best_delta:
                best_delta = delta_e(rgb_to_lab(code_color), rgb_to_lab(noise_color))
                best_color = list(code_color)

        if best_color == color_1:
            current.append(1)
        else:
            current.append(0)

    return sum(current) / len(current)

if __name__ == "__main__":
    trials_each=1000
    runs=[0.5+0.1*x for x in range(25)]

    from concurrent.futures import ProcessPoolExecutor
    import matplotlib.pyplot as plt

    with ProcessPoolExecutor(32) as exe:
        results = exe.map(simulate, runs)

    plt.scatter(runs,list(results))
    plt.show()








