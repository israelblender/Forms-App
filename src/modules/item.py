# -*- coding: Latin-1 -*-
from Tkinter import *
from utilities import createVarByTextWidget
from modules.db import DatabaseGui

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
		self.master = master
		self.eventWhenAddElement = eventWhenAddElement
		self.eventWhenDelElement = eventWhenDelElement
		self.nameFormVar = nameFormVar

		self.db = DatabaseGui()
		self.listElementThisForm = {}
		self.idTemporaryElement = 0
		self.titleFormVar = StringVar()
		self.defineFontsVars()

	def getElementsAdded(self):
		return self.listElementThisForm

	def defineFontsVars(self):
		self.font = ("Arial", 13)
		self.fontMin = ("Arial", 10)
		self.fontMax = ("Arial", 15)
		self.listOptionWidgetClass = []

	def renderAbaItem(self):
		# -------------- tabFrameFieldForm -------------
		
		Label(self.master, textvariable=self.titleFormVar, font=self.font).pack(side=TOP)

		frameBodyForm = Frame(self.master, background="lightcyan")
		frameBodyForm.pack(side=TOP, fill=BOTH, expand=True, padx=5)

		frameMenuElementsForm = Frame(frameBodyForm)#Frame que contera todos os elementos existentes
		frameMenuElementsForm.pack(side=LEFT, fill=Y, ipadx=5)
		self.frameRenderElementsForm = Frame(frameBodyForm)#Frame que contera todos os elementos escolhidos pelo usuario
		self.frameRenderElementsForm.pack(side=LEFT, fill=Y, ipadx=5, ipady=5)

		Label(frameMenuElementsForm, text="Elementos", font=self.font).pack(side=TOP)
		for element in self.db.getAllElemments(): #Mostra todos os elementos em forma de botoes para serem adicionados no formulário
			function = lambda id_element=element[0], name_element=element[1], type_element=element[2], multline=element[3], widget_tkinter=element[5]:\
			 self.actionAddElement(id_element, name_element, type_element, multline, widget_tkinter)

			Button(frameMenuElementsForm, width=15, height=2, \
				text=element[1], command=function, repeatdelay=700, \
				borderwidth=3, activebackground="lightseagreen", \
				background="darkcyan", cursor="sb_right_arrow").pack(side=TOP)
		#return frameRenderElementsForm #Aba para renderização dos elementos

	def updateTitleFormVar(self):
		self.titleFormVar.set("Crie o formulário para seu App  ( "+self.nameFormVar.get()+" ) aqui!")
		
	def actionAddElement(self, id_element, name_element, type_element, multline, widget_tkinter): #Adiciona elemento para renderizacao com evento de botao
		infoAppFrame = Frame(self.frameRenderElementsForm, background="powderblue")
		infoAppFrame.pack(side=TOP, fill=X)
		infoAppFrame.idTemporaryElement = self.idTemporaryElement

		def removeElement():# Funcao para remover o elemento da interface
			del self.listElementThisForm[infoAppFrame.idTemporaryElement]
			infoAppFrame.destroy()# Remove o frame da tela
			self.eventWhenDelElement()# Deleta o item da lista de elementos adicionados do formulario

		Button(infoAppFrame, text="X", command=removeElement, font=("Arial", 6), takefocus=False)\
		.pack(side=RIGHT, ipadx=2, padx=2)#Botao para remover o elemento

		nameElementVar = StringVar()
		nameElement = Entry(infoAppFrame, width=18, justify=CENTER, relief=FLAT, \
			textvariable=nameElementVar, font=("Agency FB", 14))
		nameElement.pack(side=LEFT, padx=10, fill=X)
		nameElementVar.set(name_element)
		nameElement.focus_force()
		nameElement.select_range(0, END)

		self.renderSampleInputElement(infoAppFrame, widget_tkinter)#Renderiza os inputs como amostra na interface
		
		#Salva na lista o id do elemento,nome da variavel controladora e o tipo de dado que sera inserido no banco
		self.listElementThisForm[self.idTemporaryElement] = {
		"id_element": id_element, 
		"name_element_var": nameElementVar, #Nome do elemento definido pelo usuario
		"type_element": type_element, #tipo do elemento definido no banco
		"info_app_frame": infoAppFrame} #Frame

		self.idTemporaryElement += 1
		self.eventWhenAddElement()

	def renderSampleInputElement(self, infoAppFrame, widget_tkinter):
		"Renderiza os inputs como amostra na interface"
		params = None
		if widget_tkinter == "entry": inputElement = Entry(infoAppFrame, takefocus=False, state="disabled", width=40, font=self.font)
		elif widget_tkinter == "text": inputElement = Text(infoAppFrame, takefocus=False, state="disabled", width=40, height=4, font=self.font)
		elif widget_tkinter == "spinbox": inputElement = Spinbox(infoAppFrame, takefocus=False, state="disabled", width=7, font=self.font)
		elif widget_tkinter == "entry-date": inputElement = Entry(infoAppFrame, takefocus=False, state="disabled", width=10, font=self.font)
		elif widget_tkinter == "entry-phone": inputElement = Entry(infoAppFrame, takefocus=False, state="disabled", width=15, font=self.font)
		elif widget_tkinter == "option-box":
			ow = OptionWidget(infoAppFrame)
			self.listOptionWidgetClass.append(ow)
			inputElement = Button(infoAppFrame, text="+", font=self.fontMax, \
				command=lambda:ow.addOption())
		if params: infoAppFrame.params = ow.getListVars()
		else: infoAppFrame.params = ""

		inputElement.pack(side=LEFT, padx=10, pady=5)

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