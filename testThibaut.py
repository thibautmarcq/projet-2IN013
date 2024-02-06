import math
from tkinter import *

from .Code.environnement import Environnement
from .Code.robot import Robot

# Configs de la fenêtre
root=Tk()
root.geometry("1030x550")
root.title("Simulation - Robocar Poli")
#root.iconbitmap('Code\logo.ico')
# root.config(background="purple")

labb = Label(root)
labb.place_forget()



# Frames

#  --------------
# |titre         |
#  --------------
# |g up  ||c     |
# | tuto ||      |
#  --------------

frame_titre = LabelFrame(root, bd=-1)
frame_titre.grid(row=0, sticky='w', padx=15)

frame_row1 = LabelFrame(root, bd=0)
frame_row1.grid(row=1)

frame_gauche = LabelFrame(frame_row1, width=400, height=425, bd=0)
frame_gauche.grid(row=1, column=0, padx=5, pady=5)

frame_up = LabelFrame(frame_gauche, bd=0)
frame_up.grid(row=0)

frame_vitesses = LabelFrame(frame_up, text='Vitesses', width=350, height=200) # btn_vitesse + coordonnées
frame_vitesses.grid(row=0, column=0, padx=10, pady=10)

frame_coordonnees = LabelFrame(frame_up, text='Coordonnées', )
frame_coordonnees.grid(row=0, column=1)

frame_tutorial = LabelFrame(frame_gauche, text="Tutorial", bd=1)
frame_tutorial.grid(row=1)
tutorial_image = PhotoImage(file="Code/Interface/tutorial_up_key.png").subsample(2,2)
tutorial = Label(frame_tutorial, image=tutorial_image)
tutorial.grid(row=1, column=1)

frame_canva = LabelFrame(frame_row1, padx=10, pady=10)
frame_canva.grid(row=1, column=1, padx=10, pady=10)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)


# Creation d'un label
lab = Label(frame_titre, text="Robocar Poli - Simulation Robot 2D", font=('Helvetica', 20), justify=LEFT).pack()

## Création d'un canva !!
"""Plus les choses sont en bas (dans les lignes de code), plus haut elles seront affichées"""
canv = Canvas(frame_canva, width=600 , height=400, bg="white" )
canv.grid(row=3, column=0)


# -------------------------------------------------------
# Test de la visualisation du vecteur directeur du robot
# -------------------------------------------------------

# on crée le robot en 150 100
robot = Robot("Claude", 150, 100, 50, 80, 30)

# Afficheur de coordonnées
# global lab_coord_nom, lab_coord_x, lab_coord_y
lab_coord_nom = Label(frame_coordonnees, text=("Coordonnées du robot "+robot.nom+" :")).grid(row=0, column=0, padx=5, pady=5)
lab_coord_x = Label(frame_coordonnees, text=("x ="+str(robot.x)))
lab_coord_x.grid(row=1, column=0)
lab_coord_y = Label(frame_coordonnees, text=("y ="+str(robot.y)))
lab_coord_y.grid(row=1, column=1)



def update_coord_affichage():

    """ Met à jour l'affichage des coordonnées dans l'affichage (implémenter chaque avancement)
        :returns: ne retourne rien, fait juste l'affichage à jour des coordonnées
    """

    # Update labels
    lab_coord_x.config(text=("x ="+str(round(robot.x, 2))))
    lab_coord_y.config(text=("y ="+str(round(robot.y, 2))))


# on crée le visuel pour le vecteur directeur de ce robot

def create_robot_rect(canv, robot):

    """ Crée le polygone qui représente notre robot sur l'interface graphique
        :param robot: le robot qu'on veut représenter par un polygone dans l'interface graphique
        :returns: ne retourne rien, crée le robot uniquement
    """

    robot.points = [robot.x-(robot.width/2), robot.y-(robot.length/2),
                    robot.x+(robot.width/2), robot.y-(robot.length/2),
                    robot.x+(robot.width/2), robot.y+(robot.length/2),
                    robot.x-(robot.width/2), robot.y+(robot.length/2)]
    robot.rect = canv.create_polygon(robot.points, fill="orange")

create_robot_rect(canv, robot)
robot_vec = canv.create_line(robot.x, robot.y, robot.x+(75*robot.direction[0]), robot.y+(75*robot.direction[1]))

def rotationVecteur(v, angle):

    """ Fonction qui fait une rotation du vecteur2D <v> de <angle>
        :param v: le vecteur de direction de départ
        :param angle: l'angle par lequel on veut tourner le robot
        :returns: le nouveau vecteur directeur
    """

    x, y = v
    return (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle))

