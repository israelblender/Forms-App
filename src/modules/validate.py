from Tkinter import *

def insert(index, string):
    e.after(100, lambda: e.insert(int(index), string))

#Validar ano
def validateYear(index, after, insertion, before):
    #print index, after, insertion, before
    index = int(index)
    if index in (1, 4) and len(after)-len(before) > 0: insert(index+1, "/")

    if insertion.isdigit() and index < 10: return True
    elif insertion == "/" and index in (2, 5): return True
    else:return False

#Validar telefone
def validatePhone(index, after, insertion, before):
    print index, after, insertion, before
    index = int(index)
    if index == 0 and not before: insert(0, "(")
    elif index == 2 and len(after)-len(before) > 0: insert(3, ") ")
    elif index == 9 and len(after)-len(before) > 0: insert(10, "-")


    if insertion.isdigit() and index < 15: return True
    elif insertion == "(" and index == 0 or insertion == ") " and index == 3: return True
    elif insertion == "-" and index == 10: return True
    else: return False

#Validar hora
def validadeHour(index, after, insertion, before):
    print index, after, insertion, before
    index = int(index)
    if not len(after) - len(before) > 0: return True

    if insertion.isdigit() and index < 8:
        if index in (1, 4) and len(after) - len(before) > 0: insert(index+1, ":")

        insertion = int(insertion)
        try: number_previous = int(before[-1])
        except: number_previous = None

        if (index == 0 and insertion <= 2): return True
        elif index == 1 and ((insertion <= 9 and number_previous < 2) or\
            (insertion <= 4 and number_previous == 2)): return True

        elif index == 3 and insertion <= 5: return True
        elif index == 4 and insertion <= 9: return True
        elif index == 6 and insertion <= 5: return True
        elif index == 7 and insertion <= 9: return True
        else: return False

    elif insertion == ":" and index in (2, 5): return True
    else: return False


if __name__ == "__main__":
    window = Tk()

    entradaVar = StringVar()
    e = Entry(window, textvariable=entradaVar)
    e.place(x=50, y=50)

    validateYearReg = window.register(validateYear)
    validatePhoneReg = window.register(validatePhone)
    validadeHourReg = window.register(validadeHour)

    e.config(validate="key", validatecommand=(validadeHourReg, '%i','%P', '%S', '%s'))

    e.mainloop()
