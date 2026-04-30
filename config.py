# config.py - Constantes y configuraciones para el proyecto de pruebas de aleatoriedad

# Probabilidades para la prueba de Poker
PROBABILIDADES_POKER = {
    "Todos diferentes": 0.3024,
    "Un par": 0.5040,
    "Dos pares": 0.1080,
    "Trica": 0.0720,
    "Full": 0.0090,
    "Poker": 0.0045,
    "Quintilla": 0.0001
}

# Valores críticos de Chi-cuadrado para alpha=0.05
CHI_CRITICO_005 = {
    1: 3.84, 2: 5.99, 3: 7.81, 4: 9.49, 5: 11.07,
    6: 12.59, 7: 14.07, 8: 15.51, 9: 16.92, 10: 18.31,
    11: 19.68, 12: 21.03, 13: 22.36, 14: 23.68, 15: 25.00,
    16: 26.30, 17: 27.59, 18: 28.87, 19: 30.14, 20: 31.41
}

# Valor crítico para prueba de Kolmogorov-Smirnov (alpha=0.05)
KS_CRITICO_005 = 1.36

# Valor crítico para prueba de Promedios (alpha=0.05, dos colas)
Z_CRITICO_PROMEDIOS = 1.96