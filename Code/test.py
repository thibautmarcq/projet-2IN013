from tkinter import *

# Configs de la fenêtre
root=Tk()
root.geometry("400x350")
root.title("Test Tkinter")
root.iconbitmap('Code\logo.ico')
root.config(background="purple")

# Creation d'un label
lab = Label(root, text="cc la tim")
lab.place(x=50, y=10)

labb = Label(root)
labb.place_forget()



## Création d'un canva !!
"""Plus les choses sont en bas (dans les lignes de code), plus haut elles seront affichées"""
canv = Canvas(root, width=300 , height=200, bg="white" )
canv.place(x=50, y=50)
x=50
canv.create_line(0,200,300, 20) #(x1,y1, x2,y2)
canv.create_rectangle(50,x,250,150, fill='lightblue') #(xTopLeft,yTopLeft, xBtmRight,yBtmRight)
canv.create_line(0,100,150, 20, fill='green')




# Creation d'une entrée
inp = Entry(root)
inp.place(x=50, y=258)

# Test avec fonction et bouton
def affiche():
    print('coucou')
    x=x+5
    canv.create_rectangle(50,x,250,150, fill='lightblue')
    labb.config(text="Does this work? ->"+inp.get()+"!")
    labb.place(x=50, y=288)

btn = Button(root, text="Change", command=affiche)
btn.place(x=230, y=258)

# Boucle de la fenètre principale
root.mainloop()