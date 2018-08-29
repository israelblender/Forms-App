# -*- coding: utf-8 -*-

#Autor: Israel Gomes
#Data: 26/08/2018
from modules.db import Database
from modules.utilities import renderPhoto, savePhoto
from tkMessageBox import showwarning
from ttk import Notebook
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
from random import randint


class DatabaseGui(Database):
	"""Classe destinada a avisar com interface grafica caso ocorra erro na conexao"""
	def __init__(self):
		Database.__init__(self)
		if not self.checkStatus():
			message = u"Erro ao inicializar o FormsApp\nNão foi possível se conectar ao Banco de dados"
			print(message)
			showwarning("Erro", message)
		else: print("Banco conectado com sucesso")

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
		self.db = DatabaseGui()

		self.defineFontsVars()
		self.configWindow("1.0.0")
		self.defineVars()
		self.configWidgetsMenuOptions()
		self.configWidgetsCreateForm()
		self.configWidgetsGetApps()

		self.setWidgets()

	def defineVars(self):
		self.frameOld = None
		self.optionVar = IntVar()
		self.nameFormVar = StringVar()
		self.pathImageFormVar = StringVar()

		self.menuOptionsFunctions = [self.activeOptionCreateForm, self.activeOptionGetApps]
		self.listElementThisForm = {}
		self.idTemporaryElement = 0
		self.menuSideFieldForm = False

	def defineFontsVars(self):
		Interface.font = self.font = ("Arial", 13)
		Interface.fontMin = self.fontMin = ("Arial", 10)
		Interface.fontMax = self.fontMax = ("Arial", 15)

	def setWidgets(self):

		self.optionVar.set(0)
		self.pathImageFormVar.set("link da imagem")
		self.rb1.invoke()#Aciona o RadioButton CreateForm para renderizar os elementos na frameCreateForm

	def configWindow(self, version):
		self.window = Tk()
		self.window.title("Forms App {}".format(version))
		self.window.geometry("900x500+150+100")
		self.window.iconbitmap( "..\FormsApp\src\images\imagesFormsApp\imageApp.ico")

		title = "Crie seu App, formulários, realize estatísticas, \nedite e estude seus dados com o Forms App"
		image = renderPhoto("..\FormsApp\src\images\imagesFormsApp\imageApp.png", (60, 60))
		Label(self.window, font=self.fontMax, background="#2F4F4F", foreground="#00CED1", \
			text=title, padx=10, pady=10, image=image, compound=RIGHT)\
		.pack(side=TOP, fill="x", ipady=5)
		self.frameBody = Frame(self.window, background="#20B2AA")
		self.frameBody.pack(side=TOP, expand=True, fill=BOTH)

		self.menuSide = Frame(self.frameBody, background="#20B2AA", width=150)
		self.menuSide.pack(side=RIGHT, fill=Y)
		
	def configWidgetsMenuOptions(self):
		frameOptions = Frame(self.frameBody, background="#20B2AA")
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


		self.framesNotebook.add(self.tabFrameInfoForm, sticky=W+E+N+S, text="Info App", padding='0.1i')
		self.framesNotebook.add(self.tabFrameFieldForm, sticky=W+E+N+S, text="Item", padding='0.1i')
		self.framesNotebook.hide(self.tabFrameFieldForm)

		# -------------- tabFrameInfoForm -------------

		title = "Crie seu App de forma rápida"
		Label(self.tabFrameInfoForm, text=title, font=self.font)\
		.grid(row=0, column=0, columnspan=5)

		Label(self.tabFrameInfoForm, text="Nome", font=self.fontMin).grid(row=1, column=0)
		Entry(self.tabFrameInfoForm, font=self.fontMin, textvariable=self.nameFormVar)\
		.grid(row=1, column=1, pady=10, sticky=W+E+N+S)

		Label(self.tabFrameInfoForm, text="Descrição", font=self.fontMin).grid(row=2, column=0)
		self.textWidget = Text(self.tabFrameInfoForm, pady=10, font=self.fontMin, width=50, height=3)
		self.textWidget.grid(row=2, column=1, sticky=W+E+N+S)

		self.imageWidget = Label(self.tabFrameInfoForm, padx=10, pady=10, background="grey", anchor=N)
		self.imageWidget.grid(row=1, column=2, rowspan=2, sticky=W+E+N+S, padx=10, pady=10)

		Label(self.tabFrameInfoForm, padx=10, pady=10, background="grey", font=self.fontMin, textvariable=self.pathImageFormVar)\
		.grid(row=3, column=1, sticky=W+E+N+S)
		Button(self.tabFrameInfoForm, font=self.fontMin, text="Procurar Imagem", command=self.actionChoiseImageForm)\
		.grid(row=3, column=2, padx=10, pady=10)

		Button(self.tabFrameInfoForm, font=self.fontMin, text="Prosseguir", command=self.actionNextTabFrameFieldForm)\
		.grid(row=4, column=1, padx=20, pady=15)

		# -------------- tabFrameFieldForm -------------

		title = "Crie seu formulário com toda praticidade do Forms App de forma rápida"
		Label(self.tabFrameFieldForm, text=title, font=self.font)\
		.pack(side=TOP)

		frameBodyForm = Frame(self.tabFrameFieldForm, background="#5F9EA0")
		frameBodyForm.pack(side=TOP, fill=BOTH, expand=True, padx=5)

		frameMenuElementsForm = Frame(frameBodyForm)#Frame que contera todos os elementos existentes
		frameMenuElementsForm.pack(side=LEFT, fill=Y, ipadx=5)
		self.frameRenderElementsForm = Frame(frameBodyForm)#Frame que contera todos os elementos escolhidos pelo usuario
		self.frameRenderElementsForm.pack(side=LEFT, fill=Y, ipadx=5, ipady=5)

		Label(frameMenuElementsForm, text="Elementos", font=self.font).pack(side=TOP)
		for element in self.db.getAllElemments(): #Mostra todos os elementos em forma de botoes para serem adicionados no formulário
			function = lambda id_element=element[0], name_element=element[1], type_element=element[2], multline=element[3], widget_tkinter=element[5]:\
			 self.actionAddElement(id_element, name_element, type_element, multline, widget_tkinter)

			Button(frameMenuElementsForm, width=15, height=2, text=element[1], \
			command=function, repeatinterval=700).pack(side=TOP)
	
	def actionAddElement(self, id_element, name_element, type_element, multline, widget_tkinter): #Adiciona elemento para renderizacao com evento de botao
		print("ActionAddElement acionado", id_element, name_element, type_element, multline, widget_tkinter)
		#self.addElement(id_element, name_element, type_element, multline, widget_tkinter, True)

		print("Chamando funcao para gerar novo Elemento")
		infoAppFrame = Frame(self.frameRenderElementsForm, background="grey")
		infoAppFrame.pack(side=TOP, fill=X)
		infoAppFrame.idTemporaryElement = self.idTemporaryElement
		def removeElement():#Funcao que remove o frame da tela e deleta o item da lista de elementos adicionados do formulario
			#print ("LISTA DE ELEMENTOS: ", self.listElementThisForm.keys())
			del self.listElementThisForm[infoAppFrame.idTemporaryElement]
			infoAppFrame.destroy()

		Button(infoAppFrame, text="X", command=removeElement).pack(side=RIGHT, ipadx=4, padx=4)

		nameElementVar = StringVar()
		nameElement = Entry(infoAppFrame, width=18, justify=CENTER, relief=FLAT, textvariable=nameElementVar, font=self.font)
		nameElement.pack(side=LEFT, padx=10, fill=X)
		nameElementVar.set(name_element)

		self.showElement(infoAppFrame, widget_tkinter)
		
		#Salva na lista o id do elemento,nome da variavel controladora e o tipo de dado que sera inserido no banco
		self.listElementThisForm[self.idTemporaryElement] = (id_element, nameElementVar, type_element)
		self.idTemporaryElement += 1

	def showElement(self, infoAppFrame, widget_tkinter):
		"Apenas renderiza os elementos na tela sem mais configuracoes"
		if widget_tkinter == "entry": inputElement = Entry(infoAppFrame, state="disabled", width=40, font=self.font)
		elif widget_tkinter == "text": inputElement = Text(infoAppFrame, state="disabled", width=40, height=4, font=self.font)
		elif widget_tkinter == "spinbox": inputElement = Spinbox(infoAppFrame, state="disabled", width=5, font=self.font)
		elif widget_tkinter == "entry-date": pass
		elif widget_tkinter == "entry-phone": pass

		inputElement.pack(side=RIGHT, padx=10, pady=10)
		return inputElement

		

	def renderElement(self, infoAppFrame, widget_tkinter):
		"Renderiza os elementos na tela com configurações de variáveis"
		if widget_tkinter == "entry":
			inputElementVar = StringVar()
			inputElement = Entry(infoAppFrame, width=40, textvariable=inputElementVar, font=self.font)

		elif widget_tkinter == "text":
			inputElement = Text(infoAppFrame, width=40, height=4, font=self.font)
			def set(string):
				inputElement.delete('0.0', END)
				inputElement.insert("0.0", string)
			inputElementVar = type("inputElementVar", (), \
				{"get": lambda: inputElement.get("0.0", END), "set": set})

		elif widget_tkinter == "spinbox":
			inputElementVar = StringVar()
			inputElement = Spinbox(infoAppFrame, width=5, textvariable=inputElementVar, font=self.font)
		
		elif widget_tkinter == "entry-date": pass
		elif widget_tkinter == "entry-phone": pass
		
		inputElement.pack(side=LEFT, padx=10, pady=10)
		return (inputElement, inputElementVar)


	def configWidgetsGetApps(self): # Configura todos os widgets que pertencem ao frame que mostra todos os apps e forms
		self.frameGetApps = Frame(self.frameBody)

		self.frameAbasGetApps = Notebook(self.frameGetApps)
		self.frameAbasGetApps.pack(side=TOP, fill=BOTH)
		

		self.frameApp = Frame(self.frameAbasGetApps)
		self.frameInfoApp = Frame(self.frameApp)
		self.frameInfoApp.pack(side=TOP, fill=BOTH)
		self.frameFieldsApp = Frame(self.frameApp)
		self.frameFieldsApp.pack(side=TOP, fill=BOTH)

		for idApp, nomeApp, pathImage in self.db.getAllInfoForms("id", "nome_formulario", "caminho_imagem"):
			image = renderPhoto(str("..\\formsApp\\src\\"+pathImage), (35, 35))
			self.frameAbasGetApps.add(self.frameApp, compound=LEFT, image=image, text=nomeApp, sticky=W+E+N+S)
			break

		

	# def generateTabsApps(self):
	# 	self.listTabsApps = []
	# 	for app_info in self.db.getAllInfoForms("id", "nome_formulario"):
	# 		self.listTabsApps.append(self.generateTab(  ))

	# def activeTabApp(self, name_form, description, name_table, path_image):
		
	# 	self.frameInfoApp
	# 	self.frameFieldsApp



	def actionChoiseImageForm(self):
		path_origin = tkFileDialog.askopenfilename(initialdir = "/",title = "Selecione o Arquivo",filetypes = (("Arquivos jpeg", "*.jpg"), ("Arquivos png", "*.png"),("Todos arquivos", "*.*")))
		if path_origin:
			file_name = path_origin.split("/")[-1]
			self.pathImageFormVar.set(file_name)

			path_destiny = "/images/iconsApps/"+file_name
			path_destiny = path_destiny.encode("latin-1")
			
			path_origin = path_origin.encode("latin-1")

			savePhoto(path_origin, path_destiny (100, 100))

			image = renderPhoto(path_destiny, (50, 50))
			
			self.imageWidget["image"] = image

	def actionNextTabFrameFieldForm(self):
		"Salva o app na db e pula para a proxima aba"
		#self.nameFormVar.set("Eventos Mensais")
		#self.textWidget.insert("0.0", "Eventos e palestrar de tecnologia que estão perto de ocorrer no ano de 2018.")
		self.nextTabFrameFieldForm()
		#Cria opcoes especificas no meu direito para FieldForm
		self.createMenuSideForFieldForm()

	def saveAll(self):
		nameTableFormated = self.formatNameTable(self.nameFormVar.get())+str(randint(1, 1000000))
		appId = self.saveApp(nameTableFormated)
		self.saveFieldsForm(appId)
		self.saveTableForm(nameTableFormated)

	def saveApp(self, nameTableFormated):
		"Salva o app no banco de dados"
		
		self.db.saveRecordApp(
			self.nameFormVar.get(), 
			self.textWidget.get("0.0", END), 
			nameTableFormated, 
			self.pathImageFormVar.get())

		return self.db.getIdOfLastRecordInApps()[0]

	def saveFieldsForm(self, appId):
		#(id_element, nameElementVar, type_element)
		index_posicao = 0
		indexTemps = list(self.listElementThisForm)
		indexTemps.sort()

		for indexTemp in indexTemps:
			id_element, nameElementVar, type_element = self.listElementThisForm.get(indexTemp)
