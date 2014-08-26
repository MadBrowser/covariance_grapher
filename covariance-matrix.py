#!/usr/bin/python
# coding=utf-8
''' Este código está pensado para leer archivos SAC que contengan sólo 1 canal.
    Como parámetro de entrada se debe entregar la ruta completa a los archivos
    SAC. En este caso para la matriz de covarianza se necesitan las 3
    componentes N-E-Z por lo que se entiende serán 3 rutas como parámetros de
    entrada. Se asume también que todos los canales tienen el mismo SR
'''
from obspy.core import read
from operator import attrgetter
import numpy as np
import sys

channels = []
mean_values = []

# Lectura de archivos.
if len(sys.argv) == 5:
    for i in range(1, 4):
        channels.append(read(sys.argv[i])[0])  # Único canal del archivo
    window = sys.argv[4]
else:
    print 'Número de parámetros de entrada incorrecto'

# Corrección del tiempo en los canales
channels = sorted(channels, key=attrgetter('stats.starttime'), reverse=True)
for channel in channels:
    delta = (channels[0].stats.starttime - channel.stats.starttime)
    delta_samples = int(delta * channel.stats.sampling_rate)
    channel.data = channel.data[delta_samples:channel.stats.npts]

''' TODO: Resolver como corregir los arreglos cuando tienen distintos números
    de elementos.
'''

# Cálculo de número de muestras para la ventana
n = float(window) * channels[0].stats.sampling_rate

# Creación vector en donde a cada componente se le resta el promedio del canal
for channel in channels:
    new_values = []  # Crea un arreglo auxiliar
    mean = np.mean(channel.data)  # Calcula el promedio del canal
    for sample in channel:  # Para cada elemento del canal
        value = sample - mean  # Calcula su nuevo valor
        new_values.append(value)  # Y lo agrega al arreglo auxiliar
    mean_values.append(new_values)  # Cuando termina agrega el arreglo auxiliar
                                    # al arreglo con los nuevos canales.
# Cálculo de los componenetes de la matriz.
x = [0, 0]
y = [0, 0]
z = [0, 0]
covariance_matrix = np.matrix([x, y, z])
