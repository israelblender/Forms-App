from tkMessageBox import showwarning

class ErrorReport:
	def __init__(self, file_name):
		self.file_name = file_name
		self.selfError = False

	def showAndSaveError(self, error_message, description_name):
		self.saveErrorLog(error_message)
		if not self.selfError:
			showwarning("Erro para desenvolvedores", description_name+"\nMensagem de erro: {}".format(error_message))

	def saveErrorLog(self, error_message):
		try: 
			self.saveFile(self.file_name, error_message)
		except Exception as error:
			showwarning("Erro para desenvolvedores", 
			"""ERRO NO PROPRIO CONTROLADOR DE ERROS
			Mensagem de erro: {}
			PASTA ATUAL: {}""".format( str(error), os.getcwd() ))

			input("APERTE QUALQUER TECLA PARA SAIR")
			
			self.saveFile("error_self.log", str(error))
			self.selfError = True

	def saveFile(self, file_name, error_message):
		logFile = file(file_name, 'a+')
		logFile.write("\n"+error_message)
		logFile.close()