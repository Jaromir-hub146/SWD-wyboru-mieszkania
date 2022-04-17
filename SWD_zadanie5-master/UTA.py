""" ....... """


import numpy as np
from mieszkania import B, v, weight, przedz
'''
# TODO
1. Zapytać o dobód wartości uźyteczności do poszczególnych kryteriów
2. Uwzglednic ewentualne wagi
'''


def _dic2matrix(dict_):
    """
    zamiana słownika na macierz numpy
    """
    keys = list(dict_.keys())
    arr = dict_[keys[0]]
    for key in keys[1:]:
        arr = np.vstack([arr, dict_[key]])
    return arr, keys


def _get_max(matrix):
    '''
    funkcja zwraca maksima w macierzy
    '''
    return np.max(matrix, axis=0)


def _get_min(matrix):
    '''
    funkcja zwraca minima w macierzy
    '''
    return np.min(matrix, axis=0)


def podz_kryt(matrix, przedz, v):
    '''
    funkcja zwacajaca podzial punktów posrednich poszczegolnych kryteriow na rowne odleglosci
    '''

    min_el = _get_min(matrix)
    max_el = _get_max(matrix)
    pkt_posrednie = []
    for i in range(len(min_el)):
        res = max_el[i] - min_el[i]
        res = res / (przedz[i] - 1)
        temp = []
        for j in range(przedz[i]):
            if v[i] == 1:
                next_el = max_el[i] - res * j
            else:
                next_el = min_el[i] + res * j
            temp.append(next_el)
        pkt_posrednie.append(temp)
    return pkt_posrednie


def _get_ideal(matrix, v):
    '''
    funkcja obliczjaca punkty idealne
    '''
    ideal = []
    for i in range(len(v)):
        if v[i] == 0:
            ideal.append(np.min(matrix[:, i]))
        else:
            ideal.append(np.max(matrix[:, i]))
    return ideal


def _get_aideal(matrix, v):
    '''
    funkcja obliczjaca punkty antyidealne
    '''
    aideal = []
    for i in range(len(v)):
        if v[i] == 1:
            aideal.append(np.min(matrix[:, i]))
        else:
            aideal.append(np.max(matrix[:, i]))
    return aideal


def _get_utility_f_val(przedz, weight):
    x = 1 / np.sum(weight)
    utility_vals = []
    for i, w in enumerate(weight):
        temp = []
        r = (x * w) / (przedz[i] - 1)
        for j in range(przedz[i]):
            temp.append(x * w - j * r)
        utility_vals.append(temp)
    return utility_vals


def wsp_aib(p_posr, v_util):
    wsp = []
    for i in range(len(p_posr)):
        p = p_posr[i]
        u = v_util[i]
        p1 = p[0]
        u1 = u[0]
        temp = []
        for j in range(1, len(p)):
            p2 = p[j]
            u2 = u[j]
            a = (u1 - u2) / (p1 - p2)
            b = u1 - a * p1
            temp.append((a, b))
        wsp.append(temp)
    return wsp


def _get_score_1cryt(u1, wsp_u1, podz_u1, isMax):
    scores = []
    for u in u1:
        for j, pkt in enumerate(podz_u1):
            if isMax and u <= pkt:
                score = wsp_u1[j - 1][0] * u + wsp_u1[j - 1][1]
                scores.append(score)
                break
            if u >= pkt and not isMax:
                score = wsp_u1[j - 1][0] * u + wsp_u1[j - 1][1]
                scores.append(score)
                break
    return scores


def skoring(matrix, wsp, pkt_posrednie, v):
    u = []
    for i in range(len(matrix[1])):
        ui = matrix[:, i]
        wsp_ui = wsp[i]
        podz_ui = pkt_posrednie[i]
        isMax = True if v[i] == 1 else False
        scores = _get_score_1cryt(ui, wsp_ui, podz_ui, isMax)
        u.append(scores)
    return np.array(u)


def ranking(u, keys):
    results = np.sum(u.T, axis=1)
    ranks = list(zip(keys, results))
    ranks.sort(key=lambda x: x[1], reverse=True)
    return ranks


def UTA(B, weight, przedz, v, consider):
    arr, keys = _dic2matrix(B)
    if consider:
        for col in consider:
            np.delete(arr, col, axis=1)
            keys.pop(col)
    pkt_posrednie = podz_kryt(arr, przedz, v)
    utility_vals = _get_utility_f_val(przedz, weight)
    wsp = wsp_aib(pkt_posrednie, utility_vals)
    u = skoring(arr, wsp, pkt_posrednie, v)
    ranks = ranking(u, keys)
    print("|Ranking|Nazwa\t|Wynik\t\t\t|")
    for i in range(len(ranks)):
        print(f"|{i + 1}\t|{ranks[i][0]}\t|{ranks[i][1]}\t|")
    return ranks


if __name__ == '__main__':
    # print(len(B['M8']))
    # print(len(weight))
    # print(len(przedz))
    # print(len(v))
    ranks = UTA(B, weight, przedz, v)
    print(ranks)
