""" ....... """


from typing import List, Any, Dict, Callable, Tuple, Union
from numpy import vstack, amax, inf, amin
from mieszkania import B, v, weight, przedz
#from RSM import B2


def _normalize(matrix):
    """
    normalizacja macierzy
    """
    matrix = matrix / ((matrix ** 2).sum(axis=0)) ** (1 / 2)
    return matrix


def _apply_weights(matrix, weights):
    """
    zastosowanie wag kryteriów
    """
    return matrix * weights


def _apply_maxim(matrix, vector):
    """
    za pomocą wektora vector można określić które kryteria mają być
    maksymalizowane a które minimalizowane
    1 - maxymalizacja
    0 - minimalizacja
    """
    v2 = [1 if x == 0 else -1 for x in vector]
    print(matrix)
    print(matrix.shape)
    print(v2)
    matrix = matrix * v2
    matrix = matrix + vector
    return matrix


def _dic2matrix(dict_):
    """
    zamiana słownika na macierz numpy
    """
    keys = list(dict_.keys())
    arr = dict_[keys[0]]
    for key in keys[1:]:
        arr = vstack([arr, dict_[key]])
    return arr, keys


def _get_len(struct):
    return len(next(iter(struct.values())))


def _sort_res(ci: List[float], keys) -> List[Tuple[Any, ...]]:
    inp = list(zip(keys, ci))
    return sorted(inp, key=lambda x: x[1], reverse=True)


def _eukl_metr(matrix, max_, min_):
    """
    metryka euklidesowa dla macierzy z zadanymi max i min
    """
    max_odl = ((max_ - matrix) ** 2)
    min_odl = ((matrix - min_) ** 2)
    return min_odl, max_odl


def _get_did(matrix, metr, min_, max_):
    """
    zwraca parametry did i dig dla metody fuzzy topsis z zadanymi punktami min i max
    """
    dig_alm, did_alm = metr(matrix, max_, min_)
    dig = sum(dig_alm.T)
    did = sum(did_alm.T)
    return dig, did


def _get_ci(dig, did):
    """
    obliczenie parametru ci
    """
    return did / (did + dig)


def is_domi(x, y):
    """
    funkcja sprawdzająca czy dany punkt dominuje drugi
    :param x: pkt 1
    :param y: pkt 2
    :return: x,y - większy, None - nieporównywalne, Err - takie same
    """
    len_ = len(x)
    gr = [None] * len_
    eq = [None] * len_
    sm = [None] * len_

    for i in range(len_):
        gr[i] = (x[i] >= y[i])
        eq[i] = (x[i] == y[i])
        sm[i] = (x[i] <= y[i])
    if all(eq):
        raise ValueError(f"the same error {x}")  # dwa takie same punkty
    if all(gr):
        return x  # punkt x większy
    elif all(sm):
        return y  # punkt y większy
    else:
        return None  # punkty nieporównywalne


def is_gr_gra(gra, sma):
    """
    funkcja sprawdzająca czy jeden zbiór dominuje drugi
    :param gra: zbiór potencjalnie większy
    :param sma: zbiór potencjalnie mniejszy
    """
    for g in gra:
        for s in sma:
            res = is_domi(gra[g], sma[s])
            if res != gra[g]:
                raise ValueError(f"Grupy nie są dobrze zdominowane: {g} < {s}")


def is_niepor(group):
    for p1 in group:
        for p2 in group:
            if p1 != p2:
                res = is_domi(group[p1], group[p2])
                if res is not None:
                    raise ValueError(
                        "grupa nie jest wewnętrznie nieporównywalna")


def conf_bool_to_int(group):
    no_bool_group = {}
    for point_id, cryteria in group.items():
        no_bool_cryteria = []
        for cryt in cryteria:
            if cryt is True:
                no_bool_cryteria.append(1)
            elif cryt is False:
                no_bool_cryteria.append(0)
            else:
                no_bool_cryteria.append(cryt)
        no_bool_group[point_id] = no_bool_cryteria
    return no_bool_group


