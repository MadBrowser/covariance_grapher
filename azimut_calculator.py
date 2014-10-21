#!/usr/bin/python
# coding=utf-8
""" Código que toma 2 vectores y cálcula el árco tangente entre ellos.
"""
import numpy as np

# Vectores de ejemplo
v1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
v2 = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

y = v2[-1]
x = v1[-1]

if x != 0 and y != 0:
    # Cálculo del ángulo en grados (no en radianes), se usa valor absoluto
    # para poder sumar 90 de acuerdo al cuadrante
    angulo = np.abs(np.arctan(y/x) * 180 / np.pi)

    if x > 0 and y < 0:
        angulo = angulo + 90
    elif x < 0 and y < 0:
        angulo = angulo + 180
    elif x < 0 and y > 0:
        angulo = angulo + 270
else:
    angulo = 0
return angulo
