""" Jaromir-hub146 """


from typing import List, Any, Dict, Callable, Tuple, Union
import numpy as np
import networkx as nx
from mieszkania import B, weight, v, przedz
import matplotlib.pyplot as plt
from fuzzy_topsis import fuzzy_topsis
from UTA import UTA_v2
from RSM import RSM_v2


# Funkcja zwracająca wektor n elementowy, gdzie: n - liczba porównywanych mieszkań.
# Indeks w wektorze odpowiada numerowi punktu, wartość znajdująca się pod tym indeksem jest pozycją w rankingu
def convert(B: Dict[str, Union[int, float, bool]], ranking: List[Tuple[str, float]]) -> List[int]:
    vect = list()
    prev = list()
    for el in B.keys():
        for ob in ranking:
            if ob[0] == el:
                if ob[1] not in prev:
                    vect.append(1 + ranking.index(ob))
                    prev.append(ob[1])
                else:
                    vect.append(ranking.index(ob))

    return vect


# Funkcja zwracająca odległość pomiędzy dwoma zadanymi rankingami.
# Do obliczenia odległości zastosowano metrykę euklidesową.
def compare_rankings_1(B, rank1, rank2):
    rank1_ = convert(B, rank1)
    rank2_ = convert(B, rank2)
    if len(rank1_) == len(rank2_):
        distance = 0
        sum_ = 0
        for i in range(len(rank1_)):
            if rank1[i][1] != 0 and rank2[i][1] != 0:
                sum_ += (rank1_[i] - rank2_[i]) ** 2
        distance += sum_ ** (1 / 2)
    else:
        raise ValueError
    return int(distance)


# Funkcja zwracająca odległość pomiędzy dwoma zadanymi rankingami.
# Dodano wagi pozwlające określić jakie miejsce w rankingu zajmują punkty.
# Waga jest maksymalną różnicą pomiędzy zajmowanymi miejscami w rankingu przez punktu, a ilością punktów w rankingu.
# Do obliczenia odległości zastosowano metrykę euklidesową.
def compare_rankings_2(B, rank1, rank2):
    rank1_ = convert(B, rank1)
    rank2_ = convert(B, rank2)
    if len(rank1_) == len(rank2_):
        length = len(rank1_)
        distance = 0
        sum_ = []
        for i in range(len(rank1_)):
            if rank1[i][1] != 0 and rank2[i][1] != 0:
                sum_.append((rank1_[i] - rank2_[i]) ** 2)

        for i in range(len(rank1_)):
            if rank1[i][1] != 0 and rank2[i][1] != 0:
                distance += max(length - rank1_[i], length - rank2_[i]) * sum_[i]
    else:
        raise ValueError

    return int(distance ** (1 / 2))


# Funkcja tworząca na podstawie listy rankingów macierz sąsiedztwa, która zawiera informacje o odległości
# pomiędzy każdą parą rankingów. Wkorzystywana jest do wizualizacji odległości pomiędzy rankingami.
def matrix_of_rank_value(B: Dict[str, Union[int, float, bool]], rankings: List[List[Tuple[str, float]]], weight: bool) -> np.ndarray:
    matrix = np.zeros((len(rankings), len(rankings)))

    for row in range(len(rankings)):
        for col in range(len(rankings)):
            if row == col:
                matrix[row][col] = 0
            else:
                if weight:
                    matrix[row][col] = compare_rankings_2(B, rankings[row], rankings[col])
                else:
                    matrix[row][col] = compare_rankings_1(B, rankings[row], rankings[col])

    return matrix.astype(int)


# Funkcja tworząca graf z wagami, gdzie wagi reprezentują odległości pomiędzy rankingami.
# Do utworzenia grafu wykorzystano bibliotekę NetworkX - wykorzystywaną
# do rozwiązywania i wizualizacji problemów grafowych.
# Metoda RSM zwraca ranking zwierający mniejszą ilość miast
# z tego powodu porównanie rankingów w przypadku metody RSM z pozostałymi przeprowadzono
# dla miast, których wartość funkcji skoringowej była różna od zera.
def plot_graph(matrix: np.ndarray):
    labeldict = dict()
    labeldict[0] = "Fuzzy Topsis"
    labeldict[1] = "UTA"
    labeldict[2] = "RSM"
    # labeldict[0] = "Metoda 1"
    # labeldict[1] = "Metoda 2"
    # labeldict[2] = "Metoda 3"
    plt.figure(figsize=(12, 6))
    G = nx.from_numpy_matrix(np.matrix(matrix), create_using=nx.DiGraph())
    layout = nx.spring_layout(G)
    nx.draw(G, layout, node_size=400, labels=labeldict, node_color="green", with_labels=True, font_weight='bold', font_size=12, font_color="red", width=3, edge_color="tab:green")
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels, font_size=12)
    plt.show()


