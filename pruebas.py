from collections import Counter

probabilidades = {
    "Todos diferentes": 0.3024,
    "Un par": 0.5040,
    "Dos pares": 0.1080,
    "Trica": 0.0720,
    "Full": 0.0090,
    "Poker": 0.0045,
    "Quintilla": 0.0001
}

CHI_CRITICO_005 = {
    1: 3.84, 2: 5.99, 3: 7.81, 4: 9.49, 5: 11.07,
    6: 12.59, 7: 14.07, 8: 15.51, 9: 16.92, 10: 18.31,
    11: 19.68, 12: 21.03, 13: 22.36, 14: 23.68, 15: 25.00,
    16: 26.30, 17: 27.59, 18: 28.87, 19: 30.14, 20: 31.41
}

def obtener_chi_critico(gl):
    if gl in CHI_CRITICO_005:
        return CHI_CRITICO_005[gl]
    else:
        return None  # fuera de tabla

def agrupar_categorias(tabla):
    """
    tabla: lista de tuplas (categoria, FO, FE)
    """
    nueva_tabla = []
    grupo_FO = 0
    grupo_FE = 0
    nombres = []

    for categoria, FO, FE in tabla:
        grupo_FO += FO
        grupo_FE += FE
        nombres.append(categoria)

        if grupo_FE >= 5:
            nueva_tabla.append((
                " + ".join(nombres),
                grupo_FO,
                grupo_FE
            ))
            grupo_FO = 0
            grupo_FE = 0
            nombres = []

    # Si sobra algo, se une al último grupo
    if grupo_FE > 0:
        if nueva_tabla:
            ultima = nueva_tabla[-1]
            nueva_tabla[-1] = (
                ultima[0] + " + " + " + ".join(nombres),
                ultima[1] + grupo_FO,
                ultima[2] + grupo_FE
            )
        else:
            nueva_tabla.append((" + ".join(nombres), grupo_FO, grupo_FE))

    return nueva_tabla

def tabla_corridas(FO, FE):
    tabla = []
    for i in FE:
        tabla.append((f"L={i}", FO.get(i,0), FE[i]))
    return tabla

def obtener_digitos(numero):
    decimal = str(numero).split(".")[1]
    return decimal.ljust(5, '0')[:5]

def clasificar_numero(numero):
    digitos = obtener_digitos(numero)
    conteo = Counter(digitos)
    valores = sorted(conteo.values(), reverse=True)

    if valores == [5]:
        return "Quintilla"
    elif valores == [4,1]:
        return "Poker"
    elif valores == [3,2]:
        return "Full"
    elif valores == [3,1,1]:
        return "Trica"
    elif valores == [2,2,1]:
        return "Dos pares"
    elif valores == [2,1,1,1]:
        return "Un par"
    else:
        return "Todos diferentes"

def contar_frecuencias(lista):
    return Counter([clasificar_numero(n) for n in lista])

def chi_cuadrado(frecuencias, N):
    chi = 0
    for categoria, prob in probabilidades.items():
        FO = frecuencias.get(categoria, 0)
        FE = N * prob
        if FE > 0:
            chi += ((FO - FE) ** 2) / FE
    return chi

def chi_cuadrado_agrupado(tabla):
    chi = 0
    for _, FO, FE in tabla:
        if FE > 0:
            chi += ((FO - FE) ** 2) / FE
    return chi

def generar_tabla(frecuencias, N):
    return [(cat, frecuencias.get(cat, 0), N * prob)
            for cat, prob in probabilidades.items()]

# ---------- AUXILIARES DE PRUEBA ----------

def obtener_chi_critico_gl(gl):
    # Retorna chi crítico a 0.05 si existe en la tabla o aproximado (nonide)
    return obtener_chi_critico(gl)


def ks_critico(n, alpha=0.05):
    if n <= 0:
        return None
    if alpha == 0.05:
        return 1.36 / (n ** 0.5)
    if alpha == 0.01:
        return 1.63 / (n ** 0.5)
    # valor por defecto aproximado
    return 1.36 / (n ** 0.5)


def prueba_poker(numeros, gl=None, alpha=0.05):
    N = len(numeros)
    frec = contar_frecuencias(numeros)
    tabla = generar_tabla(frec, N)
    tabla_agrupada = agrupar_categorias(tabla)
    chi = chi_cuadrado_agrupado(tabla_agrupada)
    if gl is None:
        gl = max(len(tabla_agrupada) - 1, 1)
    chi_critico = obtener_chi_critico_gl(gl)
    decision = "Rechaza H0" if chi_critico is not None and chi > chi_critico else "No rechaza H0"

    return {
        "metodo": "Poker",
        "chi": chi,
        "gl": gl,
        "chi_critico": chi_critico,
        "decision": decision,
        "tabla_agrupada": tabla_agrupada
    }


def prueba_corridas(numeros, gl=None, alpha=0.05):
    N = len(numeros)
    if N == 0:
        return None

    binaria = generar_binaria(numeros)
    corr = obtener_corridas(binaria)
    FO = frecuencia_corridas(corr)
    max_long = max(FO.keys()) if FO else 0
    FE = frecuencia_esperada_corridas(N, max_long)
    tabla = tabla_corridas(FO, FE)
    tabla_agrupada = agrupar_categorias(tabla)
    chi = chi_cuadrado_agrupado(tabla_agrupada)
    if gl is None:
        gl = max(len(tabla_agrupada) - 1, 1)
    chi_critico = obtener_chi_critico_gl(gl)
    decision = "Rechaza H0" if chi_critico is not None and chi > chi_critico else "No rechaza H0"

    return {
        "metodo": "Corridas",
        "chi": chi,
        "gl": gl,
        "chi_critico": chi_critico,
        "decision": decision,
        "tabla_agrupada": tabla_agrupada,
        "corridas": corr,
        "FO": FO,
        "FE": FE
    }


def prueba_ks(numeros, alpha=0.05):
    if not numeros:
        return None

    D, Dp, Dm = kolmogorov_smirnov(numeros)
    D_critico = ks_critico(len(numeros), alpha)
    decision = "Rechaza H0" if D > D_critico else "No rechaza H0"

    return {
        "metodo": "Kolmogorov-Smirnov",
        "D": D,
        "Dp": Dp,
        "Dm": Dm,
        "D_critico": D_critico,
        "decision": decision
    }

# ---------- CORRIDAS ----------

def generar_binaria(numeros):
    return [1 if n >= 0.5 else 0 for n in numeros]

def obtener_corridas(binaria):
    corridas, longitud = [], 1
    for i in range(1, len(binaria)):
        if binaria[i] == binaria[i-1]:
            longitud += 1
        else:
            corridas.append(longitud)
            longitud = 1
    corridas.append(longitud)
    return corridas

def frecuencia_corridas(corridas):
    return Counter(corridas)

def frecuencia_esperada_corridas(n, max_long):
    return {i: (n - i + 3) / (2 ** (i + 2)) for i in range(1, max_long+1)}

def chi_cuadrado_corridas(FO, FE):
    return sum(((FO.get(i,0)-FE[i])**2)/FE[i] for i in FE if FE[i] > 0)

# ---------- KS ----------

def kolmogorov_smirnov(numeros):
    datos = sorted(numeros)
    n = len(datos)

    Dp = max((i/n - r) for i, r in enumerate(datos, start=1))
    Dm = max((r - (i-1)/n) for i, r in enumerate(datos, start=1))

    return max(Dp, Dm), Dp, Dm