def get_max_min(A0, A1, matr):
    if isinstance(A0, dict) and A0:
        A0 = conf_bool_to_int(A0)
        A0, _ = _dic2matrix(A0)
        g_max = amax(A0, 0)
    elif A0 is None:
        g_max = amax(matr, 0)
    else:
        raise ValueError("Invalid input format A0")
    if isinstance(A1, dict) and A1:
        A1 = conf_bool_to_int(A1)
        A1, _ = _dic2matrix(A1)
        g_min = amin(A1, 0)
    elif A1 is None:
        g_min = amin(matr, 0)
    else:
        raise ValueError("Invalid input format A1")
    return g_max, g_min


def _preproces_data(A0, A1, B):
    B = conf_bool_to_int(B)
    a1_was = False
    if A0:
        A0 = conf_bool_to_int(A0)
        is_niepor(A0)
        if A1:
            a1_was = True
            A1 = conf_bool_to_int(A1)
            is_gr_gra(A1, A0)
            is_gr_gra(B, A0)
            is_gr_gra(A1, B)
    if not a1_was and A1:
        A1 = conf_bool_to_int(A1)
        is_niepor(A1)

    matrix, keys = _dic2matrix(B)
    return A0, A1, matrix, keys


def fuzzy_topsis(B: Dict[Any, List],
                 weights: List[float],
                 directions: List[int],
                 metric: Callable = _eukl_metr,
                 A0: Union[Dict[Any, List], None] = None,
                 A1: Union[Dict[Any, List], None] = None,
                 ) -> List[Tuple[int, Any, Tuple]]:
    """
    # todo skonsultować
    1. Każda z grup punktów musi być wewnętrznie nieporównywalna
        - jeżeli tak nie będzie funkcja zwróci ValueError
    2. Każda kolejna jest zdominowana przez poprzednią
        A0 < B < A1
        - grupy A0, A1 to grupy odniesienia dla metody fuzzy topsis
        - jeżeli tak nie będzie funkcja zwróci ValueError
    3. Grupy A0, A1 i B mają mieć postać słownika:
        { ID_punktu_1: [w11, w12, w13, ...], ID_punktu_2: [w21, w22, w23, ...], ...}
            listy [wi1,wi2,...] przechowują wartości kolejnych kryteriów dla danego punktu
            wik = wartość kryterium k dla punktu i
            np.     k1       k2   k3            k1        k2   k3
            {'M1': [58000.0, 1.0, 7.0], 'M2': [120000.0, 3.2, 8.0], 'M3': [80000.0, 4.8, 5.0],
             'M4': [68000.0, 1.6, 6.0], 'M5': [12000.0, 0.9, 3.0], 'M6': [16000.0, 1.9, 5.0]}
            - jeżeli tak nie będzie funkcja zwróci ValueError

    :param A0: granice optymalności
    :param A1: antyidealne
    :param B: grupa zawierająca punkty z których chcemy dokonać wyboru
    :param weights: lista (o długości ilości kryteriów) zawiera wartości wag dla poszczególnych kryteriów [0;1]
    :param directions: lista (o długości ilości kryteriów) mówiąca czy dane kryterium jest
        minimalizowane czy maksymalizowane {0;1}
        0 - minimalizacja kryterium, 1 - maksymalizacja kryterium
    :param metric: opcjonalna metryka  - domyślna euklidesowa
    :return: posortowane lista (ranking) podanych w gr B punktów w postaci:
        [[id_punktu1, wartość współczynnika ci metody topsis], [id_punktu2, wa...], ...]
    """

    A0, A1, matrix, keys = _preproces_data(A0, A1, B)
    matrix = _normalize(matrix)
    matrix = _apply_maxim(matrix, directions)
    matrix = _apply_weights(matrix, weights)
    g_max, g_min = get_max_min(A0, A1, matrix)
    dig, did = _get_did(matrix, metric, g_min, g_max)
    ci = _get_ci(dig, did)
    result = _sort_res(ci, keys)
    result = [(vals[0], round(vals[1], 5)) for vals in result]
    print(result)
    return result
