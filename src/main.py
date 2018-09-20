# -*- coding: utf-8 -*-

#Autor: Israel Gomes
#Data: 26/08/2018
from modules.db import Database
from modules.utilities import renderPhoto, createVarByTextWidget, formatName
from modules.item import TabItem, ItemWidget
from modules.app import TabInfoApp
from modules.validate import validateDate, validatePhone
#from tkMessageBox import showwarning
from ttk import Notebook
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
from random import randint

from os import getcwd
from modules.report import ErrorReport

class Elements:
	def __init__(self):
		self.db = Database()

	def getAllElemments(self):

		# retorna (id, nome, tipo, multilinha, caminho_imagem)
		all_elements = self.db.getAllElemments()

		return all_elements

class Forms:
	def __init__(self):
		self.db = Database()

	def getAllForms(self):
		# retorna (id, nome_formulario, descricao, nome_tabela, caminho_imagem)
		all_forms = self.db.getAllInfoForms()

		return all_forms

class Interface():
	def __init__(self):
		print ("PASTA ATUAL PRINCIPAL: " +getcwd())
		self.errorReport = ErrorReport("logs_errors/error_db.log")
		self.db = Database()
		if self.db.checkStatus():
			self.defineFonts()# Define as variaveis de fontes padroes da aplicacao
			self.window = self.createWindow("1.0.0")

			self.defineVars()# Define as variaveis globais da classe
			self.configTitleLogo(self.window)

			frameBody = Frame(self.window, background="paleturquoise")
			frameBody.pack(side=TOP, expand=True, fill=BOTH)
	
			self.createWidgetsMenuOptions	(frameBody)
			self.createMenuRight			(frameBody)
			self.createWidgetsNewApp		(frameBody)# Cria self.tabInfoApp e self.tabItem
			self.createWidgetsGetApps		(frameBody)

			self.tabInfoApp.setDefaultValuesWidgets()#Preeche com valores padroes da aplicacao

			############################ CHAMADAS TEMPORARIAS APENAS PARA DESENVOLVIMENTO
			self.tabInfoApp.setPersonValuesWidgets()#Simula preenchimento de valores personalizados
			self.nextTabFrameItem()
			self.rb1.invoke()#Aciona o RadioButton CreateForm para renderizar os elementos na frameApp
		else:
			self.errorReport.showAndSaveError(self.db.getErrorDb(), "Erro ao inicializar banco de dados")		

	def defineVars(self):
		"Define as variaveis globais da classe"
		self.optionVar = IntVar()#Variavel controladora responsavel por definir as opcoes do menu
		self.optionVar.set(0)

		self.validateDateReg = self.window.register(validateDate)
		self.validatePhoneReg = self.window.register(validatePhone)

		self.menuOptionsFunctions = [self.activeOptionCreateForm, self.activeOptionGetApps]
		
		self.frameOld = None
		self.menuRightStateVar = False

	def defineFonts(self):
		"Define as variaveis de fontes padroes da aplicacao"
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

	def createWidgetsNewApp(self, master):
		self.frameCreateApp = Frame(master)

		self.framesNotebook = Notebook(self.frameCreateApp)
		self.framesNotebook.pack(expand=True, fill=BOTH)

		self.tabInfoApp = TabInfoApp(master=self.framesNotebook, eventWhenChangeValue=self.checkAbaInfoAppCompleted)
		tabFrameInfoApp = self.tabInfoApp.createAba()
		self.tabInfoApp.buttonNext.config(command=self.nextTabFrameItem)

		self.tabItem = TabItem(master=self.framesNotebook, nameFormVar=self.tabInfoApp.nameFormVar, eventWhenAddElement=self.checkAbaItemCompleted, eventWhenDelElement=self.checkAbaItemCompleted)
		self.tabFrameItem = self.tabItem.createAba()

		self.framesNotebook.add(tabFrameInfoApp, compound=LEFT, image=renderPhoto("images\\imagesFormsApp\\app.png", (40, 40)), sticky=W+E+N+S, text="Info App", padding='0.1i')
		self.framesNotebook.add(self.tabFrameItem, compound=LEFT, image=renderPhoto("images\\imagesFormsApp\\document.png", (40, 40)), sticky=W+E+N+S, text="Item", padding='0.1i')
		self.framesNotebook.hide(self.tabFrameItem)	

		#Cria opcoes especificas no menu direito para FieldForm
		self.createMenuSideForItem()
		
	def checkAbaInfoAppCompleted(self, a=None, b=None, c=None):#checa se todos os campos de informacoes do app foram preenchidas
		"Verifica se todos os inputs da aba InfoApp foram preenchidos"

		if self.tabInfoApp.checkAbaCompleted():
			self.tabInfoApp.buttonNext.config(state="active")
			try: self.tabItem.updateTitleFormVar()
			except: pass
		else:
			self.activeDeactivateTabFrameItem()
			self.tabInfoApp.buttonNext.config(state="disabled")
			self.buttonSaveApp.config(state="disabled")

	def checkAbaItemCompleted(self):
		"Verifica se todos os inputs da aba Item foram preenchidos"
		if self.tabItem.getElementsAdded(): self.buttonSaveApp.config(state="active")
		else: self.buttonSaveApp.config(state="disabled")

	def saveAll(self):
		nameTableFormated = formatName(self.tabItem.nameFormVar.get())+str(randint(1, 1000000))
		#appId = self.saveApp(nameTableFormated)#Salva as informacoes do App
		self.saveFieldsForm(2154)#Salva a ordem dos elementos no formulario
		#self.saveTableForm(nameTableFormated)#Salva a tabela para inserir os futuros itens

		self.tabInfoApp.cleanAbaInfoApp()#Limpa todos os campos preenchimentos de Info App
		self.tabItem.cleanFieldForm()#Remove todos os Itens adicionados na criacao do formulario
		self.activeDeactivateTabFrameItem()#Torna a aba Item invisivel novamente

	def saveApp(self, nameTableFormated):
		"Salva as informacoes do app no banco de dados"
		self.db.saveRecordApp(
			self.tabItem.nameFormVar.get(), 
			self.tabItem.descriptionFormVar.get(), 
			nameTableFormated, 
			self.pathImageFormVar.get())

		return self.db.getIdOfLastRecordInApps()[0]

	def saveFieldsForm(self, app_id):
		"Salva a ordem dos elementos no formulario"
		index_posicao = 0
		indexTemps = list(self.tabItem.getElementsAdded())
		indexTemps.sort()

		for indexTemp in indexTemps:
			element = self.tabItem.getElementsAdded().get(indexTemp)
			self.db.saveFieldApp(
				id_form=app_id,
				id_element=element.get("id_element"), 
				title=element.get("name_element_var").get(), #.encode("utf-8")
				text_help="", 
				index_position=element.get("info_app_frame").idTemporaryElement)

			if element.get("info_app_frame").params:
				for param in element.get("info_app_frame").params:# Adiciona opcoes no banco
					self.db.saveOption(param.get())

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

	def createMenuSideForItem(self):
		"Cria menu a direita para a aba item"
		if not self.menuRightStateVar:
			self.menuRight["background"] = "red"
			self.menuRightApp = Frame(self.menuRight)
			self.menuRightApp.pack(side=TOP, padx=10, pady=10)

			self.buttonSaveApp = Button(self.menuRightApp, command=self.saveAll, \
				font=self.font, text="Salvar App")
			self.buttonSaveApp.pack(side=TOP, ipadx=10)
		self.menuRightStateVar = True

	def hideMenuFieldForm(self): self.menuRightApp.forget()

	def showMenuItem(self): self.menuRightApp.pack(side=TOP, padx=10, pady=10)

	def nextTabFrameItem(self):
		self.activeDeactivateTabFrameItem()
		self.framesNotebook.select(self.tabFrameItem)

	def activeDeactivateTabFrameItem(self): self.framesNotebook.hide(self.tabFrameItem)

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

			nameAppVar = StringVar()
			aboutAppVar = StringVar()
			Label(infoAppFrame, textvariable=nameAppVar, font=self.font, foreground="lightcoral").pack(side=TOP, expand=True, fill=BOTH)
			Label(infoAppFrame, textvariable=aboutAppVar).pack(side=TOP, expand=True, fill=BOTH)
			
			nameAppVar.set(nomeApp)
			aboutAppVar.set(descricao)

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
		self.frameCreateApp.pack(side=LEFT, expand=True, fill=BOTH)
		self.showMenuItem()
		return self.frameCreateApp

	def activeOptionGetApps(self):
		self.frameGetApps.pack(side=LEFT, expand=True, fill=BOTH)
		self.hideMenuFieldForm()
		return self.frameGetApps




if  __name__ == "__main__":
	elem = Elements()
	form = Forms()
	inter = Interface()
	if inter.db.checkStatus(): inter.window.mainloop()