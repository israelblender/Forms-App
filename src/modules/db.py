# -*- coding: Latin-1 -*-

#Autor: Israel Gomes
#Data: 26/08/2018

import sqlite3
#from modules.report import ErrorReport
"""Classes relacionada ao banco de dados"""

class Database(object):
	"Classe Singleton para conexao com banco de dados Sqlite3"
	_instance_n = 0
	def __new__(self):
		if not hasattr(self, "_instance"):
			self._instance = super(Database, self).__new__(self)
		self._instance_n += 1
		return self._instance
	def checkStatus(self):#Retorna o True caso o banco esteja conectado
		return self.status

	def getErrorDb(self):
		return self.error.message

	def __init__(self):
		if self._instance_n == 1:
			try:
				#1/0
				self.db = sqlite3.connect("databases/database.db")
				self.dbUser = sqlite3.connect("databases/databaseUser.db")
				self.cursor = self.db.cursor()
				self.execute = self.cursor.execute
				self.fetchall = self.cursor.fetchall
				self.fetchone = self.cursor.fetchone

				self.cursorUser = self.dbUser.cursor()
				self.executeUser = self.cursorUser.execute
				self.fetchallUser = self.cursorUser.fetchall
				self.fetchoneUser = self.cursorUser.fetchone
				#print("\n\nBanco conectado com sucesso"+ str(id(self._instance)))
				self.status = True
			except Exception as error: 
				self.error = error
				self.status = False
		#print("\nClasse Database inicializada com sucesso"+ str(id(self)))

	def getAllElemments(self):
		self.execute("select id, nome, tipo, multilinha, caminho_imagem, widget_tkinter from elementos")
		return self.fetchall()

	def getAllInfoForms(self, *columns):
		"""Retorna as informacoes de todos os apps existentes no banco"""
		if not columns: self.execute("select * from apps")
		else: self.execute("select {} from apps".format(", ".join(columns)))
		return self.fetchall()

	def getInfoFormByNameLike(self, name_form):
		"""Retorna a informacao do formulario informando o nome do formulario"""
		query = "select * from apps where like nome_formulario '%{}%'".format(name_form)
		self.execute(query)
		return self.fetchall()

	def getInfoFormByNameTable(self, name_table):
		"""Retorna a informacao do formulario informando o nome da tabela"""
		query = "select * from apps where nome_tabela='{}'".format(name_form)
		self.execute(query)
		return self.fetchall()

	def getIdOfLastRecordInApps(self):
		"Obtem o ultimo app adicionado pelo usuario"
		query = "select id from apps order by id desc limit 1"
		self.execute(query)
		return self.fetchall()[0]

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

	def saveFieldApp(self, id_form, id_element, title, text_help, index_position, params):
		query = u"""insert into sequencia_elementos_formulario
		(id_formulario, id_elemento, titulo, texto_ajuda, index_posicao, parametros)
		values(?, ?, ?, ?, ?, ?)
		"""
		self.execute(query, (id_form, id_element, title, text_help, index_position, ",".join(params)))
		self.db.commit()

	def saveTableApp(self, name_table, fields_types):
		query = """
			create table {}(id INTEGER PRIMARY KEY AUTOINCREMENT, {})
		""".format(name_table, ", ".join(fields_types))

		self.executeUser(query)
		self.dbUser.commit()

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