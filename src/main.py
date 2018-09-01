# -*- coding: utf-8 -*-

#Autor: Israel Gomes
#Data: 26/08/2018
from modules.db import Database
from modules.utilities import renderPhoto, savePhoto
from modules.validate import validateDate, validatePhone
#from tkMessageBox import showwarning
from ttk import Notebook
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
from random import randint

import os
from modules.report import ErrorReport

class DatabaseGui(Database):
	"""Classe destinada a avisar com interface grafica caso ocorra erro na conexao"""
	def __new__(cls):
		if not hasattr(cls, "_instance"):
			cls._instance = super(DatabaseGui, cls).__new__(cls)
			cls.instance_n = 0

		cls.instance_n += 1
		return cls._instance

	def __init__(self):
		if self.instance_n == 1:
			Database.__init__(self)

class Elements:
	def __init__(self):
		self.db = DatabaseGui()

	def getAllElemments(self):

		# retorna (id, nome, tipo, multilinha, caminho_imagem)
		all_elements = self.db.getAllElemments()

		return all_elements

class Forms:
	def __init__(self):
		self.db = DatabaseGui()

	def getAllForms(self):
		# retorna (id, nome_formulario, descricao, nome_tabela, caminho_imagem)
		all_forms = self.db.getAllInfoForms()

		return all_forms

