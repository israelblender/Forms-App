# -*- coding: utf-8 -*-

#Autor: Israel Gomes
#Data: 26/08/2018
from modules.db import Database
from Tkinter import *

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
		self.configWindow("1.0.0")
		self.defineVars()
		self.configWidgets()

		self.setWidgets()

	def defineVars(self):
		self.windowOld = None
		self.optionVar = IntVar()

		self.frameAction0 = Frame(self.window, background="green")
		self.frameAction1 = Frame(self.window, background="red")

	def setWidgets(self):
		self.optionVar.set(0)

	def configWindow(self, version):
		self.window = Tk()
		self.window.title("Forms App {}".format(version))
		self.window.geometry("800x500+150+100")
		self.font = ("Arial", 12)

	def configWidgets(self):
		title = "Crie Formulários, realize estatísticas, \nedite e estude os dados com o Form App"
		Label(self.window, font=self.font, text=title, padx=10, pady=10).grid(columnspa=3, row=0, column=0)
		
		rb1 = Radiobutton(self.window, font=self.font, text="Criar", variable=self.optionVar,
		value=0, indicatoron=0, width=15, height=2, command=self.actionOptions)
		rb1.grid(row=1, column=0)
		rb2 = Radiobutton(self.window, font=self.font, text="Todos", variable=self.optionVar,
		value=1, indicatoron=0, width=15, height=2, command=self.actionOptions)
		rb2.grid(row=2, column=0)

	def actionOptions(self):
		if self.optionVar.get() == 0:
			self.windowOld.forget()
			self.windowOld = self.activeOptionCreateForm()
		elif self.optionVar.get() == 1:
			self.windowOld.forget()
			self.windowOld = self.activeOptionGetForms()

	def activeOptionCreateForm(self):
		print("CreateForm")
		self.frameAction0.grid(row=1, column=1, columnspan=2, rowspan=3)
		return self.frameAction0

	def activeOptionGetForms(self):
		print("GetForms")
		self.frameAction1.grid(row=1, column=1, columnspan=2, rowspan=3)
		return self.frameAction1

if  __name__ == "__main__":
	elem = Elements()
	print (elem.getAllElemments())

	form = Forms()
	inter = Interface()
	inter.window.mainloop()
