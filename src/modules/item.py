# -*- coding: utf-8 -*-
from Tkinter import *
from utilities import createVarByTextWidget
from modules.db import Database


class OptionWidget:
	def __init__(self, master):
		self.master = master

		self._listVars = []

	def addOption(self, event=None):
		inputElementVar = StringVar()
		frameOption = Frame(self.master, width=15, height=2, relief=RAISED, border=2)
		frameOption.pack(side=TOP, padx=10, pady=5)
		input = Entry(frameOption, textvariable=inputElementVar, relief=FLAT, \
			width=15, justify=CENTER)
		input.pack(side=LEFT, padx=5, pady=3)
		input.focus_force()
		input.bind("<Return>", self.addOption)

		buttonDestroy = Button(frameOption, font=("Arial", 5), text="X", command=lambda frame_option=frameOption, element_var=inputElementVar: self.removeOption(frame_option, element_var), takefocus=False)\
		.pack(side=RIGHT, ipadx=0, padx=0)

		self._listVars.append(inputElementVar)

	def removeOption(self, element, elementVar):
		element.destroy()
		self._listVars.remove(elementVar)

	def getListVars(self):
		return self._listVars

class TabItem:
	def __init__(self, master, nameFormVar, eventWhenAddElement=None, eventWhenDelElement=None):
		"""
		master				: Frame que contem a aba Item
		nameFormVar			: Variável controladora do nome da aplicacao definida na aba InfoApp
		eventWhenAddElement	: Evento que será chamado quando adicionar um elemento
		eventWhenDelElement	: Evento que será chamado quando remover um elemento"""

		self.master = master
		self.nameFormVar = nameFormVar
		self.eventWhenAddElement = eventWhenAddElement
		self.eventWhenDelElement = eventWhenDelElement
		
		self.db = Database()#Cria instancia do banco de dados
		self.defineVars()# Define as variaveis globais da classe
		self.defineFonts()# Define as variaveis de fontes padroes da aplicacao

	def getElementsAdded(self):
		"Retorna todos elementos adicionados pelo usuário"
		return self.listElementThisForm

	def defineVars(self):
		self.listOptionWidgetClass = []
		self.listElementThisForm = {}
		self.idTemporaryElement = 0
		self.titleFormVar = StringVar()

	def defineFonts(self):
		"Variaveis de fonte globais para estética padrão da aplicação"
		self.font = ("Arial", 13)
		self.fontMin = ("Arial", 10)
		self.fontMax = ("Arial", 15)

	def createAba(self):
		"Cria a aba Item para criacao de formulario"
		frame = Frame(self.master)
		Label(frame, textvariable=self.titleFormVar, font=self.font).pack(side=TOP)
		# Frame que contem os frames de menu de tipos de elementos e de elementos escolhidos pelo usuario
		frameBodyForm = Frame(frame, background="lightcyan")
		frameBodyForm.pack(side=TOP, fill=BOTH, expand=True, padx=5)

		self.generateMenuElements(frameBodyForm)
		return frame

	def generateMenuElements(self, master):
		"Mostra todos os elementos em forma de botoes para serem adicionados no formulário"
		#Frame que contem todos os tipos de elementos disponíveis no banco
		frameMenuElementsForm = Frame(master)
		frameMenuElementsForm.pack(side=LEFT, fill=Y, ipadx=5)

		Label(frameMenuElementsForm, text="Elementos", font=self.font).pack(side=TOP, pady=10)
		
		#Frame que contem todos os elementos escolhidos pelo usuario
		frameElementsForm = Frame(master)
		frameElementsForm.pack(side=LEFT, fill=Y, ipadx=5, ipady=5)

		for id_element, name_element, type_element, multline, path_image, widget_tkinter in self.db.getAllElemments():
			function = lambda \
			id_element=id_element, \
			name_element=name_element, \
			type_element=type_element, \
			multline=multline, \
			widget_tkinter=widget_tkinter:\
			 self.actionAddElement(frameElementsForm, id_element, name_element, type_element, multline, widget_tkinter)

			Button(frameMenuElementsForm, width=15, height=2, \
				text=name_element, command=function, repeatdelay=700, \
				borderwidth=3, activebackground="mediumaquamarine", \
				background="cadetblue", cursor="sb_right_arrow").pack(side=TOP)

	def updateTitleFormVar(self):
		self.titleFormVar.set("Crie o formulário para seu App  ( "+self.nameFormVar.get()+" ) aqui!")
		
	def actionAddElement(self, master, id_element, name_element, type_element, multline, widget_tkinter): #Adiciona elemento para renderizacao com evento de botao
		"Aciona quando adicionado algum elemento na interface por meio de algum evento"
		infoAppFrame = Frame(master, background="powderblue")
		infoAppFrame.pack(side=TOP, fill=X)
		infoAppFrame.idTemporaryElement = self.idTemporaryElement

		def removeElement():# Funcao para remover o elemento da interface
			del self.listElementThisForm[infoAppFrame.idTemporaryElement]# Deleta o item da lista de elementos adicionados do formulario
			infoAppFrame.destroy()# Remove o frame da tela
			self.eventWhenDelElement()# Funcao que sera chamada apos remocao do elemento

		Button(infoAppFrame, text="X", command=removeElement, font=("Arial", 6), takefocus=False)\
		.pack(side=RIGHT, ipadx=2, padx=2)#Botao para remover o elemento

		nameElementVar = self.renderLabelSampleElement(infoAppFrame, name_element)#Cria o Label do elemento e retorna a variável controladora de saída

		self.renderInputSampleElement(infoAppFrame, widget_tkinter)#Cria os inputs como amostra na interface
		
		#Salva na lista os tipos de dados que serão inseridos no banco
		self.listElementThisForm[self.idTemporaryElement] = {
		"id_element": id_element, # Identificacao do elemento
		"name_element_var": nameElementVar, # Nome do elemento definido pelo usuario
		"type_element": type_element, # Tipo do elemento(SQL) definido dentro banco
		"info_app_frame": infoAppFrame} # Frame

		self.idTemporaryElement += 1
		self.eventWhenAddElement()

	def renderLabelSampleElement(self, master, name_element):
		"Cria o Label do elemento e retorna a variável controladora de saída"
		nameElementVar = StringVar()
		nameElement = Entry(master, width=18, justify=CENTER, \
			textvariable=nameElementVar, font=("Agency FB", 14))
		nameElement.pack(side=LEFT, padx=10, fill=X)
		nameElementVar.set(name_element)
		nameElement.focus_force()
		nameElement.select_range(0, END)
		return nameElementVar

	def renderInputSampleElement(self, master, widget_tkinter):
		"Cria os inputs como amostra na interface"
		params = False
		
		if widget_tkinter == "entry":
			inputElement = Entry(master, relief=FLAT, width=40)
			inputElement.insert(0, "Texto de uma linha")
			inputElement.config(state="disabled")
		elif widget_tkinter == "text":
			inputElement = Text(master, relief=FLAT, width=40, height=4)
			inputElement.insert("0.0", "Texto multi-linha")
			inputElement.config(state="disabled")
		elif widget_tkinter == "spinbox":

			inputElement = Spinbox(master, relief=FLAT, width=7)
			inputElement.insert(0, "0")
			inputElement.config(state="disabled")
		elif widget_tkinter == "entry-date":
			inputElement = Entry(master, relief=FLAT, width=10)
			inputElement.insert(0, "     /    /  ")
			inputElement.config(state="disabled")
		elif widget_tkinter == "entry-phone":
			inputElement = Entry(master, relief=FLAT, width=15)
			inputElement.insert(0, "(99) 99999-9999")
			inputElement.config(state="disabled")
		elif widget_tkinter == "option-box":
			ow = OptionWidget(master)
			self.listOptionWidgetClass.append(ow)
			inputElement = Button(master, text="+", font=self.fontMax, \
				command=lambda:ow.addOption())
			params = True
			master.params = ow.getListVars()

		if not params: master.params = ""

		inputElement.pack(side=LEFT, padx=10, pady=5)
		inputElement.config(takefocus=False, font=self.font)

		return inputElement

	def cleanFieldForm(self):
		for element in self.listElementThisForm.values():
			element.get("info_app_frame").destroy()
		self.listElementThisForm = {}

if __name__ == "__main__":
	window = Tk()
	window.geometry("800x400+150+150")
	window.title("Teste ItemWidget")

	ItemWidget(window, ("title", "message")).pack(side=TOP)

	window.mainloop()