import matplotlib.pyplot as plt
from collections import Counter

def _es_discreto(numeros):
    """Detecta si los datos son de distribución discreta."""
    if not numeros:
        return False
    
    # Convertir a float y verificar si todos son enteros
    try:
        valores_float = [float(x) for x in numeros]
        return all(v == int(v) for v in valores_float)
    except (ValueError, TypeError):
        return False

def _histograma_continuo(ax, numeros, bins=10):
    """Grafica histograma para distribuciones continuas."""
    ax.hist(numeros, bins=bins, edgecolor='black', alpha=0.7)
    ax.set_xlabel("Valor")
    ax.set_ylabel("Frecuencia")

def _histograma_discreto(ax, numeros):
    """Grafica histograma para distribuciones discretas."""
    # Convertir a enteros y contar frecuencias
    valores_int = [int(float(x)) for x in numeros]
    contador = Counter(valores_int)
    
    valores = sorted(contador.keys())
    frecuencias = [contador[v] for v in valores]
    
    ax.bar(valores, frecuencias, width=0.8, edgecolor='black', alpha=0.7)
    ax.set_xlabel("Valor")
    ax.set_ylabel("Frecuencia")
    ax.set_xticks(valores)

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
    """Histograma adaptado para distribuciones continuas y discretas."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    if not numeros:
        ax.set_title("Histograma (vacío)")
        if show:
            plt.show()
        return fig
    
    # Detectar tipo de distribución
    es_discreto = _es_discreto(numeros)
    
    if es_discreto:
        _histograma_discreto(ax, numeros)
        ax.set_title("Histograma (Discreta)")
    else:
        _histograma_continuo(ax, numeros, bins=10)
        ax.set_title("Histograma (Continua)")
    
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