from tkinter import *
from robot import Robot

# Configs de la fenêtre
root=Tk()
root.geometry("400x350")
root.title("Simulation - Robocar Poli")
#root.iconbitmap('Code\logo.ico')
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
#canv.create_line(0,200,300, 20) #(x1,y1, x2,y2)
#rect = canv.create_rectangle(50,x,250,150, fill='lightblue') #(xTopLeft,yTopLeft, xBtmRight,yBtmRight)
#canv.create_line(0,100,150, 20, fill='green')

robot = Robot("Claude", 150, 100)

robot_vec = canv.create_line(robot.posx, robot.posy, robot.posx+(75*robot.direction[0]), robot.posy+(75*robot.direction[1]))

def updateVecteur(angle):
    global robot_vec
    robot.rotation(angle)
    canv.coords(robot_vec, robot.posx, robot.posy, robot.posx+(75*robot.direction[0]), robot.posy+(75*robot.direction[1]))
def updateVecteurR(z):
    updateVecteur(0.1)
def updateVecteurL(z):
    updateVecteur(-0.1)


# Déplacement clavier
def down(event):
    canv.move(rect, 0, 5)
def up(event):
    canv.move(rect, 0, -5)
def right(event):
    canv.move(rect, 5, 0)
def left(event):
    canv.move(rect, -5, 0)
# Déplacement boutons
def downBtn():
    canv.move(rect, 0, 5)
def upBtn():
    canv.move(rect, 0, -5)
def rightBtn():
    canv.move(rect, 5, 0)
def leftBtn():
    canv.move(rect, -5, 0)

root.bind("<Down>", down)
root.bind("<Up>", up)
#root.bind("<Left>", left)
#root.bind("<Right>", right)
root.bind("<Right>", updateVecteurR)
root.bind("<Left>", updateVecteurL)

btn = Button(root, text="Up", command=upBtn)
btn.place(x=180, y=258)
btn = Button(root, text="Down", command=downBtn)
btn.place(x=180, y=288)
btn = Button(root, text="Left", command=leftBtn)
btn.place(x=130, y=288)
btn = Button(root, text="Right", command=rightBtn)
btn.place(x=230, y=288)


# Creation d'une entrée
inp = Entry(root)
inp.place(x=50, y=258)

# Test avec fonction et bouton
def affiche():
    print('coucou')
    labb.config(text="Does this work? ->"+inp.get()+"!")
    labb.place(x=50, y=288)

btn = Button(root, text="Change", command=affiche)
btn.place(x=230, y=258)

# Boucle de la fenètre principale
root.mainloop()