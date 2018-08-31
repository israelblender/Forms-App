from Tkinter import *

window = Tk()
window.geometry("400x300+150+100")
Button(window, width=15, height=2, text="Elemento", borderwidth=5, \
	activebackground="lightseagreen", background="darkcyan",\
	cursor="sb_right_arrow",
	highlightbackground = "red",
	highlightcolor = "green",
	highlightthickness = 20
	).pack(side=TOP)
Button(window, text="Elemento").pack(side=TOP)
window.mainloop()