#salvar em saveFieldApp ---> id_formulario, id_elemento, titulo, texto_ajuda, index_posicao
			
			self.db.saveFieldApp(appId, id_element, str(nameElementVar.get()), "", index_posicao)
			index_posicao += 1

	def saveTableForm(self, nameTableFormated):
		#try:
			fields_types = map(lambda element: self.formatNameColumn(element[1].get())+\
			" "+element[2], self.listElementThisForm.values())
			self.db.saveTableApp(nameTableFormated, fields_types)
		#except:
			#sys.stderr = file('error.log', 'a')
			#showwarning("Erro", "Erro ocorreu durante salvamento da tabela")

	def createMenuSideForFieldForm(self):
		if not self.menuSideFieldForm:
			self.menuSideOptionsFrame = Frame(self.menuSide)
			self.menuSideOptionsFrame.pack(side=TOP, padx=10, pady=10)

			Button(self.menuSideOptionsFrame, command=self.saveAll, \
				font=self.font, text="Salvar").pack(ipadx=10)
		self.menuSideFieldForm = True

	def nextTabFrameFieldForm(self):
		self.activeTabFrameFieldForm()
		self.framesNotebook.select(self.tabFrameFieldForm)

	def activeTabFrameFieldForm(self):
		self.framesNotebook.hide(self.tabFrameFieldForm)

	def formatNameColumn(self, name_field):
		name_formated = "_".join(name_field.lower().split(" ")[0:2])
		return name_formated

	def formatNameTable(self, name_form):
		name_formated = "_".join(name_form.lower().split(" ")[0:2])
		return name_formated

	def actionOptions(self):
		if self.frameOld: self.frameOld.forget()
		self.frameOld = self.menuOptionsFunctions[self.optionVar.get()]()

	def activeOptionCreateForm(self):
		print("CreateForm")
		self.frameCreateForm.pack(side=LEFT, expand=True, fill=BOTH)
		return self.frameCreateForm

	def activeOptionGetApps(self):
		print("GetApps")
		self.frameGetApps.pack(side=LEFT, expand=True, fill=BOTH)
		return self.frameGetApps
		

if  __name__ == "__main__":
	elem = Elements()
	#print (elem.getAllElemments())

	form = Forms()
	inter = Interface()
	inter.window.mainloop()
