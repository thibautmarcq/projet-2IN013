from tkinter import *

# Configs de la fenêtre
root=Tk()
root.geometry("400x300")
root.title("Test Tkinter")
root.config(background="#130879")

# Creation d'un label
lab = Label(root, text="cc la tim")
lab.place(x=50, y=10)

labb = Label(root)
labb.place_forget()

# Creation d'une entrée
inp = Entry(root)
inp.place(x=50, y=45)

# Test avec fonction et bouton
def affiche():
    print('coucou')
    labb.config(text="Does this work? ->"+inp.get()+"!")
    labb.place(x=50, y=250)

btn = Button(root, text="Afficher", command=affiche)
btn.place(x=50, y=200)

# Boucle de la fenètre principale
root.mainloop()