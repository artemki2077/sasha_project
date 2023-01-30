from random import random
from PIL import Image as Im
from math import exp as e


class Neiron():
    def active(self, inputs, weights):
        self.activator = sum([inputs[i] * weights[i] for i in range(len(inputs))])
        return self.func(self.activator)

    def func(self, activator):
        return 1 / (1 + e(-activator))


class Grid():
    def build(self, inp, neirons, out, weights):
        self.n_grid = [[0 for t in range(inp)]] + [[Neiron() for i1 in range(neirons[i])] for i in range(len(neirons))] + [[Neiron() for j in range(out)]]
        self.w = weights
        self.anss = 0

    def start(self, inp):
        t_n = [inp]
        for column in range(1, len(self.n_grid)):
            ans = []
            for neiron in range(len(self.n_grid[column])):
                t_neiron = self.n_grid[column][neiron]
                ans.append(t_neiron.active(t_n[column - 1], self.w[column - 1][neiron]))
            t_n.append(ans)
        self.anss = t_n
        return t_n[-1][0]

    def learn(self, filename):
        with open(filename) as f:
            weights = [[[float(k) for k in j.split(' ')] for j in i.split('\n')] for i in f.read().split('\n\n')]
        self.w = weights


def part(i, j, size):
    global g_image
    return [_1 for _0 in [_[j: j + size] for _ in g_image[i: i + size]] for _1 in _0]


def randweight(inp, neirons, out):
    ans = [[[int(random() * 1000) / 1000 - 0.5 for j in range(inp)] for i in range(neirons[0])]]
    ans += [[[int(random() * 1000) / 1000 - 0.5 for _ in range(neirons[i - 1])] for j in range(neirons[i])] for i in range(1, len(neirons))]
    ans += [[[int(random() * 1000) / 1000 - 0.5 for j in range(neirons[-1])] for i in range(out)]]
    return ans


def good_image(src):
    im = Im.open(src)
    pixels = im.load()
    x, y = im.size
    g_image = [[0] * (x + 100) for _ in range(50)]
    for j in range(y):
        t_n = []
        for i in range(x):
            r, g, b = pixels[i, j]
            white_black = (r + g + b) // 3
            t_n.append(int(white_black / 255 * 1000) / 1000)
        g_image.append([0] * 50 + t_n + [0] * 50)
    g_image += [[0] * (x + 100) for _ in range(50)]
    # need corect
    t_n = [j for i in g_image for j in i]
    if sum(t_n) / len(t_n) < 30:
        return g_image
    return 'not stars sky'


BASE = [25, [4], 1]
weights = randweight(*BASE)
N_N5 = Grid()
N_N5.build(*BASE, weights)

BASE = [100, [7], 1]
weights = randweight(*BASE)
N_N10 = Grid()
N_N10.build(*BASE, weights)

BASE = [900, [15], 1]
weights = randweight(*BASE)
N_N30 = Grid()
N_N30.build(*BASE, weights)

BASE = [2500, [20, 5], 1]
weights = randweight(*BASE)
N_N50 = Grid()
N_N50.build(*BASE, weights)

N_N5.learn('weights/for_5')
N_N10.learn('weights/for_10')
N_N30.learn('weights/for_30')
N_N50.learn('weights/for_50')


def count_stars(src):
    global g_image
    count = 0
    g_image = good_image(src)
    if type(g_image) == int:
        l_g = len(g_image)
        l_g0 = len(g_image[0])
        for i in range(0, l_g, 2):
            for j in range(0, l_g0, 2):
                if i + 5 < l_g and j + 5 < l_g0:
                    if N_N5.start(part(i, j, 5)) >= 0.7:
                        count += 1
                if i + 10 < l_g and j + 10 < l_g0 and i % 4 == 0 and j % 4 == 0:
                    if N_N10.start(part(i, j, 10)) >= 0.7:
                        count += 1
                if i + 30 < l_g and j + 30 < l_g0 and i % 15 == 0 and j % 15 == 0:
                    if N_N30.start(part(i, j, 30)) >= 0.7:
                        count += 1
                if i + 50 < l_g and j + 50 < l_g0 and i % 20 == 0 and j % 20 == 0:
                    if N_N50.start(part(i, j, 50)) >= 0.7:
                        count += 1
        return count
    else:
        return g_image


if __name__ == '__main__':
    count = 0
    g_image = good_image('files/photos/file_0.jpg')
    l_g = len(g_image)
    l_g0 = len(g_image[0])
    for i in range(0, l_g, 2):
        for j in range(0, l_g0, 2):
            if i + 5 < l_g and j + 5 < l_g0:
                if N_N5.start(part(i, j, 5)) >= 0.7:
                    count += 1
            if i + 10 < l_g and j + 10 < l_g0 and i % 4 == 0 and j % 4 == 0:
                if N_N10.start(part(i, j, 10)) >= 0.7:
                    count += 1
            if i + 30 < l_g and j + 30 < l_g0 and i % 15 == 0 and j % 15 == 0:
                if N_N30.start(part(i, j, 30)) >= 0.7:
                    count += 1
            if i + 50 < l_g and j + 50 < l_g0 and i % 20 == 0 and j % 20 == 0:
                if N_N50.start(part(i, j, 50)) >= 0.7:
                    count += 1
    print(count)