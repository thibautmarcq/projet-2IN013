from tkinter import *
from robot import Robot
import math


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

frame_stats = LabelFrame(frame_up, text='Stats', width=350, height=200) # btn_vitesse + coordonnées
frame_stats.grid(row=0, column=0, padx=10, pady=10)

frame_coordonnees = LabelFrame(frame_up, text='Coordonnées', )
frame_coordonnees.grid(row=0, column=1)

frame_tutorial = LabelFrame(frame_gauche, text="Tutorial", bd=1)
frame_tutorial.grid(row=1)
tutorial_image = PhotoImage(file="Code/tutorial.png").subsample(2,2)
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
    """
    Met à jour l'affichage des coordonnées dans l'affichage (implémenter chaque avancement)
    """
    # Update labels
    lab_coord_x.config(text=("x ="+str(round(robot.x, 2))))
    lab_coord_y.config(text=("y ="+str(round(robot.y, 2))))


# on crée le visuel pour le vecteur directeur de ce robot

def create_robot_rect(canv, robot):
    """
    crée le polygone qui représente notre robot sur l'interface graphique
    """
    robot.points = [robot.x-(robot.width/2), robot.y-(robot.height/2),
                    robot.x+(robot.width/2), robot.y-(robot.height/2),
                    robot.x+(robot.width/2), robot.y+(robot.height/2),
                    robot.x-(robot.width/2), robot.y+(robot.height/2)]
    robot.rect = canv.create_polygon(robot.points, fill="orange")

create_robot_rect(canv, robot)
robot_vec = canv.create_line(robot.x, robot.y, robot.x+(75*robot.direction[0]), robot.y+(75*robot.direction[1]))

def rotationVecteur(v, angle):
    """fonction qui fais une rotation du vecteur2D <v> de <angle>"""
    x, y = v
    return (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle))

def rotate_robot_rect(canvas, robot, angle):
    """fait une rotation du rectangle qui représente le robot"""
    for i in range(0, 8, 2):
        v = rotationVecteur((robot.points[i]-robot.x, robot.points[i+1]-robot.y), angle)
        robot.points[i] = v[0] + robot.x
        robot.points[i+1] = v[1] + robot.y
    canvas.coords(robot.rect, robot.points)



def refresh_position_robot_visuel(canvas, robot):
    """Update la position du visuel du robot"""
    for i in range(0,8,2):
        robot.points[i] = robot.points[i]+robot.speed*robot.direction[0]
        robot.points[i+1] = robot.points[i+1]+robot.speed*robot.direction[1]
    canvas.coords(robot.rect, robot.points)
    canvas.coords(robot_vec, robot.x, robot.y, robot.x+(75*robot.direction[0]), robot.y+(75*robot.direction[1]))
    update_coord_affichage()

def rotationRobot(angle):
    """fait une rotation de notre robot de <angle>
        et refresh le visuel de la direction de notre robot
    """
    robot.rotation(angle)
    canv.coords(robot_vec, robot.x, robot.y, robot.x+(75*robot.direction[0]), robot.y+(75*robot.direction[1]))
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


# Key binds
root.bind("<Right>", rotationRobotD)
root.bind("<Left>", rotationRobotG)
root.bind("<space>", avancerRobot)

# Slider de vitesse
btn_vitesse = Scale(frame_stats, from_=1, to=100,  orient=HORIZONTAL, label="Vitesse", command=robot.setVitesse)
btn_vitesse.set(robot.speed) # permet d'initialiser le slider a la vitesse initiale du robot
btn_vitesse.grid(row=0, column=0, padx=5, pady=5)

# Boucle de la fenètre principale
root.mainloop()