from encode import max_value, color_seq
from math import ceil


# https://www.image-engineering.de/library/technotes/958-how-to-convert-between-srgb-and-ciexyz
def rgb_to_xyz(input_rgb):
    linear_rgb = [x / 3294.6 if x <= 10 else ((x / 255 + 0.055) / 1.055) ** 2.4 for x in input_rgb]

    X_D65 = 41.24564 * linear_rgb[0] + 35.75761 * linear_rgb[1] + 18.04375 * linear_rgb[2]
    Y_D65 = 21.26729 * linear_rgb[0] + 71.51522 * linear_rgb[1] + 7.21750 * linear_rgb[2]
    Z_D65 = 1.93339 * linear_rgb[0] + 11.91920 * linear_rgb[1] + 95.03041 * linear_rgb[2]
    return [X_D65, Y_D65, Z_D65]


# wikipedia
def foo(x):
    return x ** (1 / 3) if x > 216/24389 else ((x * (841/108)) + 4 / 29)


def xyz_to_lab(input_xyz):
    L = 116 * (foo(input_xyz[1] / 100)) - 16
    a = 500 * (foo(input_xyz[0] / 95.0489) - foo(input_xyz[1] / 100))
    b = 200 * (foo(input_xyz[1] / 100) - foo(input_xyz[2] / 108.8840))
    return [L, a, b]


def rgb_to_lab(input_rgb):
    return xyz_to_lab(rgb_to_xyz(input_rgb))


# returns SQUARE of delta e, not actually delta e
def delta_e(lab1, lab2):
    return (lab2[0] - lab1[0]) ** 2 + (lab2[1] - lab1[1]) ** 2 + (lab2[2] - lab1[2]) ** 2



def get_best_codex_for_delta_e(de, order=(0,1,2)):
    codex = [1, 1, 1]
    delta_e_val = de ** 2

    best = 0
    best_codex = [-1,-1,-1]
    while True:
        bases = [ceil(256 / num) for num in codex]
        max_num = max_value(bases, order)

        bad = False
        if max_num > best:
            colors = color_seq(1, codex, order)
            colors[0] = rgb_to_lab(colors[0])

            for i in range(2, max_num + 1):
                current_rgb = color_seq(i, codex, order)[0]
                current_lab = rgb_to_lab(current_rgb)

                for c in colors:
                    if delta_e(c, current_lab) < delta_e_val:
                        bad = True
                        break
                if not bad:
                    colors.append(current_lab)
                else:
                    break

        if max_num > best and not bad:
            #print(f"WORKS!!!\n{codex}\nmax: {max_num}", flush=True)
            best = max_num
            best_codex=list(codex)

        else:
            if codex[0] == 255:
                codex[0] = 1
                if codex[1] == 255:
                    codex[1] = 1
                    if codex[2] == 255:
                        #print("end", flush=True)
                        return best_codex
                    else:
                        codex[2] += 1
                        #if max_num <= best and not bad:
                            #print(f"\nget better. L.\n{codex}", flush=True)
                        #else:
                            #print(f"\nruh roh\n{codex}", flush=True)
                else:
                    codex[1] += 1
            else:
                codex[0] += 1


if __name__=="__main__":
    from concurrent.futures import ProcessPoolExecutor

    test_deltas=[8.971916,11.3191,18.94112,10.18343]

    with ProcessPoolExecutor(4) as exe:
        # perform calculations
        results = exe.map(get_best_codex_for_delta_e, test_deltas)

    for i,r in enumerate(results):

        bases = [ceil(256 / num) for num in r]
        max_num = max_value(bases, [0,1,2])

        print(f"optimal codex for {test_deltas[i]} Delta E = {r}", flush=True)
        print(f"max num possible for {r} codex = {max_num}\n", flush=True)


