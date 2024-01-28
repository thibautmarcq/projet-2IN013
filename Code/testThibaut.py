from tkinter import *
from robot import Robot
import math


# Configs de la fenêtre
root=Tk()
root.geometry("1130x550")
root.title("Simulation - Robocar Poli")
#root.iconbitmap('Code\logo.ico')
# root.config(background="purple")

labb = Label(root)
labb.place_forget()



# Frames

#  ----------
# |titre     |
#  ----------
# |g   ||c   |
#  ----------

frame_titre = LabelFrame(root, bd=-1)
frame_titre.grid(row=0, sticky='w', padx=15)

frame_row1 = LabelFrame(root, bd=0)
frame_row1.grid(row=1)

frame_gauche = LabelFrame(frame_row1, width=400, height=425, bd=0)
frame_gauche.grid(row=1, column=0, padx=5, pady=5)
# frame_gauche.grid_propagate(True)

frame_stats = LabelFrame(frame_gauche, text='Stats', width=350, height=200) # btn_vitesse + coordonnées
frame_stats.grid(row=1, column=0, padx=10, pady=10)
frame_gauche.grid_propagate(False)

frame_coordonnees = LabelFrame(frame_gauche, text='Coordonnées', )

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


# Key binds
root.bind("<Right>", rotationRobotD)
root.bind("<Left>", rotationRobotG)
root.bind("<space>", avancerRobot)

# Slider de vitesse
btn_vitesse = Scale(frame_stats, from_=1, to=100,  orient=HORIZONTAL, label="Vitesse", command=robot.setVitesse)
btn_vitesse.grid(row=0, column=0, padx=5, pady=5)

# Afficheur de coordonnées
lab_coord = Label(frame_stats, text='cc mv')
lab_coord.grid(row=0, column=1, padx=5, pady=5)

# Boucle de la fenètre principale
root.mainloop()