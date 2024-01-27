from tkinter import *
from robot import Robot
import math

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

# -------------------------
# Test de la visualisation 
# du vecteur directeur du robot
# -------------------------

# on crée le robot en 150 100
robot = Robot("Claude", 150, 100, 50,80, 30)
# on crée le visuel pour le vecteur directeur de ce robot

def create_robot_rect(canv, robot):
    """crée le polygone qui représente notre robot sur l'interface graphique"""
    robot.points = [robot.posx-(robot.width/2), robot.posy-(robot.height/2),
                    robot.posx+(robot.width/2), robot.posy-(robot.height/2),
                    robot.posx+(robot.width/2), robot.posy+(robot.height/2),
                    robot.posx-(robot.width/2), robot.posy+(robot.height/2)]
    robot.rect = canv.create_polygon(robot.points, fill="orange")

create_robot_rect(canv, robot)
robot_vec = canv.create_line(robot.posx, robot.posy, robot.posx+(75*robot.direction[0]), robot.posy+(75*robot.direction[1]))

def rotationVecteur(v, angle):
    """fonction qui fais une rotation du vecteur2D <v> de <angle>"""
    x, y = v
    return (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle))

def rotate_robot_rect(canvas, robot, angle):
    """fait une rotation du rectangle qui représente le robot"""
    for i in range(0, 8, 2):
        v = rotationVecteur((robot.points[i]-robot.posx, robot.points[i+1]-robot.posy), angle)
        robot.points[i] = v[0] + robot.posx
        robot.points[i+1] = v[1] + robot.posy
    canvas.coords(robot.rect, robot.points)



def refresh_position_robot_visuel(canvas, robot):
    """Update la position du visuel du robot"""

    for i in range(0,8,2):
        robot.points[i] = robot.points[i]+robot.speed*robot.direction[0]
        robot.points[i+1] = robot.points[i+1]+robot.speed*robot.direction[1]
    canvas.coords(robot.rect, robot.points)
    canvas.coords(robot_vec, robot.posx, robot.posy, robot.posx+(75*robot.direction[0]), robot.posy+(75*robot.direction[1]))



def rotationRobot(angle):
    """fait une rotation de notre robot de <angle>
        et refresh le visuel de la direction de notre robot
    """
    robot.rotation(angle)
    canv.coords(robot_vec, robot.posx, robot.posy, robot.posx+(75*robot.direction[0]), robot.posy+(75*robot.direction[1]))
    rotate_robot_rect(canv, robot, angle)

def rotationRobotD(event):
    """fonction callback pour bind avec tkinter
    possede un argument event car demandé par tkinter
    mais pas utilisé
    """
    rotationRobot(math.pi/10)
def rotationRobotG(event):
    """fonction callback pour bind avec tkinter
    l'argument event est obligatoire pour récupérer l'evenement
    mais il nous est pas utile
    """
    rotationRobot(-math.pi/10)

def avancerRobot(event):
    """Fonction callback qui fait avancer notre robot"""
    robot.avancerDirection()
    refresh_position_robot_visuel(canv, robot)


# # Déplacement clavier
# def down(event):
#     canv.move(rect, 0, 5)
# def up(event):
#     canv.move(rect, 0, -5)
# def right(event):
#     canv.move(rect, 5, 0)
# def left(event):
#     canv.move(rect, -5, 0)
# # Déplacement boutons
# def downBtn():
#     canv.move(rect, 0, 5)
# def upBtn():
#     canv.move(rect, 0, -5)
# def rightBtn():
#     canv.move(rect, 5, 0)
# def leftBtn():
#     canv.move(rect, -5, 0)

# root.bind("<Down>", down)
# root.bind("<Up>", up)
# #root.bind("<Left>", left)
# #root.bind("<Right>", right)
root.bind("<Right>", rotationRobotD)
root.bind("<Left>", rotationRobotG)
root.bind("<Up>", avancerRobot)

# btn = Button(root, text="Up", command=upBtn)
# btn.place(x=180, y=258)
# btn = Button(root, text="Down", command=downBtn)
# btn.place(x=180, y=288)
# btn = Button(root, text="Left", command=leftBtn)
# btn.place(x=130, y=288)
# btn = Button(root, text="Right", command=rightBtn)
# btn.place(x=230, y=288)


# # Creation d'une entrée
# inp = Entry(root)
# inp.place(x=50, y=258)

# # Test avec fonction et bouton
# def affiche():
#     print('coucou')
#     labb.config(text="Does this work? ->"+inp.get()+"!")
#     labb.place(x=50, y=288)

# btn = Button(root, text="Change", command=affiche)
# btn.place(x=230, y=258)

# Boucle de la fenètre principale
root.mainloop()