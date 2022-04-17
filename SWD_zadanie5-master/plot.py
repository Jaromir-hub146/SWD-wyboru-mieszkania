""" ....... """


from typing import List, Dict, Any, Tuple
from numpy import inf
import matplotlib.pyplot as plt
import os


def plot(data: Dict[Any, List], weights: List[float], ranks: List[Tuple], param_names: List[str], method: str):
    """
    Rysuje wykres z podpisanym rankingiem, wybór parametrów na podstawie wag
    @param method: nazwa metody
    @param param_names: nazwy parametrów
    @param data: słownik mieszkań
    @param weights: wagi parametrów
    @param ranks: ranking [["M3", 0.02], ["M4", 0.07], ...]
    """
    if method != 'RSM':
        i1, max1 = 0, -inf
        i2, max2 = 1, -inf
        i3, max3 = 2, -inf
        for i, w in enumerate(weights[3:]):
            if w > max1:
                i3, max3 = i2, max2
                i2, max2 = i1, max1
                i1, max1 = i, w
            elif w > max2:
                i3, max3 = i2, max2
                i2, max2 = i, w
            elif w > max3:
                i3, max3 = i, w
    else:
        i1, i2, i3 = 0, 8, 18

    plt.figure(figsize=(8, 5))
    ax = plt.axes(projection='3d')
    for n, r in enumerate(ranks):
        ax.scatter(data[r[0]][i1], data[r[0]][i2], data[r[0]][i3])
        if n < 5:
            ax.text(data[r[0]][i1], data[r[0]][i2],
                    data[r[0]][i3], f" [{n + 1}] {r[0]}")
    ax.dist = 12
    ax.set_xlabel(param_names[i1])
    ax.set_ylabel(param_names[i2])
    ax.set_zlabel(param_names[i3])
    ax.set_title(method)
    path = os.path.abspath("plot_img.png")
    plt.savefig(path, bbox_inches='tight')
