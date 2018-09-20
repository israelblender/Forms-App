# -*- coding: cp1252 -*-
from Tkinter import *
from utilities import createVarByTextWidget
from modules.db import Database

class ItemWidget(Frame):
	def __init__(self, master, fields_show):
		"VALORES ACEITOS PARA fields_show: entry, entry-date, entry-phone, spinbox, text, option "
		self.fields_show = fields_show
		super(frame, self).__init__(self, master)
		self.createItem(master)
		self.createAttrs()

	def setValues():
		pass

	def createAttrs(self, attrs):
		self.attrs = dict([{field_name: {
			"field_show":field_show, 
			"stringvar":StringVar(),
			"index":index}}	for index, field_name, field_show in enumerate(attrs)])

		print "ATTRS: ", self.attrs

	def createItem(self, master):
		frameItem = Frame(master)
		frameItem.pack(padx=10, pady=10)

		#for 
		#self.createWidget()

	def createWidget(self, master, type_widget, stringvar):
		if type_widget == "title":
			Label(master, textvariable=stringvar).pack(side=TOP)

		elif type_widget == "text":
			text = Text(master)
			text.pack(side=TOP)
			text.config(textvariable=createVarByTextWidget(text))#createVarByTextWidget adiciona metodo set e get de StringVar
	
	#def renderElement(self, infoAppFrame, widget_tkinter):
		"Renderiza os titulos de elementos na tela com configurações de variáveis"
		inputElementVar = None
		if widget_tkinter == "entry":
			inputElementVar = StringVar()
			inputElement = Entry(infoAppFrame, width=40, textvariable=inputElementVar, font=self.font)
		
		elif widget_tkinter == "entry-date":
			inputElementVar = StringVar()
			inputElement = Entry(infoAppFrame, width=10, textvariable=inputElementVar, font=self.font)
			inputElement.config(validate="key", validatecommand=(self.validadeDateReg, '%i','%P', '%S', '%s'))

		elif widget_tkinter == "entry-phone":
			inputElementVar = StringVar()
			inputElement = Entry(infoAppFrame, width=15, textvariable=inputElementVar, font=self.font)
			inputElement.config(validate="key", validatecommand=(self.validadePhoneReg, '%i','%P', '%S', '%s'))

                elif widget_tkinter == "spinbox":
			inputElementVar = StringVar()
			inputElement = Spinbox(infoAppFrame, width=5, textvariable=inputElementVar, font=self.font)
		
		elif widget_tkinter == "text":
			inputElement = Text(infoAppFrame, width=40, height=4, font=self.font)
			inputElementVar = createVarByTextWidget(inputElement)

		elif widget_tkinter == "option":
			pass

		inputElement.pack(side=LEFT, padx=10, pady=10)

class OptionWidget:
	def __init__(self, master):
		self.master = master
		self._listVars = []

	def addOption(self):
		inputElementVar = StringVar()
		frameOption = Frame(self.master, width=15,\
			height=2, relief=RAISED, border=3)
		frameOption.pack(side=LEFT, padx=10)
		Entry(frameOption, textvariable=inputElementVar, relief=FLAT, 
			width=15, justify=CENTER).pack(padx=5, pady=3)
		self._listVars.append(inputElementVar)

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
		#Frame que contem todos os tipos de elementos disponíveis no banco
		frameMenuElementsForm = Frame(frameBodyForm)
		frameMenuElementsForm.pack(side=LEFT, fill=Y, ipadx=5)
		#Frame que contem todos os elementos escolhidos pelo usuario
		frameElementsForm = Frame(frameBodyForm)
		frameElementsForm.pack(side=LEFT, fill=Y, ipadx=5, ipady=5)

		Label(frameMenuElementsForm, text="Elementos", font=self.font).pack(side=TOP)
		for id_element, name_element, type_element, multline, path_image, widget_tkinter in self.db.getAllElemments(): #Mostra todos os elementos em forma de botoes para serem adicionados no formulário
			function = lambda \
			id_element=id_element, \
			name_element=name_element, \
			type_element=type_element, \
			multline=multline, \
			widget_tkinter=widget_tkinter:\
			 self.actionAddElement(frameElementsForm, id_element, name_element, type_element, multline, widget_tkinter)

			Button(frameMenuElementsForm, width=15, height=2, \
				text=name_element, command=function, repeatdelay=700, \
				borderwidth=3, activebackground="lightseagreen", \
				background="darkcyan", cursor="sb_right_arrow").pack(side=TOP)
		#return frameRenderElementsForm #Aba para renderização dos elementos
		return frame

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
		if widget_tkinter == "entry": 			inputElement = Entry(master, state="disabled", relief=FLAT, width=40)
		elif widget_tkinter == "text": 			inputElement = Text(master, state="disabled", relief=FLAT, width=40, height=4)
		elif widget_tkinter == "spinbox": 		inputElement = Spinbox(master, state="disabled", relief=FLAT, width=7)
		elif widget_tkinter == "entry-date": 	inputElement = Entry(master, state="disabled", relief=FLAT, width=10)
		elif widget_tkinter == "entry-phone": 	inputElement = Entry(master, state="disabled", relief=FLAT, width=15)
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