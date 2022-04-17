""" ....... """


import os
from traceback import print_tb
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from typing import List, Any, Dict, Callable, Tuple, Union
from typing import List, Any, Dict, Callable, Tuple, Union
from numpy import vstack, amax, inf, amin

# Funkcja szukająca kolejne klasy punktów niezdominowanych


def normalization(matrix):
    m, n = matrix.shape
    new = np.zeros(n)
    for i in range(m):
        for j in range(n):
            new[j] += (matrix[i, j])**2
            new[j] += (matrix[i, j]) ** 2
    for k in range(len(new)):
        new[k] = np.sqrt(new[k])
    return new


def get_sets(Fu):
    klasy = []
    niezdom_keys = []
    Fu.sort(key=lambda tup: tup[0])
    while len(Fu) > 0:
        niezdom = []
        a, b, c = Fu[0]
        niezdom.append((a, b, c))
        for el in range(1, len(Fu)):
            d, e, f = Fu[el]
            if a <= d and b <= e and c <= f:
                continue
            elif a <= d and (b >= e or c >= f):
                isDominated = False
                for a1, b1, c1 in niezdom:
                    if a1 <= d and b1 <= e and c1 <= f:
                        isDominated = True
                        break
                    elif a1 >= d and (b1 >= e or c1 >= f):
                        niezdom.remove((a1, b1, c1))

                if not isDominated:
                    niezdom.append((d, e, f))
            else:
                niezdom.clear()
                a, b, c = d, e, f
                niezdom.append((a, b, c))
        klasy.append(niezdom)
        for i in niezdom:
            Fu.remove(i)
    return klasy


# Funkcja szukająca odpowiednich punktów do sprawdzenia metody RMS

def get_correct_sets(Fu):
    klasy = get_sets(Fu)
    saved = []
    docel = []
    anty = []
    for i, kl in enumerate(klasy):
        if i == 0:
            saved.append((kl))
        elif i <= len(klasy) - 2:
            for el in kl:
                docel.append((el))
                print
        else:
            anty = kl

    saved.append(docel)
    saved.append(anty)

    return saved

# Kod sprawdzający czy punkt u jest w prostopadloscianie zawartym miedzy dwoma punktami


def sprawdz(p1, u, p2):
    x1, y1, z1 = p1
    xu, yu, zu = u
    x2, y2, z2 = p2
    isInside = False
    if (x1 <= xu <= x2 or x1 >= xu >= x2) and (y1 <= yu <= y2 or y1 >= yu >= y2) and (z1 <= zu <= z2 or z1 >= zu >= z2):
        isInside = True

    return isInside

# Kod obliczjący pbjetosc prostopadloscianu miedzy dwoma punktami


