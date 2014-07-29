#!/usr/bin/python
#coding=utf-8
from obspy.core import read
import numpy as np
import Gnuplot
import wx, os

raw_input("ABRIR ARCHIVO")#stop para presentar

app = wx.PySimpleApp()
wildcard = 	"Archivos SAC (*.SAC)|*.SAC|" \
			"Archivos Python (*.py)|*.py|" \
        	"Archivos de texto (*.txt)|*.txt|" \
        	"All files (*.*)|*.*"
dialog = wx.FileDialog(None, "Prog_Cov", os.getcwd(), "", wildcard, wx.OPEN)
if dialog.ShowModal() == wx.ID_OK: 
    print dialog.GetFilename() 
    lol = str(dialog.GetPath())

covarianza = []
tiempo = []

st = read(lol)
tr = st[0]
print tr.stats
sr = int(tr.stats.sampling_rate) #muestra
w = int(raw_input('Ingrese Intervalo: ')) #cantidad de mediciones

cant_medi = len(tr)
cant_vect = len(tr) / (sr * w) #cantidad de vectores

i = 1

for i in range(1, cant_vect + 1):
	rang1 = (i - 1) * w * sr
	rang2 = (i * w *sr) - 1
	seg = i * w
	vect = tr.data[rang1:rang2]
	cov = float(np.cov(vect))
	covarianza.append([cov,seg])

for j in range(0,cant_vect,w):
    tiempo.append(float(j))



raw_input("MATRIZ COVARIANZA")
print "MATRIZ DE COVARIANZA"
print "**********************************"
print covarianza
print np.matrix(covarianza)
print "**********************************"
raw_input("GRAFICAR COVARIANZA")
g = Gnuplot.Gnuplot()
d1=Gnuplot.Data(covarianza, using='2:1',with_="lines", title="Covarianza")

g.title('GRAFICA DE LA COVARIANZA')
g.xlabel('Intervalo de Tiempo')
g.ylabel('Valor Covarianza')
g.plot(d1)

raw_input("GRAFICAR LA SEÑAL")
tr.plot()


raw_input("El programa a terminado. Presione una tecla para terminar.....")

