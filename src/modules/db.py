# -*- coding: Latin-1 -*-

#Autor: Israel Gomes
#Data: 26/08/2018

import sqlite3
"""Classes relacionada ao banco de dados"""

class Database(object):
	"Classe Singleton para conexao com banco de dados Sqlite3"
	def __new__(self):
		if not hasattr(self, "_instance"):
			self._instance = super(Database, self).__new__(self)
			try:
				self.db = sqlite3.connect("..\FormsApp\src\databases\database.db")
				self.cursor = self.db.cursor()
				self.execute = self.cursor.execute
				self.fetchall = self.cursor.fetchall
				self.fetchone = self.cursor.fetchone
				print("\n\nBanco conectado com sucesso"+ str(id(self._instance)))
				self.status = True
			except: 
				self.status = False

		return self._instance
	def checkStatus(self):#Retorna o True caso o banco esteja conectado
		return self.status

	def __init__(self):
		print("\nClasse Database inicializada com sucesso"+ str(id(self)))

	def getAllElemments(self):
		self.execute("select id, nome, tipo, multilinha, caminho_imagem, widget_tkinter from elementos")
		return self.fetchall()

	def getAllInfoForms(self, *columns):
		"""Retorna as informacoes de todos os apps existentes no banco"""
		if not columns: self.execute("select * from apps")
		else: self.execute("select {} from apps".format(", ".join(columns)))
		return self.fetchall()

	def getInfoFormByName(self, name_form):
		"""Retorna a informacao do formulario informando o nome do formulario"""
		query = "select * from apps where nome_formulario = '{}'".format(name_form)
		self.execute(query)
		return self.fetchall()

	def getInfoFormById(self, id_form):
		"""Retorna a tabela que representa o id identificador de formulario informado"""
		query = "select * from apps where id = {}".format(id_form)
		#print(query)
		self.execute(query)
		return self.fetchall()

	def getRecordAppByNameTableAndId(self, name_table, id_record):
		"""Retorna o registro da tabela
		 informada com o id informado"""

		query = "select * from {} where id_ = {}".format(name_table, id_record)
		#print(query)
		self.execute(query)
		return self.fetchall()

	def getAllDataAppByNameTable(self, name_table):
		"""Retorna todos os registros da tabela informando
		o nome da tabela"""

		query = "select * from {}".format(name_table)
		#print(query)
		self.execute(query)
		return self.fetchall()

	def getAllDataAppByNameApp(self, name_app):
		"""Retorna informacoes do formulario informando
		o nome identificador do formulario"""

		# Retorna id, nome_formulario, descricao, nome_tabela
		info_form = self.getFormByName(name_app)
		table_name = info_form[3]
		data_form = self.getAllDataTableByNameForm(name_form)
		return data_form

	def getAllDataFormByIdApp(self, id_app):
		"""Retorna informacoes do formulario informando
		o id identificador do formulario"""

		# Retorna id, nome_formulario, descricao, nome_tabela
		info_form = self.getFormById(name_form)
		table_name = info_form[0]
		data_form = self.getAllDataTableByNameForm(name_form)
		return data_form

	def saveRecordApp(self, name_form, description, name_table, path_image):
		query = """insert into apps
		(nome_formulario, descricao, nome_tabela, caminho_imagem)
		values(?, ?, ?, ?)"""
		self.execute(query, (name_form, description, name_table, path_image))

		self.db.commit()

