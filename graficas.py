import matplotlib.pyplot as plt

def graficar_poker(tabla):
    categorias = [x[0] for x in tabla]
    FO = [x[1] for x in tabla]
    FE = [x[2] for x in tabla]

    x = range(len(categorias))

    plt.figure()
    plt.bar(x, FO)
    plt.bar(x, FE, bottom=FO)

    plt.xticks(x, categorias, rotation=45)
    plt.title("FO vs FE")
    plt.tight_layout()
    plt.show()

def graficar_corridas(frec):
    plt.figure()
    plt.bar(list(frec.keys()), list(frec.values()))
    plt.title("Corridas")
    plt.show()

def graficar_ks(numeros):
    datos = sorted(numeros)
    n = len(datos)

    plt.figure()
    plt.step(datos, [(i+1)/n for i in range(n)], where='post')
    plt.plot([0,1],[0,1])
    plt.title("K-S")
    plt.show()

def histograma(numeros, show=True):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(numeros, bins=10)
    ax.set_title("Histograma")
    if show:
        plt.show()
    return fig


def dispersion(numeros, show=True):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(numeros[:-1], numeros[1:])
    ax.set_title("Dispersión")
    if show:
        plt.show()
    return fig