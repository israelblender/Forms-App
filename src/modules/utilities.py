# -*- coding: Latin-1 -*-
from PIL import Image, ImageTk
from datetime import datetime


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
    image = Image.open(path)
    image = image.resize(size, Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    list_images.append(photo)
    return photo

def savePhoto(path_origin, path_destiny, size):
    image = Image.open(path_origin)
    image = image.resize(size, Image.ANTIALIAS)
    image.save(path_destiny, "png")