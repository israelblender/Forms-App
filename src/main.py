# -*- coding: utf-8 -*-

#Autor: Israel Gomes
#Data: 26/08/2018
from modules.db import Database, DatabaseGui
from modules.utilities import renderPhoto, savePhoto, createVarByTextWidget
from modules.item import TabItem, ItemWidget
from modules.validate import validateDate, validatePhone
#from tkMessageBox import showwarning
from ttk import Notebook
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
from random import randint

import os
from modules.report import ErrorReport

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
		print ("PASTA ATUAL PRINCIPAL: " +os.getcwd())
		self.errorReport = ErrorReport("logs_errors/error_db.log")
		self.db = DatabaseGui()
		if self.db.checkStatus():
			self.defineFontsVars()
			self.window = self.createWindow("1.0.0")

			self.defineVars()
			self.configTitleLogo(self.window)

			frameBody = Frame(self.window, background="paleturquoise")
			frameBody.pack(side=TOP, expand=True, fill=BOTH)
	
			self.createWidgetsMenuOptions	(frameBody)
			self.createMenuRight			(frameBody)
			self.createWidgetsCreateForm	(frameBody)
			self.createWidgetsGetApps		(frameBody)

			#self.checkInfoAppCompleted()#Checa se as informações da aba InfoApp estao todas preenchidas
			self.setDefaultValuesWidgets()#Preeche com valores padroes da aplicacao

			############################ CHAMADAS TEMPORARIAS APENAS PARA DESENVOLVIMENTO
			self.setPersonValuesWidgets()#Simula preenchimento de valores personalizados
			self.nextTabFrameFieldForm()
		else:
			self.errorReport.showAndSaveError(self.db.getErrorDb(), "Erro ao inicializar banco de dados")		

	def setPersonValuesWidgets(self):
		"FUNCAO DESENVOLVEDOR: Preenche com valores personalizados"
		self.nameFormVar.set("Eventos Mensais")
		self.textWidget.insert("0.0", "Eventos e palestrar de tecnologia que estão perto de ocorrer no ano de 2018.")
		self.actionChoiseImageForm("images/iconsApps/video.png")#Define a imagem que representara o app
		self.rb1.invoke()
		#self.cleanInfoApp()

	def setDefaultValuesWidgets(self):
		"Preeche com valores padroes da aplicacao"
		self.optionVar.set(0)
		self.pathImageFormVar.set("link da imagem")
		self.rb1.invoke()#Aciona o RadioButton CreateForm para renderizar os elementos na frameCreateForm

	def defineVars(self):
		self.optionVar = IntVar()
		self.nameFormVar = StringVar()
		self.pathImageFormVar = StringVar()
		self.optionsExist = False# Variavel usada na condicional para salvar no banco caso existam

		self.validateDateReg = self.window.register(validateDate)
		self.validatePhoneReg = self.window.register(validatePhone)

		self.nameFormVar.trace("w", self.checkInfoAppCompleted)
		self.pathImageFormVar.trace("w", self.checkInfoAppCompleted)

		self.menuOptionsFunctions = [self.activeOptionCreateForm, self.activeOptionGetApps]
		
		self.frameOld = None
		self.menuRightStateVar = False

	def defineFontsVars(self):
		self.font = ("Arial", 13)
		self.fontMin = ("Arial", 10)
		self.fontMax = ("Arial", 15)

	def createWindow(self, version):
		window = Tk()
		window.title("Forms App {}".format(version))
		window.geometry("900x500+150+100")
		window.iconbitmap( "images/imagesFormsApp/imageApp.ico")
		return window

	def configTitleLogo(self, master):
		title = "Crie seu App, formulários, realize estatísticas, \nedite e estude seus dados com o Forms App"
		image = renderPhoto("images/imagesFormsApp/imageApp.png", (60, 60))
		Label(master, font=("Arial Rounded MT Bold", 15), background="thistle", foreground="chocolate", \
			text=title, padx=10, pady=10, image=image, compound=RIGHT)\
		.pack(side=TOP, fill="x", ipady=5)

	def createMenuRight(self, master):
		self.menuRight = Frame(master, background="paleturquoise", width=150)
		self.menuRight.pack(side=RIGHT, fill=Y)
		
	def createWidgetsMenuOptions(self, master):
		frameOptions = Frame(master, background="paleturquoise")
		frameOptions.pack(side=LEFT, fill=Y, padx=5, pady=5)

		self.rb1 = Radiobutton(frameOptions, font=self.font, text="Novo App", variable=self.optionVar,
		value=0, indicatoron=0, width=15, height=2, command=self.actionOptions)
		self.rb1.grid(row=1, column=0)
		self.rb2 = Radiobutton(frameOptions, font=self.font, text="Todos", variable=self.optionVar,
		value=1, indicatoron=0, width=15, height=2, command=self.actionOptions)
		self.rb2.grid(row=2, column=0)

	def createWidgetsCreateForm(self, master):
		self.frameCreateForm = Frame(master)

		self.framesNotebook = Notebook(self.frameCreateForm)
		self.framesNotebook.pack(expand=True, fill=BOTH)

		self.tabFrameInfoForm = Frame(self.framesNotebook)
		self.tabFrameFieldForm = Frame(self.framesNotebook)


		self.framesNotebook.add(self.tabFrameInfoForm, compound=LEFT, image=renderPhoto("images\\imagesFormsApp\\app.png", (40, 40)), sticky=W+E+N+S, text="Info App", padding='0.1i')
		self.framesNotebook.add(self.tabFrameFieldForm, compound=LEFT, image=renderPhoto("images\\imagesFormsApp\\document.png", (40, 40)), sticky=W+E+N+S, text="Item", padding='0.1i')
		self.framesNotebook.hide(self.tabFrameFieldForm)

		self.renderAbaInfoApp()

		self.tabItem = TabItem(master=self.tabFrameFieldForm, nameFormVar=self.nameFormVar, eventWhenAddElement=self.checkFormCompleted, eventWhenDelElement=self.checkFormCompleted)
		self.tabItem.renderAbaItem()

		#Cria opcoes especificas no meu direito para FieldForm
		self.createMenuSideForFieldForm()
		
	def renderAbaInfoApp(self):
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
		self.descriptionFormVar = createVarByTextWidget(self.textWidget)

		self.imageWidget = Label(self.tabFrameInfoForm, padx=10, pady=10, background="lightcyan", anchor=N)
		self.imageWidget.grid(row=1, column=2, rowspan=2, sticky=W+E+N+S, padx=10, pady=10)

		Label(self.tabFrameInfoForm, padx=10, pady=10, background="lightcyan", font=self.fontMin, textvariable=self.pathImageFormVar)\
		.grid(row=3, column=1, sticky=W+E+N+S)
		Button(self.tabFrameInfoForm, font=self.fontMin, text="Procurar Imagem", command=self.actionChoiseImageForm)\
		.grid(row=3, column=2, padx=10, pady=10)

		self.buttonNext = Button(self.tabFrameInfoForm, state="disabled", font=self.fontMin, text="Prosseguir", command=self.actionNextTabFrameFieldForm)
		self.buttonNext.grid(row=4, column=1, padx=20, pady=15)
	
	def checkInfoAppCompleted(self, a=None, b=None, c=None):#checa se todos os campos de informacoes do app foram preenchidas
		
		if self.nameFormVar.get() and self.pathImageFormVar.get() != "link da imagem":
			self.buttonNext.config(state="active")
			try: self.tabItem.updateTitleFormVar()
			except: pass
		else:
			self.activeDeactivateTabFrameFieldForm()
			self.buttonNext.config(state="disabled")
			self.buttonSaveApp.config(state="disabled")

	def checkFormCompleted(self):
		if self.tabItem.getElementsAdded(): self.buttonSaveApp.config(state="active")
		else: self.buttonSaveApp.config(state="disabled")

	def renderInputElement(self, infoAppFrame, widget_tkinter):
		"Renderiza os inputs dos elementos na tela para input do usuario"
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

		elif widget_tkinter == "option-box":
			pass			

		inputElement.pack(side=LEFT, padx=10, pady=10)

		return (inputElement, inputElementVar)

	def actionChoiseImageForm(self, path_origin=None):
		"Escolhe imagem atravez de acao ou atraves de chamada call"
		if path_origin == "": 
			self.imageWidget["image"] = None
			self.imageWidget["background"] = "grey"
			self.pathImageFormVar.set("")

		elif path_origin == None: path_origin = tkFileDialog.askopenfilename(initialdir = "/",title = "Selecione o Arquivo", filetypes = (("Arquivos jpeg", "*.jpg"), ("Arquivos png", "*.png"),("Todos arquivos", "*.*")))
		
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
		self.nextTabFrameFieldForm()

	def cleanInfoApp(self):
		self.nameFormVar.set("")
		self.descriptionFormVar.set("")
		#self.actionChoiseImageForm("")

	def saveAll(self):
		nameTableFormated = self.formatName(self.nameFormVar.get())+str(randint(1, 1000000))
		#appId = self.saveApp(nameTableFormated)#Salva as informacoes do App
		self.saveFieldsForm(2154)#Salva a ordem dos elementos no formulario
		#self.saveTableForm(nameTableFormated)#Salva a tabela para inserir os futuros itens

		self.cleanInfoApp()#Limpa todos os campos preenchimentos de Info App
		self.tabItem.cleanFieldForm()#Remove todos os Itens adicionados na criacao do formulario
		self.activeDeactivateTabFrameFieldForm()#Torna a aba Item invisivel novamente

	def saveApp(self, nameTableFormated):
		"Salva as informacoes do app no banco de dados"
		self.db.saveRecordApp(
			self.nameFormVar.get(), 
			self.textWidget.get("0.0", END), 
			nameTableFormated, 
			self.pathImageFormVar.get())

		return self.db.getIdOfLastRecordInApps()[0]

	def saveFieldsForm(self, appId):
		"Salva a ordem dos elementos no formulario"
		#(id_element, nameElementVar, type_element, inputElement)
		index_posicao = 0
		indexTemps = list(self.tabItem.getElementsAdded())
		indexTemps.sort()

		for indexTemp in indexTemps:
			element = self.tabItem.getElementsAdded().get(indexTemp)
			#id_element, name_element_var, type_element, info_app_frame = self.tabItem.getElementsAdded().get(indexTemp)
			#salvar em saveFieldApp ---> id_formulario, id_elemento, titulo, texto_ajuda, index_posicao
			print "PARAMS: ", element.get("info_app_frame").params
			self.db.saveFieldApp(
				id_form=appId,
				id_element=element.get("id_element"), 
				title=element.get("name_element_var").get(), #.encode("utf-8")
				text_help="", 
				index_position=element.get("info_app_frame").idTemporaryElement, 
				params=[param.get() for param in element.get("info_app_frame").params])

			if self.optionsExist:
				self.db.saveOptionsElements()

			index_posicao += 1

	def saveTableForm(self, nameTableFormated):
		"Salva a tabela criada pelo usuario implicitamente"
		try:
			fields_types = [
			self.formatName(element.get("name_element_var").get())+" "+element.get("type_element") \
				for element in self.tabItem.getElementsAdded().values()]

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

	def formatName(self, name_field):
		"Formata nomes de colunas e tabelas"
		name_formated = "_".join(name_field.lower().split(" ")[0:2])
		return name_formated

	def createWidgetsGetApps(self, frame): # Configura todos os widgets que pertencem ao frame que mostra todos os apps e forms
		self.frameGetApps = Frame(frame)

		self.frameAbasGetApps = Notebook(self.frameGetApps)
		self.frameAbasGetApps.pack(side=TOP, expand=True, fill=BOTH)

		for idApp, nomeApp, descricao, pathImage in self.db.getAllInfoForms("id", "nome_formulario", "descricao", "caminho_imagem"):
			frameApp = Frame(self.frameAbasGetApps)

			image = renderPhoto(pathImage, (30, 30))
			self.frameAbasGetApps.add(frameApp, compound=LEFT, image=image, text=nomeApp, sticky=W+E+N+S)

			headerFrame = Frame(frameApp)
			headerFrame.pack(side=TOP)

			buttonsAppFrame = Frame(headerFrame)
			buttonsAppFrame.pack(side=RIGHT)

			Button(buttonsAppFrame, text="Configurações").pack(side=TOP, padx=10, pady=5)
			Button(buttonsAppFrame, text="Adicionar Item").pack(side=TOP, padx=10, pady=5)

			infoAppFrame = LabelFrame(headerFrame, text="Informações do App")
			infoAppFrame.pack(side=LEFT, fill=X, padx=10, pady=10, ipadx=10, ipady=10)

			self.nameAppVar = StringVar()
			self.aboutAppVar = StringVar()
			Label(infoAppFrame, textvariable=self.nameAppVar, font=self.font, foreground="lightcoral").pack(side=TOP, expand=True, fill=BOTH)
			Label(infoAppFrame, textvariable=self.aboutAppVar).pack(side=TOP, expand=True, fill=BOTH)
			
			self.nameAppVar.set(nomeApp)
			self.aboutAppVar.set(descricao)

			itemsFrame = Frame(frameApp, background="red")
			itemsFrame.pack(side=TOP, expand=True, fill=BOTH)



			#break


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