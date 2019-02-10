# -*- coding: utf-8 -*-
from Tkinter import *
from utilities import createVarByTextWidget

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