"""Funciones para transformar números uniformes en otras distribuciones.

Todas las funciones reciben una lista de números en [0,1], validan el rango y
retornan una lista transformada sin generar números adicionales.
"""

import math
from typing import Iterable, List

__all__ = [
    "validar_uniformes",
    "exponencial",
    "normal_box_muller",
    "poisson_inversion",
    "bernoulli",
    "binomial",
    "triangular",
]

EPSILON = 1e-15


def validar_uniformes(numeros: Iterable[float]) -> None:
    """Verifica que los valores estén en el rango [0, 1]."""
    if numeros is None:
        raise ValueError("La lista de números uniforme no puede ser None.")

    for indice, valor in enumerate(numeros):
        try:
            x = float(valor)
        except (TypeError, ValueError):
            raise ValueError(f"Valor no numérico en posición {indice}: {valor}")

        if x < 0.0 or x > 1.0:
            raise ValueError(
                f"Valor fuera de rango [0,1] en posición {indice}: {valor}"
            )


def _ajustar_uniforme(valor: float) -> float:
    """Ajusta bordes para evitar valores que rompan la inversa de algunas distribuciones."""
    return min(max(valor, 0.0), 1.0 - EPSILON)


def exponencial(uniformes: Iterable[float], lam: float = 1.0) -> List[float]:
    """Transforma uniformes en una muestra de distribución exponencial.

    Args:
        uniformes: lista de valores en [0,1].
        lam: tasa de la distribución exponencial.

    Returns:
        Lista de valores exponenciales.
    """
    if lam <= 0:
        raise ValueError("La tasa lam debe ser mayor que 0.")

    uniformes = list(uniformes)
    validar_uniformes(uniformes)

    return [-(math.log(1.0 - _ajustar_uniforme(u)) / lam) for u in uniformes]


def normal_box_muller(uniformes: Iterable[float], mu: float = 0.0, sigma: float = 1.0) -> List[float]:
    """Transforma uniformes en una muestra normal usando Box-Muller.

    Debe recibir una cantidad par de uniformes. Cada par produce dos valores normales.
    """
    if sigma <= 0:
        raise ValueError("La desviación estándar sigma debe ser mayor que 0.")

    uniformes = list(uniformes)
    validar_uniformes(uniformes)

    if len(uniformes) < 2:
        raise ValueError("Se requieren al menos 2 uniformes para generar normales.")

    if len(uniformes) % 2 != 0:
        uniformes = uniformes[:-1]

    resultado: List[float] = []
    for i in range(0, len(uniformes), 2):
        u1 = _ajustar_uniforme(uniformes[i])
        u2 = uniformes[i + 1]
        r = math.sqrt(-2.0 * math.log(1.0 - u1))
        theta = 2.0 * math.pi * u2
        resultado.append(mu + sigma * r * math.cos(theta))
        resultado.append(mu + sigma * r * math.sin(theta))

    return resultado


def poisson_inversion(uniformes: Iterable[float], lam: float) -> List[int]:
    """Transforma uniformes en una muestra de Poisson por inversión de la CDF."""
    if lam <= 0:
        raise ValueError("El parámetro lam debe ser mayor que 0.")

    uniformes = list(uniformes)
    validar_uniformes(uniformes)

    resultado: List[int] = []
    for u in uniformes:
        u = _ajustar_uniforme(u)
        p = math.exp(-lam)
        F = p
        k = 0

        while u > F:
            k += 1
            p *= lam / k
            F += p

        resultado.append(k)

    return resultado


def bernoulli(uniformes: Iterable[float], p: float = 0.5) -> List[int]:
    """Transforma uniformes en una muestra de Bernoulli con probabilidad p."""
    if p < 0.0 or p > 1.0:
        raise ValueError("La probabilidad p debe estar en [0,1].")

    uniformes = list(uniformes)
    validar_uniformes(uniformes)
    return [1 if u < p else 0 for u in uniformes]


def binomial(uniformes: Iterable[float], n: int, p: float) -> List[int]:
    """Transforma uniformes en una muestra binomial usando bloques de n uniformes."""
    if n <= 0:
        raise ValueError("El parámetro n debe ser un entero positivo.")
    if p < 0.0 or p > 1.0:
        raise ValueError("La probabilidad p debe estar en [0,1].")

    uniformes = list(uniformes)
    validar_uniformes(uniformes)

    if len(uniformes) < n:
        raise ValueError("Se requieren al menos n uniformes para generar una muestra binomial.")

    resultado: List[int] = []
    bloques = len(uniformes) // n
    for i in range(bloques):
        bloque = uniformes[i * n:(i + 1) * n]
        resultado.append(sum(1 if u < p else 0 for u in bloque))

    return resultado


def triangular(uniformes: Iterable[float], a: float = 0.0, b: float = 1.0, c: float = 0.5) -> List[float]:
    """Transforma uniformes en una muestra de distribución triangular.

    Args:
        uniformes: lista de valores en [0,1].
        a: límite inferior.
        b: límite superior.
        c: moda.
    """
    if a > c or c > b:
        raise ValueError("Los parámetros deben cumplir a <= c <= b.")

    uniformes = list(uniformes)
    validar_uniformes(uniformes)

    resultado: List[float] = []
    f = (c - a) / (b - a) if b != a else 0.0

    for u in uniformes:
        u = _ajustar_uniforme(u)
        if u < f:
            resultado.append(a + math.sqrt(u * (b - a) * (c - a)))
        else:
            resultado.append(b - math.sqrt((1.0 - u) * (b - a) * (b - c)))

    return resultado
