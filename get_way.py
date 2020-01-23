way = []
def main():
    lab = []
    n, m = list(map(int, input().split()))
    for i in range(n):
        rdl = input()
        stroka = []
        for k in range(len(rdl)):
            if int(rdl[k]) == 1:
                stroka.append(-1)
            else:
                stroka.append(int(rdl[k]))
        lab.append(stroka)
    x1, y1 = list(map(int, input().split()))
    x2, y2 = list(map(int, input().split()))
    lab = wave(x1, y1, 1, n, m, lab)
    if lab[x2][y2] > 0:
        for i in lab:
            print(*i)
        print("Mozhet")
        get_way(x2, y2, n, m, lab, lab[x2][y2])
        print(way)
    else:
        print("Ne mozhet")


def wave(x, y, cur, n, m, lab):
    lab[x][y] = cur
    if y + 1 < m:
        if lab[x][y + 1] == 0 or (lab[x][y + 1] != -1 and lab[x][y + 1] > cur):
            wave(x, y + 1, cur + 1, n, m, lab)
    if x + 1 < n:
        if lab[x + 1][y] == 0 or (lab[x + 1][y] != -1 and lab[x + 1][y] > cur):
            wave(x + 1, y, cur + 1, n, m, lab)
    if x - 1 >= 0:
        if lab[x - 1][y] == 0 or (lab[x - 1][y] != -1 and lab[x - 1][y] > cur):
            wave(x - 1, y, cur + 1, n, m, lab)
    if y - 1 >= 0:
        if lab[x][y - 1] == 0 or (lab[x][y - 1] != -1 and lab[x][y - 1] > cur):
            wave(x, y - 1, cur + 1, n, m, lab)
    return lab


def get_way(x, y, n, m, lab, cur):
    global way
    if y + 1 < m and lab[x][y + 1] + 1 == cur:
        way.append((0, 1))
        get_way(x, y + 1, n, m, lab, cur - 1)
    elif x + 1 < n and lab[x + 1][y] + 1 == cur:
        way.append((1, 0))
        get_way(x + 1, y, n, m, lab, cur - 1)
    elif x - 1 >= 0 and lab[x - 1][y] + 1 == cur:
        way.append((-1, 0))
        get_way(x - 1, y, n, m, lab, cur - 1)
    elif y - 1 >= 0 and lab[x][y - 1] + 1 == cur:
        way.append((0, -1))
        get_way(x, y - 1, n, m, lab, cur - 1)


main()
