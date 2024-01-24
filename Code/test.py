from tkinter import *

# Configs de la fenêtre
root=Tk()
root.geometry("400x350")
root.title("Test Tkinter")
root.iconbitmap()
root.config(background="purple")

# Creation d'un label
lab = Label(root, text="cc la tim")
lab.place(x=50, y=10)

labb = Label(root)
labb.place_forget()

# Création d'un canva
canv = Canvas(root, width=300 , height=200, bg="white" )
canv.place(x=50, y=50)

# Creation d'une entrée
inp = Entry(root)
inp.place(x=50, y=258)

# Test avec fonction et bouton
def affiche():
    print('coucou')
    labb.config(text="Does this work? ->"+inp.get()+"!")
    labb.place(x=50, y=288)

btn = Button(root, text="Afficher", command=affiche)
btn.place(x=230, y=258)

# Boucle de la fenètre principale
root.mainloop()