def rotate_robot_rect(canvas, robot, angle):

    """ Fait une rotation du rectangle qui représente le robot
        :param canvas: le canva dans lequel on est placé
        :param robot: le robot qu'on veut représenter graphiquement
        :param angle: l'angle de rotation du robot
        :returns: ne retourne rien, fait juste une modification sur le canva
    """

    for i in range(0, 8, 2):
        v = rotationVecteur((robot.points[i]-robot.x, robot.points[i+1]-robot.y), angle)
        robot.points[i] = v[0] + robot.x
        robot.points[i+1] = v[1] + robot.y
    canvas.coords(robot.rect, robot.points)



def refresh_position_robot_visuel(canvas, robot):

    """ Update la position du visuel du robot
        :param canvas: la fenêtre visuelle sur laquelle on est et qu'on veut mettre à jour
        :param robot: le robot dont on veut mettre à jour la représentation sur le canva
        :returns: rien, on met juste à jour la fenêtre de représentation du robot et de l'environnement
    """
    for i in range(0,8,2):
        robot.points[i] = robot.points[i]+robot.vitesse*robot.direction[0]
        robot.points[i+1] = robot.points[i+1]+robot.vitesse*robot.direction[1]
    dx, dy = robot.direction
    canvas.coords(robot.rect,
                  robot.x-(robot.width/2)*(-dy)-(robot.length/2)*dx,
                  robot.y-(robot.width/2)*(dx)-(robot.length/2)*dy,
                  robot.x+(robot.width/2)*(-dy)-(robot.length/2)*dx,
                  robot.y+(robot.width/2)*(dx)-(robot.length/2)*dy,
                  robot.x+(robot.width/2)*(-dy)+(robot.length/2)*dx,
                  robot.y+(robot.width/2)*(dx)+(robot.length/2)*dy,
                  robot.x-(robot.width/2)*(-dy)+(robot.length/2)*dx,
                  robot.y-(robot.width/2)*(dx)+(robot.length/2)*dy
                  )
    canvas.coords(robot_vec, robot.x, robot.y, robot.x+(75*robot.direction[0]), robot.y+(75*robot.direction[1]))
    update_coord_affichage()
    #root.after(1000/60, refresh_position_robot_visuel(canv, robot))

def rotationRobot():
    """
    Fait une rotation de notre robot de <angle>
    et refresh le visuel de la direction de notre robot
    """
    robot.rotation()
    canv.coords(robot_vec, robot.x, robot.y, robot.x+(75*robot.direction[0]), robot.y+(75*robot.direction[1]))
    refresh_position_robot_visuel(canv, robot)

def rotationRobotD(event):

    """ Fonction callback pour bind avec tkinter
        :param event: argument appelé car demandé par tkinter mais pas utilisé
        :returns: ne retourne rien, on bind juste pour faire la rotation droite
    """
    robot.addTourD()
    robot.setVitesse()
    rotationRobot()

def rotationRobotG(event):

    """ Fonction callback pour bind avec tkinter
        :param event: l'argument event est obligatoire pour récupérer l'evenementmais il ne nous est pas utile
        :returns: ne retourne rien, on bind juste pour faire la rotation gauche
    """
    robot.addTourG()
    robot.setVitesse()
    rotationRobot()

def avancerRobot(event):

    """ Fonction callback qui fait avancer notre robot
        :param event: demandé par tkinter mais on ne l'utilise pas vraiment
        :returns: ne retourne rien, on avance puis affiche le robot
    """
    
    if robot.avancerDirection() :
        refresh_position_robot_visuel(canv, robot)

def test(event):
    """print("avant", robot.direction)
    robot.addTourD()
    print("Add tourD", robot.direction)
    robot.rotation()
    print("rotation", robot.direction)
    robot.addTourG()
    print("Add tourG", robot.direction)
    robot.rotation()
    print("rotation", robot.direction)
    robot.addTourG()
    print("Add tourG", robot.direction)
    robot.rotation()
    print("rotation", robot.direction)"""
    root.after(int(1000/60), tic_tac)

def tic_tac():
    env.refresh_env()
    refresh_position_robot_visuel(canv, robot)
    root.after(int(1000/30), tic_tac)



# Key binds
root.bind("<space>", tic_tac)

# Setup de l'environnement
env = Environnement(400, 600, 1) # un environnement qui reprend grossièrement la taille du canva test, et avec une échelle de 1, c'est pas représentatif c'est juste pour intégrer l'environnement
env.addRobot(robot)


# Slider des vitesses des roues gauche et droite respectivement
btn_tourG = Scale(frame_vitesses, from_=50, to=0, orient=VERTICAL, label="Vitesse \nroue G", command=robot.setTourG)
btn_tourG.config(length=70)
btn_tourG.grid(row=0, column=0, padx=5, pady=5)

btn_tourD = Scale(frame_vitesses, from_=50, to=0, orient=VERTICAL, label="Vitesse \nroue D", command=robot.setTourD)
btn_tourD.config(length=70)
btn_tourD.grid(row=0, column=1, padx=5, pady=5)

# Boucle de la fenètre principale
root.mainloop()