# Funkcja wykorzystywana do sortowania danych rankingów względem wartości funkcji skoringowej
# - mieszkania posortowane są od największej do najmniejszej wartości funkcji skoringowej.
def sort(rank):
    new_rank = list()
    lista = [el[1] for el in rank]
    zabr = []
    while len(lista) > len(zabr):
        wiekszy = float("-inf")
        for id in range(len(lista)):
            if id not in zabr:
                if wiekszy < lista[id]:
                    wiekszy = lista[id]

        id_max = lista.index(wiekszy)
        if id_max in zabr:
            zabr.append(id_max + 1)
            new_rank.append(rank[id_max + 1])
        else:
            zabr.append(id_max)
            new_rank.append(rank[id_max])
    return new_rank


# Funkcja zwaracjąca dwuelementową krotkę. Pierwszym elementem jest macierz nxm,
# gdzie n - liczba maieszkań, m - liczba porównywanych metod zawierająca informacje o pozycji punktów w rankingach
# Drugim element stanowi macierz nxm zawierająca informację o wartościach funkcji skoringowych
# punktów znajdujących się w pierwszej macierzy.
def convert_to_two_matrix(B, list_of_ranking):
    convert_list = list()
    for i in range(len(list_of_ranking)):
        convert_list.append(convert(B, list_of_ranking[i]))
    matrix_of_rank = np.array(convert_list)

    value_list = list()
    for i in range(len(convert_list)):
        value_list.append([list_of_ranking[i][x - 1][1] for x in convert_list[i]])
    matrix_of_value = np.array(value_list)

    return matrix_of_rank.T, matrix_of_value.T


# Główna funkcja wykorzystana do porówanania rankingów. Generuje porównanie rankingów w przestrzeni 2D oraz 3D.
# Znaczącą część ciała funkcji stanowi zobrazowanie w przestrzni trójwymiarowej punktów reprezentujących
# mieszkania rozmieszczonych w przestrzeni zgodnie z wartościami odpowiadającym imfunkcji skoringowych.
# Punkty w przestrzni zostały oznaczone kolumną zawierającą informacje o miejscach jakie zajmują w rankigach
# dla metod, zaczynając od góry: metoda pierwsza - fuzzy topsis, metoda druga - UTA, metoda trzecia - RSM.
# Dodatkowo funkcja uzupełnia ranking danej metody jeżeli jego rozmiar różni się od rozmiaru
# rankingów pozostałych metod.
def compare_rank_main_function(B, list_of_ranks, weight: bool):
    for rank in list_of_ranks:
        if len(rank) != len(list_of_ranks[0]):
            list_of_rank = [x[0] for x in rank]
            for key in B.keys():
                if key not in list_of_rank:
                    rank.append((key, 0))

    plot_graph(matrix_of_rank_value(B, list_of_ranks, weight))
    ranks, score = convert_to_two_matrix(B, list_of_ranks)

    plt.figure(figsize=(12, 6))
    ax = plt.axes(projection='3d')
    for i, point in enumerate(score[:]):
        ax.scatter(point[0], point[1], point[2])
        ax.text(point[0], point[1], point[2], f"  {ranks[i, 0]}\n  {ranks[i, 1]}\n  {ranks[i, 2]}",
                color='b', fontsize=6)
    ax.legend([f"{key} {list(ranks[i, :])}" for i, key in enumerate(B.keys())], loc='upper right',
              bbox_to_anchor=(-0.2, 0.9))
    ax.dist = 8
    ax.set_xlabel("F. Topsis - $c_i$")
    ax.set_ylabel("UTA - $c_i$")
    ax.set_zlabel("RSM - $c_i$")
    ax.set_title("Zobrazowanie położenia zadanych mieszkań w rankingach")
    plt.show()


def run_compare_1(B_, weight_, v_, przedz_):
    fuzzy_topsis_ranking = fuzzy_topsis(B_, weight_, v_)
    UTA_ranking = UTA_v2(B_, weight_, przedz_, v_)
    RMS_ranking = RSM_v2(B_)[1]
    list_of_ranks = [sort(fuzzy_topsis_ranking), sort(UTA_ranking), RMS_ranking]
    compare_rank_main_function(B_, list_of_ranks, False)


def run_compare_2(B_, weight_, v_, przedz_):
    fuzzy_topsis_ranking = fuzzy_topsis(B_, weight_, v_)
    UTA_ranking = UTA_v2(B_, weight_, przedz_, v_)
    RMS_ranking = RSM_v2(B_)[1]
    list_of_ranks = [sort(fuzzy_topsis_ranking), sort(UTA_ranking), RMS_ranking]
    compare_rank_main_function(B_, list_of_ranks, True)