def calculate_volume(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2

    a = np.abs(x2-x1)
    b = np.abs(y2-y1)
    c = np.abs(z2-z1)
    obj = a*b*c
    return obj

# Kod obliczjący wspólczynnik odleglosci wykorzystany do skoringu


def wsp_skor_odl(p1, u, p2):
    odl1 = np.sqrt((u[0] - p1[0])**2 + (u[1] - p1[1])**2 + (u[2] - p1[2])**2)
    odl2 = np.sqrt((u[0] - p2[0])**2 + (u[1] - p2[1])**2 + (u[2] - p2[2])**2)
    wsp = odl1/(odl1+odl2)
    return wsp

# Funkcja obliczjaca skoring dla jednego punktu u


def skoring(A1, u, A2):
    # Suma objetosci
    V = 0
    # Lista ktotek pol i wsp odl
    obj = []
    for a1 in A1:
        for a2 in A2:
            if sprawdz(a1, u, a2):
                P_i = calculate_volume(a1, a2)
                V += P_i
                f_i = wsp_skor_odl(a1, u, a2)
                obj.append((P_i, f_i))

    # Skoring:
    # Jeżeli nie stworzono żadnego prostopadloscianu zwracamy 1
    if V == 0:
        return 1
    else:
        F = sum([(Pi/V)*wsp for Pi, wsp in obj])
        return F

# Funkcja wyznaczająca i wyswietlajaca ranking


def get_ranking(A1, U, A2, Fu_keys, keys):
    U2 = {}
    U22 = {}
    ranking = [(u, skoring(A1, u, A2)) for u in U]
    ranking.sort(key=lambda x: x[1])
    for i in range(len(U)):
        for j in range(len(Fu_keys)):
            aa, bb, cc = Fu_keys[j]
            if (aa, bb, cc) == ranking[i][0]:
                U2[ranking[i][0]] = keys[j]

    arr, keys11 = matrix2(U2)
    rank_to_compare = [(arr[i][0], ranking[i][1]) for i in range(len(arr))]
    for i in range(len(keys11)):
        U22[str(arr[i])] = keys11[i], ranking[i][1]
    # print("Rank\t: \t Point\t\t\t\t\t\t\t\t\tSkoring")
    # for i in range(len(ranking)):
    #     print(
    #         f'{i + 1}\t:  {str(arr[i])} \t {ranking[i][0]}\t\t\t{round(ranking[i][1], 2)}')
    return U22, rank_to_compare

# zamianna bool na int


def bool_int(grupa):
    gr1 = {}
    for pkt, kryteria in grupa.items():
        kryteria1 = []
        for k in kryteria:
            if k is True:
                kryteria1.append(1)
            else:
                if k is False:
                    kryteria1.append(0)
                else:
                    kryteria1.append(k)
        gr1[pkt] = kryteria1
    return gr1

# zamiana słownika na macierz numpy


def matrix2(dict_):
    keys = list(dict_.keys())
    arr = dict_[keys[0]]
    for key in keys[1:]:
        arr = vstack([arr, dict_[key]])
    return arr, keys


# normalizacja macierzy

def normalizacja(matrix):
    matrix = matrix / ((matrix ** 2).sum(axis=0)) ** (1/2)
    return matrix


def RSM(B, idxs):
    B = bool_int(B)
    matrix, keys = matrix2(B)
    matrix = normalizacja(matrix)
    aaa, bbb = matrix.shape
    if not idxs:
        idxs = [0, 1, 2]
    elif len(idxs) < 3:
        idxs = [0, 1, 2]

    if bbb >= 3:
        #    print("za duzo kryteriow")
        #  else:
        Fu1 = []
        Fu_keys = []
        for i in range(len(matrix)):
            a2 = matrix[i][idxs[0]]
            b2 = matrix[i][idxs[1]]
            c2 = matrix[i][idxs[2]]
            Fu_keys.append([a2, b2, c2])
            Fu1.append((a2, b2, c2))

        saved = get_correct_sets(Fu1)
        # print(f'Znalezione klasy punktów: \n {saved}')
        # print(f'Zbiór punktów docelowych: \n {saved[0]}')
        # print(f'Zbiór decyzji: \n {saved[1]}')
        # print(f'Zbiór punktów status quo: \n {saved[2]}')
        A1 = saved[0]
        U = saved[1]
        A2 = saved[2]
        U2 = []

        for i in range(len(Fu_keys)):
            for j in range(len(U)):
                aa, bb, cc = Fu_keys[i]
                if (aa, bb, cc) == U[j]:
                    U2.append(keys[i])

        fig = plt.figure(figsize=(9, 6))

        ax = plt.axes(projection='3d')

        for i in range(len(saved)):
            lst = saved[i]
            x, y, z = zip(*lst)
            ax.scatter3D(x, y, z)
            plt.grid()
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        style = ['g*', 'b*', 'r*']
        print('\nRanking')
        ranking1, rank_to_compare = get_ranking(A1, U, A2, Fu_keys, keys)
        print('\n')

        fig = plt.figure(figsize=(8, 5))

        ax = plt.axes(projection='3d')

        for i in range(len(saved)):
            lst = saved[i]
            x, y, z = zip(*lst)
            ax.scatter3D(x, y, z)
            plt.grid()
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        style = ['g*', 'b*', 'r*']
        ax.legend(['punkty docelowe', 'punkty decyzyjne', 'punkty statusu quo'])
        path = os.path.abspath("plot_img.png")
        plt.savefig(path, bbox_inches='tight')

        return ranking1, rank_to_compare


# # zwraca "mieszkanie,((znormalizowana wartość kryteriów),scoring)
# B = {'M1': [58000, 36.5, 450, 7, 9, 4, 2, 9, 3, 5, 10, True, True, True, 7, 2004, False, 3, 200],
#      'M2': [108000, 60.0, 500, 3, 5, 4, 8, 2, 6, 7, 9, False, False, True, 5, 2012, False, 12, 300],
#      'M3': [72000, 15.4, 666, 9, 8, 2, 3, 4, 6, 7, 8, True, False, False, 6, 2021, False, 5, 600],
#      'M4': [99000, 70, 420, 6, 8, 7, 3, 5, 6, 7, 7, False, True, False, 4, 2010, True, 7, 1200],
#      'M5': [70000, 40, 500, 2, 10, 7, 5, 4, 3, 9, 1, True, True, True, 3, 2021, True, 15, 500],
#      'M6': [120000, 70, 350, 9, 1, 6, 8, 2, 6, 5, 5, False, False, True, 5, 2015, True, 4, 700],
#      'M7': [50000, 20, 750, 1, 5, 3, 4, 7, 4, 1, 6, False, True, False, 2, 1997, False, 3, 200],
#      'M8': [60000, 35, 440, 3, 5, 7, 10, 9, 7, 9, 5, True, True, False, 4, 2012, True, 6, 500],
#      'M9': [92000, 55, 580, 3, 6, 4, 8, 4, 6, 4, 4, True, True, False, 3, 2000, False, 2, 600],
#      'M10': [121000, 70, 700, 5, 8, 2, 3, 3, 5, 2, 9, False, True, True, 4, 2010, True, 7, 600],
#      'M11': [88000, 57, 550, 5, 10, 7, 6, 7, 6, 2, 5, True, True, False, 3, 2008, False, 3, 300],
#      'M12': [88000, 50, 500, 8, 5, 7, 7, 3, 6, 1, 5, True, True, True, 3, 2012, False, 12, 500],
#      'M13': [52000, 55, 580, 1, 7, 3, 4, 7, 9, 4, 9, False, True, False, 3, 1956, True, 3, 200],
#      'M14': [96000, 70, 700, 2, 1, 1, 9, 9, 5, 5, 7, False, False, True, 4, 1999, True, 1, 300],
#      'M15': [40000, 20, 300, 5, 2, 9, 4, 9, 1, 1, 6, False, True, True, 2, 2001, True, 4, 400],
#      'M16': [300000, 150, 1000, 7, 8, 4, 2, 9, 9, 9, 0, True, False, True, 8, 2021, False, 10, 1000],
#      'M17': [186000, 90, 800, 5, 9, 2, 3, 8, 8, 7, 9, False, True, True, 3, 2014, True, 15, 500],
#      'M18': [150000, 82, 700, 6, 7, 3, 1, 4, 5, 7, 8, False, False, True, 3, 2017, False, 10, 300],
#      'M19': [212000, 110, 900, 7, 5, 1, 5, 6, 7, 8, 7, True, True, True, 4, 1998, False, 8, 1500],
#      'M20': [250000, 150, 1000, 8, 4, 1, 8, 7, 9, 9, 6, True, True, False, 5, 1986, True, 2, 800]}

# B2 = {'M1': [58000, 7, True],
#       'M2': [108000, 3, False],
#       'M3': [72000, 9, True],
#       'M4': [99000, 6, False],
#       'M5': [70000, 2, True],
#       'M6': [120000, 9, False],
#       'M7': [50000, 1, False],
#       'M8': [60000, 3, True],
#       'M9': [92000, 3, True],
#       'M10': [121000, 5, False],
#       'M11': [88000, 5, True],
#       'M12': [88000, 8, True],
#       'M13': [52000, 1, False],
#       'M14': [96000, 2, False],
#       'M15': [40000, 5, False],
#       'M16': [300000, 7, True],
#       'M17': [186000, 5, False],
#       'M18': [150000, 6, False],
#       'M19': [212000, 7, True],
#       'M20': [250000, 8, True]}

# res = RSM(B,[1,2,3])
# print(res[0])
# print(res[1])
