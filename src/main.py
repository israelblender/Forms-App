# -*- coding: utf-8 -*-

#Autor: Israel Gomes
#Data: 26/08/2018
from modules.db import Database
from tkMessageBox import showwarning
from PIL import ImageTk, Image
from ttk import Notebook
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog


class DatabaseGui(Database):
	"""Classe destinada a avisar com interface grafica caso ocorra erro na conexao"""
	def __init__(self):
		Database.__init__(self)
		if not self.checkStatus():
			message = u"Erro ao inicializar o FormApp\nNão foi possível se conectar ao Banco de dados"
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
		self.db = Database()

	def getAllForms(self):
		# retorna (id, nome_formulario, descricao, nome_tabela, caminho_imagem)
		all_forms = self.db.getAllInfoForms()

		return all_forms

class Interface():
	index_position_current = 0
	listElementThisForm = []
	def __init__(self):
		self.db = Database()

		self.defineFontsVars()
		self.configWindow("1.0.0")
		self.defineVars()
		self.configWidgetsOptions()
		self.configWidgetsCreateForm()
		self.configWidgetsGetForms()

		self.setWidgets()

	def defineVars(self):
		#self.frameOld = None
		self.optionVar = IntVar()
		self.nameFormVar = StringVar()
		self.pathImageFormVar = StringVar()

		#self.index_position_current = 0

	def defineFontsVars(self):
		self.font = ("Arial", 12)
		self.fontMin = ("Arial", 10)
		self.fontMax = ("Arial", 15)

	def setWidgets(self):

		self.optionVar.set(0)
		self.pathImageFormVar.set("link da imagem")
		self.rb1.invoke()#Aciona o RadioButton CreateForm para renderizar os elementos na frameCreateForm

	def configWindow(self, version):
		self.window = Tk()
		self.window.title("Forms App {}".format(version))
		self.window.geometry("800x500+150+100")

		title = "Crie seu App, formulários, realize estatísticas, \nedite e estude seus dados com o FormApp"
		Label(self.window, font=self.fontMax, background="#2F4F4F", foreground="#6B8E23", text=title, padx=10, pady=10)\
		.pack(side=TOP, fill="x", ipady=15)
		self.frameBody = Frame(self.window)
		self.frameBody.pack(side=TOP)
		
	def configWidgetsOptions(self):
		frameOptions = Frame(self.frameBody)
		frameOptions.pack(side=LEFT)

		self.rb1 = Radiobutton(frameOptions, font=self.font, text="Criar App", variable=self.optionVar,
		value=0, indicatoron=0, width=15, height=2, command=self.actionOptions)
		self.rb1.grid(row=1, column=0)
		self.rb2 = Radiobutton(frameOptions, font=self.font, text="Todos", variable=self.optionVar,
		value=1, indicatoron=0, width=15, height=2, command=self.actionOptions)
		self.rb2.grid(row=2, column=0)

	def configWidgetsCreateForm(self):
		self.frameCreateForm = Frame(self.frameBody)

		self.framesNotebook = Notebook(self.frameCreateForm)
		self.framesNotebook.pack(expand=True, fill=BOTH)

		self.labelFrameInfoForm = Frame(self.framesNotebook)
		self.labelFrameFieldForm = Frame(self.framesNotebook)

		self.framesNotebook.add(self.labelFrameInfoForm, text="Info App")
		self.framesNotebook.add(self.labelFrameFieldForm, text="Formulário")

		# -------------- labelFrameInfoForm -------------

		title = "Crie seu App de forma rápida"
		Label(self.labelFrameInfoForm, text=title, font=self.font)\
		.grid(row=0, column=0, columnspan=5)

		Label(self.labelFrameInfoForm, text="Nome", font=self.fontMin).grid(row=1, column=0)
		Entry(self.labelFrameInfoForm, font=self.fontMin, textvariable=self.nameFormVar)\
		.grid(row=1, column=1, pady=10, sticky=W+E+N+S)

		Label(self.labelFrameInfoForm, text="Descrição", font=self.fontMin).grid(row=2, column=0)
		self.textWidget = Text(self.labelFrameInfoForm, pady=10, font=self.fontMin, width=50, height=3)
		self.textWidget.grid(row=2, column=1, sticky=W+E+N+S)

		self.imageWidget = Label(self.labelFrameInfoForm, padx=10, pady=10, background="gray", anchor=N)
		self.imageWidget.grid(row=1, column=2, rowspan=2, sticky=W+E+N+S, padx=10, pady=10)

		Label(self.labelFrameInfoForm, padx=10, pady=10, background="gray", font=self.fontMin, textvariable=self.pathImageFormVar)\
		.grid(row=3, column=1, sticky=W+E+N+S)
		Button(self.labelFrameInfoForm, font=self.fontMin, text="Procurar Imagem", command=self.actionChoiseImageForm)\
		.grid(row=3, column=2, padx=10, pady=10)

		Button(self.labelFrameInfoForm, font=self.fontMin, text="Salvar", command=self.actionSaveApp)\
		.grid(row=4, column=1, padx=20, pady=15)

		# -------------- labelFrameFieldForm -------------

		title = "Crie seu formulário com toda praticidade do FormApp de forma rápida"
		Label(self.labelFrameFieldForm, text=title, font=self.font)\
		.pack(side=TOP)

		frameBodyForm = Frame(self.labelFrameFieldForm, background="red")
		frameBodyForm.pack(side=TOP)

		frameMenuElementsForm = Frame(frameBodyForm)#Frame que contera todos os elementos existentes
		frameMenuElementsForm.pack(side=LEFT)
		frameRenderElementsForm = Frame(frameBodyForm)#Frame que contera todos os elementos escolhidos pelo usuario
		frameRenderElementsForm.pack(side=LEFT)

		class Action():
			def __init__(self, id_element, type_element, multline):
				self.id_element = id_element
				self.type_element = type_element
				self.multline = True if multline == '1' else False
			def __call__(self):
				Interface.actionAddElement(self.id_element, self.type_element, self.multline)

		for element in self.db.getAllElemments(): #Mostra todos os elementos em forma de botoes para serem adicionados no formulário
			action = Action(element[0], element[2], element[3])

			Button(frameMenuElementsForm, width=15, height=2, text=element[1], \
				command=action, repeatinterval=700).pack(side=TOP)
	
	@classmethod
	def actionAddElement(cls, id_element, type_element, multline): #Adiciona elemento para formulário
		print("ActionAddElement acionado", id_element, type_element, multline)
		cls.addElementToList(id_element=id_element, index_position=cls.index_position_current)
		cls.index_position_current += 1

	@classmethod
	def addElementToList(cls, id_element, index_position):#Adiciona elemento para a renderização
		cls.listElementThisForm.append((id_element, index_position))



	def configWidgetsGetForms(self): # Configura todos os widgets que pertencem ao frame que mostra todos os apps e forms
		self.frameGetForms = Frame(self.frameBody, background="red")
		

	def actionChoiseImageForm(self):
		global img
		imageFormPath = tkFileDialog.askopenfilename(initialdir = "/",title = "Selecione o Arquivo",filetypes = (("Arquivos jpeg", "*.jpg"), ("Arquivos png", "*.png"),("Todos arquivos", "*.*")))
		if imageFormPath:
			self.pathImageFormVar.set(imageFormPath.split("/")[-1])

			img_ = Image.open(imageFormPath)
			img_ = img_.resize((100, 100))
			img = ImageTk.PhotoImage(img_)
			self.imageWidget["image"] = img

	def actionSaveApp(self):
		#print (self.textWidget.get("0.0", END))
		#print ("Nome Tabela formadado: "+self.formatNameTable(self.nameFormVar.get()))
		
		self.nameFormVar.set("Eventos Mensais")
		self.textWidget.insert("0.0", "Eventos e palestrar de tecnologia que estão perto de ocorrer no ano de 2018.")
		self.db.saveRecordForm(self.nameFormVar.get(), self.textWidget.get("0.0", END), self.formatNameTable(self.nameFormVar.get()), self.pathImageFormVar.get())
				
		print("Salvo com sucesso")
	def formatNameTable(self, name_form):
		name_formated = "_".join(name_form.lower().split(" ")[0:2])
		return name_formated

	def actionOptions(self):
		if self.optionVar.get() == 0:
			try:
				self.frameOld.forget()
			except: pass
			self.frameOld = self.activeOptionCreateForm()

		elif self.optionVar.get() == 1:
			try:
				self.frameOld.forget()
			except: pass

			self.frameOld = self.activeOptionGetForms()

	def activeOptionCreateForm(self):
		print("CreateForm")
		self.frameCreateForm.pack(side=LEFT)
		return self.frameCreateForm

	def activeOptionGetForms(self):
		print("GetForms")
		self.frameGetForms.pack(side=LEFT)
		return self.frameGetForms
		

if  __name__ == "__main__":
	elem = Elements()
	print (elem.getAllElemments())

	form = Forms()
	inter = Interface()
	inter.window.mainloop()
