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
data = []

# Lectura de archivos.
if len(sys.argv) == 5:
    for i in range(1, 4):
        channels.append(read(sys.argv[i])[0])  # Único canal del archivo
    window = int(sys.argv[4])
else:
    print 'Número de parámetros de entrada incorrecto'

# Corrección del tiempo en los canales
channels = sorted(channels, key=attrgetter('stats.starttime'), reverse=True)
for channel in channels:
    delta = (channels[0].stats.starttime - channel.stats.starttime)
    delta_samples = int(delta * channel.stats.sampling_rate)
    channel.data = channel.data[delta_samples:channel.stats.npts]

# Corrección del número de elementos en cada canal
channels = sorted(channels, key=attrgetter('stats.npts'))
for channel in channels:
    delta = channel.stats.npts - channels[0].stats.npts
    channel.data = channel.data[0:channel.stats.npts - delta]

# Cálculo de número de muestras para la ventana
n = window * int(channels[0].stats.sampling_rate)

# Se pasan los valores de las señales a arreglos tipo numpy
for channel in channels:
    data.append(np.array(channel.data))

# Creación vector en donde a cada componente se le resta el promedio del canal
for channel in data:
    new_values = []  # Crea un arreglo auxiliar
    mean = np.mean(channel.data)  # Calcula el promedio del canal
    for sample in channel:  # Para cada elemento del canal
        value = sample - mean  # Calcula su nuevo valor
        new_values.append(value)  # Y lo agrega al arreglo auxiliar
    channel = new_values  # Cuando termina agrega el arreglo auxiliar
                                    # al arreglo con los nuevos canales.

''' TO DO: Optimizar esta función ya que muchas de las instrucciones son
    repetidas
'''
# Creación de la matriz de covarianza
for i in range(0, channels[0].stats.npts - window):
    # Agrego los elementos de cada canal correspondientes a la ventana
    # a un vector auxiliar.
    aux_x = []
    aux_y = []
    aux_z = []
    # Lleno los valores de la ventana
    for j in range(0, window):
        aux_x.append(data[0][i + j])
        aux_y.append(data[1][i + j])
        aux_z.append(data[2][i + j])
    # Calculo los elementos de la fila X
    m11 = float(np.dot(aux_x, aux_x) / n)
    m12 = float(np.dot(aux_x, aux_y) / n)
    m13 = float(np.dot(aux_x, aux_z) / n)
    x = [m11, m12, m13]

    # Calculo los elementos de la fila y
    m21 = float(np.dot(aux_y, aux_x) / n)
    m22 = float(np.dot(aux_y, aux_y) / n)
    m23 = float(np.dot(aux_y, aux_z) / n)
    y = [m21, m22, m23]

    # Calculo los elementos de la fila z
    m31 = float(np.dot(aux_z, aux_x) / n)
    m32 = float(np.dot(aux_z, aux_y) / n)
    m33 = float(np.dot(aux_z, aux_z) / n)
    z = [m31, m32, m33]
    covariance_matrix = np.matrix([x, y, z])
    print covariance_matrix
