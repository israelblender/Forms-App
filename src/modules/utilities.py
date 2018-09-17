# -*- coding: Latin-1 -*-
from PIL import Image, ImageTk
from datetime import datetime
from modules.report import ErrorReport

errorReport = ErrorReport("error_utilities.log")

def formatDate(date):
    "Formata data de 0000-00-00 para 00/00/0000 e vice-versa"
    if "-" in date.isoformat():
        new_date = datetime.strptime(date.isoformat(), '%Y-%m-%d').strftime('%d/%m/%Y')
    else:
        new_date = datetime.strptime(date.isoformat(), '%d/%m/%Y').strftime('%Y-%m-%d')
    return new_date

list_images = []
def renderPhoto(path, size):
    global list_images
    """ path recebe caminho em string"
        size recebe tupla (x, y) com valores do tamanho da imagem que será renderizada
    """
    #global photo
    try:
        image = Image.open(path)

    except: 
        image = Image.open("images\\testar\\Buzzfeed.png")
        print "Arquivo nao foi encontrado"
    image = image.resize(size, Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    list_images.append(photo)
    return photo


def savePhoto(path_origin, path_destiny, size):
    "Salva a foto no novo caminho com o novo tamanho informado"
    try:
        image = Image.open(path_origin)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(path_destiny, "png")
    except Exception as error:
        errorReport.showAndSaveError(error.message, "Erro direcionado a funcao savePhoto")

def createVarByTextWidget(textWidget):
    def funcSet(value):
        textWidget.delete("0.0", "end")
        textWidget.insert("0.0", value)
    return type("StringVar", (), {"set": staticmethod(funcSet), "get": staticmethod(lambda: textWidget.get("0.0", "end"))})