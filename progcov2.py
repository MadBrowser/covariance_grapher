from Tkinter import *
from tkFileDialog import *
import tkMessageBox
from sys import *
from time import *
import os
from obspy.core import read
import numpy as np
import Gnuplot

class App:
	
	def __init__(self,master):
		
		frame = Frame(master)
		frame.pack()
		self.plotLabel = Label(frame, text = "GraphCov")
		self.plotLabel.grid(rowspan = 1,columnspan = 3,sticky = W+E+N+S)
		self.plotLabel.grid(row = 1, column = 1)

		self.fileNameText = Entry(frame, bd = 2,state = DISABLED)
		self.fileNameText.grid(columnspan = 1,sticky = W+E+N+S)
		self.fileNameText.grid(row=2, column = 1)

		self.buttonFile = Button(frame, text= "Abrir", command = self.openFile)
		self.buttonFile.grid(columnspan = 1,sticky = W+E+N+S)
		self.buttonFile.grid(row = 2, column = 2)

		self.label = Label(frame, text = "Intervalo")
		self.label.grid(rowspan = 1,columnspan = 3,sticky = W+E+N+S)
		self.label.grid(row = 3,column = 1)

		self.intervalText = Entry(frame, bd = 2)
		self.intervalText.grid(columnspan = 2)
		self.intervalText.grid(row=4, column = 1)

		self.plotButton = Button(frame, text = "Plot!", command = self.ploting)
		self.plotButton.grid(rowspan = 1,columnspan = 3,sticky=W+E+N+S)
		self.plotButton.grid(row=5,column=1)

	def openFile(self):
		global fileSelectString
		'''
		self.fileOpt = options = {}
		options['defaultextension'] = '*.SAC'
		options['filetypes'] = [('Todos Los Archivos', '.*'),('Archivos SAC','.SAC'),('Archivos Python', '.py'),('Archivos de Texto', '*.txt')]
		options['initialdir'] = '\\home'
		options['initialfile'] = 'temblor.SAC'
		options['parent'] = root
		options['title'] = 'Abrir Archivo'
		FILEOPENOPTIONS = dict(defaultextension='.SAC',filetypes=[('Todos los Archivos','*.*'), ('Archivo SAC','*.SAC')])
		#filename = askopenfilename(**FILEOPENOPTIONS)
		filename = askopenfilename(**self.fileOpt)'''
		fileSelect = askopenfilename()
		fileSelectString = str(fileSelect)
		fileName = os.path.split(fileSelect)[1]
		self.fileNameText.config(state = NORMAL)
		self.fileNameText.insert(0,fileName)

	def ploting(self):
		global intervalString
		intervalString = self.intervalText.get()
		if(fileSelectString == "" or intervalString == ""):
			tkMessageBox.showinfo("Problemas","Debe seleccionar un archivo e ingresar un intervalo")

		else:
			interval = int(intervalString)
			self.covariance(fileSelectString,interval)



	def covariance(self,fname, inter):
		global covarianceArray
		global timeArray
		print fname
		print inter
		st = read(fname)
		tr = st[0]
		print tr.stats
		print tr.stats.sampling_rate
		sr = int(tr.stats.sampling_rate)
		samples = len(tr)
		arrays = len(tr)/ (sr * inter)

		i = 1

		for i in range(1, arrays + 1):
			rang1 = (i - 1) * inter * sr
			rang2 = (i * inter * sr) - 1
			seg = i * inter
			vector = tr.data[rang1:rang2]
			cov = float(np.cov(vector))
			covarianceArray.append([cov,seg])

		for j in range(0,arrays,inter):
			timeArray.append(float(j))

		'''	
		print "Matriz covarianza"
		print "*****************"
		print covarianceArray
		print np.matrix(covarianceArray) '''

		g = Gnuplot.Gnuplot()
		data = Gnuplot.Data(covarianceArray, using = '2:1', with_ = "lines", title ="Covarianza")
		g.title('Grafica de Covarianza')
		g.xlabel('Intervalo de Tiempo')
		g.ylabel('Valor Covarianza')
		g.plot(data)
		tr.plot()
		#tkMessageBox.showinfo(":)","Vale, Vale!")



fileSelectString = ""
intervalString = ""
covarianceArray = []
timeArray = []
root = Tk()
root.title("Test")
app=App(root)
root.mainloop()

