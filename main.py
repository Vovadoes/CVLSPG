import math

# from Charts import *


# from scipy.stats import t

# CONST
pi = 3.14159265
Yc = 17.3 * (10 ** -6)

dct_sip = {
        16: 1.19 / 1000,
        25: 1.2 / 1000,
        35: 0.868 / 1000,
        50: 0.641 / 1000,
        70: 0.443 / 1000,
        95: 0.320 / 1000,
        120: 0.253 / 1000
    }


def myround(x: float, lst: list):
    for i in lst:
        if x < i:
            return i
    return lst[-1]


class Calculation:
    def __init__(self, n: int, m: int, k: int, lst: list, U1: float, nl: float, cos_fi: float, P_kpd: float,
                 q: float, U2: float):
        global dct_sip
        P_i = P_kpd / n

        lst_P = []
        for i in range(m):
            lst_P.append(lst[i][1] * P_i)
        print(f"{lst_P=}")

        lst_I = []
        for i in range(m):
            lst_I.append(lst_P[i] / (U1 * cos_fi))
        print(f"{lst_I=}")

        dU = nl * U1 * 10
        print(f"{dU=}")

        lst_R = []
        for i in range(m):
            lst_R.append(dU / lst_I[i])
        print(f"{lst_R=}")

        self.lst_S = []
        for i in range(m):
            self.lst_S.append(q * lst[i][2] / lst_R[i])
        print(f"{self.lst_S=}")

        self.lst_S_gost = [
            myround(self.lst_S[i], [16, 25, 35, 50, 70, 95, 120])
            for i in range(len(self.lst_S))
        ]
        print(f"{self.lst_S_gost=}")

        self.lst_R_new = [lst[i][2] * dct_sip[self.lst_S_gost[i]] for i in range(m)]
        print(f"{self.lst_R_new=}")

        self.lst_I_new = [1000 * lst_P[i] / (k * U2) for i in range(m)]
        print(f"{self.lst_I_new=}")

        self.lst_Un = [self.lst_R_new[i] * self.lst_I_new[i] for i in range(m)]
        print(f"{self.lst_Un=}")

        self.lst_Uv = [U2 - self.lst_Un[i] for i in range(m)]
        print(f"{self.lst_Uv=}")


if __name__ == "__main__":
    n = 96
    m = 7
    lst = [
        ["1", 62, 350, 4],
        ["2", 34, 390, 4],
        ["3", 12, 120, 4],
        ["4", 18, 172, 4],
        ["5", 20, 200, 4],
        ["6", 8, 80, 4],
        ["7", 14, 120, 4],
    ]
    U1 = 0.4
    nl = 5
    cos_fi = 0.95
    P_kpd = 80
    q = 0.028

    k = 3
    U2 = 240

    calculation = Calculation(n, m, k, lst, U1, nl, cos_fi, P_kpd, q, U2)

    # ChartLinePLT(calculation.chart_v_y_data)
    # plt.legend()
    # plt.show()