class Interface():
	def __init__(self):
		print ("PASTA ATUAL MAIN: " +os.getcwd())
		self.errorReport = ErrorReport("logs_errors/error_db.log")
		self.db = DatabaseGui()
		if self.db.checkStatus():
			self.defineFontsVars()
			self.configWindow("1.0.0")
			self.defineVars()
			self.configWidgetsMenuOptions()
			self.configWidgetsCreateForm()
			self.configWidgetsGetApps()

			self.setWidgets()

			############################ FUNCAO TEMPORARIA APENAS PARA DESENVOLVIMENTO
			self.nextTabFrameFieldForm()
		else:
			self.errorReport.showAndSaveError(self.db.getErrorDb(), "Erro ao inicializar banco de dados")		

	def defineVars(self):
		self.frameOld = None
		self.optionVar = IntVar()
		self.nameFormVar = StringVar()
		self.pathImageFormVar = StringVar()
		self.titleFormVar = StringVar()

		self.validateDateReg = self.window.register(validateDate)
		self.validatePhoneReg = self.window.register(validatePhone)

		self.nameFormVar.trace("w", self.checkInfoAppCompleted)
		self.pathImageFormVar.trace("w", self.checkInfoAppCompleted)

		self.menuOptionsFunctions = [self.activeOptionCreateForm, self.activeOptionGetApps]
		self.listElementThisForm = {}
		self.idTemporaryElement = 0
		self.menuRightStateVar = False

	def defineFontsVars(self):
		self.font = ("Arial", 13)
		self.fontMin = ("Arial", 10)
		self.fontMax = ("Arial", 15)

	def setWidgets(self):
		self.optionVar.set(0)
		self.pathImageFormVar.set("link da imagem")
		self.rb1.invoke()#Aciona o RadioButton CreateForm para renderizar os elementos na frameCreateForm

	def configWindow(self, version):
		self.window = Tk()
		self.window.title("Forms App {}".format(version))
		self.window.geometry("900x500+150+100")
		self.window.iconbitmap( "images/imagesFormsApp/imageApp.ico")

		title = "Crie seu App, formulários, realize estatísticas, \nedite e estude seus dados com o Forms App"
		image = renderPhoto("images/imagesFormsApp/imageApp.png", (60, 60))
		Label(self.window, font=("Arial Rounded MT Bold", 15), background="thistle", foreground="chocolate", \
			text=title, padx=10, pady=10, image=image, compound=RIGHT)\
		.pack(side=TOP, fill="x", ipady=5)
		self.frameBody = Frame(self.window, background="paleturquoise")
		self.frameBody.pack(side=TOP, expand=True, fill=BOTH)

		self.menuRight = Frame(self.frameBody, background="paleturquoise", width=150)
		self.menuRight.pack(side=RIGHT, fill=Y)
		
	def configWidgetsMenuOptions(self):
		frameOptions = Frame(self.frameBody, background="paleturquoise")
		frameOptions.pack(side=LEFT, fill=Y, padx=5, pady=5)

		self.rb1 = Radiobutton(frameOptions, font=self.font, text="Novo App", variable=self.optionVar,
		value=0, indicatoron=0, width=15, height=2, command=self.actionOptions)
		self.rb1.grid(row=1, column=0)
		self.rb2 = Radiobutton(frameOptions, font=self.font, text="Todos", variable=self.optionVar,
		value=1, indicatoron=0, width=15, height=2, command=self.actionOptions)
		self.rb2.grid(row=2, column=0)

	def configWidgetsCreateForm(self):
		self.frameCreateForm = Frame(self.frameBody)

		self.framesNotebook = Notebook(self.frameCreateForm)
		self.framesNotebook.pack(expand=True, fill=BOTH)

		self.tabFrameInfoForm = Frame(self.framesNotebook)
		self.tabFrameFieldForm = Frame(self.framesNotebook)


		self.framesNotebook.add(self.tabFrameInfoForm, compound=LEFT, image=renderPhoto("images\\imagesFormsApp\\app.png", (40, 40)), sticky=W+E+N+S, text="Info App", padding='0.1i')
		self.framesNotebook.add(self.tabFrameFieldForm, compound=LEFT, image=renderPhoto("images\\imagesFormsApp\\document.png", (40, 40)), sticky=W+E+N+S, text="Item", padding='0.1i')
		self.framesNotebook.hide(self.tabFrameFieldForm)

		# -------------- tabFrameInfoForm -------------

		title = "Crie seu App aqui"
		Label(self.tabFrameInfoForm, text=title, font=self.font)\
		.grid(row=0, column=0, columnspan=5)

		Label(self.tabFrameInfoForm, text="Nome", font=self.fontMin).grid(row=1, column=0)
		inputName = Entry(self.tabFrameInfoForm, font=self.fontMin, textvariable=self.nameFormVar)
		inputName.grid(row=1, column=1, pady=10, sticky=W+E+N+S)
		#inputName.bind("<KeyPress>", self.checkInfoAppCompleted)

		Label(self.tabFrameInfoForm, text="Descrição", font=self.fontMin).grid(row=2, column=0)
		self.textWidget = Text(self.tabFrameInfoForm, pady=10, font=self.fontMin, width=50, height=3)
		self.textWidget.grid(row=2, column=1, sticky=W+E+N+S)
		self.descriptionFormVar = self.createVarByTextWidget(self.textWidget)

		self.imageWidget = Label(self.tabFrameInfoForm, padx=10, pady=10, background="lightcyan", anchor=N)
		self.imageWidget.grid(row=1, column=2, rowspan=2, sticky=W+E+N+S, padx=10, pady=10)

		Label(self.tabFrameInfoForm, padx=10, pady=10, background="lightcyan", font=self.fontMin, textvariable=self.pathImageFormVar)\
		.grid(row=3, column=1, sticky=W+E+N+S)
		Button(self.tabFrameInfoForm, font=self.fontMin, text="Procurar Imagem", command=self.actionChoiseImageForm)\
		.grid(row=3, column=2, padx=10, pady=10)

		self.buttonNext = Button(self.tabFrameInfoForm, state="disabled", font=self.fontMin, text="Prosseguir", command=self.actionNextTabFrameFieldForm)
		self.buttonNext.grid(row=4, column=1, padx=20, pady=15)

		# -------------- tabFrameFieldForm -------------

		Label(self.tabFrameFieldForm, textvariable=self.titleFormVar, font=self.font)\
		.pack(side=TOP)

		frameBodyForm = Frame(self.tabFrameFieldForm, background="lightcyan")
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
		
		#Cria opcoes especificas no meu direito para FieldForm
		self.createMenuSideForFieldForm()
		
	def checkInfoAppCompleted(self, a, b, c):#checa se todos os campos de informacoes do app foram preenchidas
		if self.nameFormVar.get() and self.pathImageFormVar.get() <> "link da imagem":
			self.buttonNext.config(state="active")
			self.titleFormVar.set("Crie o formulário para seu App( "+self.nameFormVar.get()+" ) aqui!")
		else:
			self.activeDeactivateTabFrameFieldForm()
			self.buttonNext.config(state="disabled")
			self.buttonSaveApp.config(state="disabled")

	def checkFormCompleted(self):
		if self.listElementThisForm:
			self.buttonSaveApp.config(state="active")
		else:
			self.buttonSaveApp.config(state="disabled")
		

	
	def actionAddElement(self, id_element, name_element, type_element, multline, widget_tkinter): #Adiciona elemento para renderizacao com evento de botao
		infoAppFrame = Frame(self.frameRenderElementsForm, background="powderblue")
		infoAppFrame.pack(side=TOP, fill=X)
		infoAppFrame.idTemporaryElement = self.idTemporaryElement
		def removeElement():#Funcao que remove o frame da tela e deleta o item da lista de elementos adicionados do formulario
			del self.listElementThisForm[infoAppFrame.idTemporaryElement]
			infoAppFrame.destroy()
			self.checkFormCompleted()

		Button(infoAppFrame, text="X", command=removeElement, font=("Arial", 6), takefocus=False)\
		.pack(side=RIGHT, ipadx=2, padx=2)

		nameElementVar = StringVar()
		nameElement = Entry(infoAppFrame, width=18, justify=CENTER, relief=FLAT, \
			textvariable=nameElementVar, font=("Agency FB", 14))
		nameElement.pack(side=LEFT, padx=10, fill=X)
		nameElementVar.set(name_element)
		nameElement.focus_force()
		nameElement.select_range(0, END)

		self.viewElement(infoAppFrame, widget_tkinter)
		
		#Salva na lista o id do elemento,nome da variavel controladora e o tipo de dado que sera inserido no banco
		self.listElementThisForm[self.idTemporaryElement] = (id_element, nameElementVar, type_element, infoAppFrame)
		self.idTemporaryElement += 1
		self.checkFormCompleted()

	def viewElement(self, infoAppFrame, widget_tkinter):
		"Apenas renderiza os elementos na tela sem mais configuracoes"
		
		if widget_tkinter == "entry": inputElement = Entry(infoAppFrame, takefocus=False, state="disabled", width=40, font=self.font)
		elif widget_tkinter == "text": inputElement = Text(infoAppFrame, takefocus=False, state="disabled", width=40, height=4, font=self.font)

		elif widget_tkinter == "spinbox": inputElement = Spinbox(infoAppFrame, takefocus=False, state="disabled", width=7, font=self.font)
		elif widget_tkinter == "entry-date": inputElement = Entry(infoAppFrame, takefocus=False, state="disabled", width=10, font=self.font)
		elif widget_tkinter == "entry-phone": inputElement = Entry(infoAppFrame, takefocus=False, state="disabled", width=15, font=self.font)

		inputElement.pack(side=LEFT, padx=10, pady=10)

		return inputElement

	def renderElement(self, infoAppFrame, widget_tkinter):
		"Renderiza os elementos na tela com configurações de variáveis"
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
			inputElementVar = self.createVarByTextWidget(inputElement)

		inputElement.pack(side=LEFT, padx=10, pady=10)

		return (inputElement, inputElementVar)

	def createVarByTextWidget(self, textWidget):
		def funcSet(value):
			textWidget.delete("0.0", END)
			textWidget.insert("0.0", value)
		return type("StringVar", (), {"set": staticmethod(funcSet), "get": staticmethod(lambda: textWidget.get("0.0", END))})

	def actionChoiseImageForm(self):
		path_origin = tkFileDialog.askopenfilename(initialdir = "/",title = "Selecione o Arquivo", filetypes = (("Arquivos jpeg", "*.jpg"), ("Arquivos png", "*.png"),("Todos arquivos", "*.*")))
		if path_origin:
			file_name = os.path.basename(path_origin)
			self.pathImageFormVar.set("images/iconsApps/"+file_name)

			path_origin = path_origin.encode("latin-1")
			path_destiny = ("images/iconsApps/"+file_name).encode("latin-1")
			
			print(path_origin, path_destiny, type(savePhoto))

			savePhoto(path_origin, path_destiny, (100, 100))
			image = renderPhoto(path_destiny, (100, 100))
			self.imageWidget["image"] = image
			self.imageWidget["background"] = "SystemButtonFace"

	def actionNextTabFrameFieldForm(self):
		"Salva o app na db e pula para a proxima aba"
		#self.nameFormVar.set("Eventos Mensais")
		#self.textWidget.insert("0.0", "Eventos e palestrar de tecnologia que estão perto de ocorrer no ano de 2018.")
		self.nextTabFrameFieldForm()

	def cleanInfoApp(self):
		self.nameFormVar.set("")
		self.pathImageFormVar.set("")
		self.descriptionFormVar.set("")

	def cleanFieldForm(self):
		for element in self.listElementThisForm.values():
			element[-1].destroy()

	def saveAll(self):
		nameTableFormated = self.formatNameTable(self.nameFormVar.get())+str(randint(1, 1000000))
		appId = self.saveApp(nameTableFormated)#Salva as informacoes do App
		self.saveFieldsForm(appId)#Salva as ordens dos elementos no formulario
		self.saveTableForm(nameTableFormated)#Salva a tabela para inserir os futuros itens

		self.cleanInfoApp()#Limpa todos os campos preenchimentos de Info App
		self.cleanFieldForm()#Remove todos os Itens adicionados na criacao do formulario
		self.activeDeactivateTabFrameFieldForm()#Torna a aba Item invisivel novamente

	def saveApp(self, nameTableFormated):
		"Salva o app no banco de dados"
		
		self.db.saveRecordApp(
			self.nameFormVar.get(), 
			self.textWidget.get("0.0", END), 
			nameTableFormated, 
			self.pathImageFormVar.get())

		return self.db.getIdOfLastRecordInApps()[0]

	def saveFieldsForm(self, appId):
		#(id_element, nameElementVar, type_element, inputElement)
		index_posicao = 0
		indexTemps = list(self.listElementThisForm)
		indexTemps.sort()

		for indexTemp in indexTemps:
			id_element, nameElementVar, type_element, _ = self.listElementThisForm.get(indexTemp)
			#salvar em saveFieldApp ---> id_formulario, id_elemento, titulo, texto_ajuda, index_posicao
			
			self.db.saveFieldApp(appId, id_element, str(nameElementVar.get()), "", index_posicao)
			index_posicao += 1

	def saveTableForm(self, nameTableFormated):
		try:
			fields_types = map(lambda element: self.formatNameColumn(element[1].get())+\
			" "+element[2], self.listElementThisForm.values())
			self.db.saveTableApp(nameTableFormated, fields_types)
		except Exception as error:
			self.errorReport.showAndSaveError(error.message, "Erro ocorreu durante salvamento da tabela")

	def createMenuSideForFieldForm(self):
		if not self.menuRightStateVar:
			self.menuRight["background"] = "red"
			self.menuRightCreateForm = Frame(self.menuRight)
			self.menuRightCreateForm.pack(side=TOP, padx=10, pady=10)

			self.buttonSaveApp = Button(self.menuRightCreateForm, command=self.saveAll, \
				font=self.font, text="Salvar App")
			self.buttonSaveApp.pack(side=TOP, ipadx=10)
		self.menuRightStateVar = True

	def hideMenuFieldForm(self): self.menuRightCreateForm.forget()

	def showMenuFieldForm(self): self.menuRightCreateForm.pack(side=TOP, padx=10, pady=10)

	def nextTabFrameFieldForm(self):
		self.activeDeactivateTabFrameFieldForm()
		self.framesNotebook.select(self.tabFrameFieldForm)

	def activeDeactivateTabFrameFieldForm(self): self.framesNotebook.hide(self.tabFrameFieldForm)

	def formatNameColumn(self, name_field):
		name_formated = "_".join(name_field.lower().split(" ")[0:2])
		return name_formated

	def formatNameTable(self, name_form):
		name_formated = "_".join(name_form.lower().split(" ")[0:2])
		return name_formated

	def configWidgetsGetApps(self): # Configura todos os widgets que pertencem ao frame que mostra todos os apps e forms
		self.frameGetApps = Frame(self.frameBody)

		self.frameAbasGetApps = Notebook(self.frameGetApps)
		self.frameAbasGetApps.pack(side=TOP, fill=BOTH)

		frameApp = Frame(self.frameAbasGetApps)
		frameInfoApp = Frame(frameApp)
		frameInfoApp.pack(side=TOP, fill=BOTH)
		frameFieldsApp = Frame(frameApp)
		frameFieldsApp.pack(side=TOP, fill=BOTH)

		for idApp, nomeApp, pathImage in self.db.getAllInfoForms("id", "nome_formulario", "caminho_imagem"):
			image = renderPhoto(pathImage, (35, 35))
			self.frameAbasGetApps.add(frameApp, compound=LEFT, image=image, text=nomeApp, sticky=W+E+N+S)
			break

	# def generateTabsApps(self):
	# 	self.listTabsApps = []
	# 	for app_info in self.db.getAllInfoForms("id", "nome_formulario"):
	# 		self.listTabsApps.append(self.generateTab(  ))

	# def activeTabApp(self, name_form, description, name_table, path_image):
		
	# 	self.frameInfoApp
	# 	self.frameFieldsApp

	def actionOptions(self):
		if self.frameOld: self.frameOld.forget()
		self.frameOld = self.menuOptionsFunctions[self.optionVar.get()]()

	def activeOptionCreateForm(self):
		self.frameCreateForm.pack(side=LEFT, expand=True, fill=BOTH)
		self.showMenuFieldForm()
		return self.frameCreateForm

	def activeOptionGetApps(self):
		self.frameGetApps.pack(side=LEFT, expand=True, fill=BOTH)
		self.hideMenuFieldForm()
		return self.frameGetApps

if  __name__ == "__main__":
	elem = Elements()
	form = Forms()
	inter = Interface()
	if inter.db.checkStatus(): inter.window.mainloop()