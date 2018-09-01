from Tkinter import Text, Tk, Button, END
w = Tk()
t = Text(w, width=10, height=2)
t.pack()

def createVarByTextWidget(textWidget):
	def funcSet(value):
		textWidget.delete("0.0", END)
		textWidget.insert("0.0", value)
	return type("StringVar", (), {"set": staticmethod(funcSet), "get": staticmethod(lambda: textWidget.get("0.0", END))})

tVar = createVarByTextWidget(t)

def set(): tVar.set("NOVO VALOR")
def get(): print(tVar.get())
Button(w, text="Set", command=set).pack()
Button(w, text="Get", command=get).pack()


print(tVar)

w.mainloop()