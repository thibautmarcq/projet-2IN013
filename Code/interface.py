from tkinter import *
import math
class Interface:

    def __init__(self, env):
        self.env = env # notre environnement a représenter graphiquement

        #initilisation de la fenetre
        self.root=Tk()
        self.root.geometry("1130x550")
        self.root.title("Simulation - Robocar Poli")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)


        self.create_widget()
        self.place_widget()

        self.main()
    def create_widget(self):
        self.labb = Label(self.root)
        self.frame_titre = LabelFrame(self.root, bd=-1)
        self.frame_row1 = LabelFrame(self.root, bd=0)
        self.frame_gauche = LabelFrame(self.frame_row1, width=400, height=425, bd=0)
        self.frame_stats = LabelFrame(self.frame_gauche, text='Stats', width=350, height=200) # btn_vitesse + coordonnées
        self.frame_coordonnees = LabelFrame(self.frame_gauche, text='Coordonnées', )
        self.frame_canva = LabelFrame(self.frame_row1, padx=10, pady=10)

        # Creation d'un label
        self.lab = Label(self.frame_titre, text="Robocar Poli - Simulation Robot 2D", font=('Helvetica', 20), justify=LEFT).pack()

        self.canv = Canvas(self.frame_canva, width=600 , height=400, bg="white" )

    def place_widget(self):
        self.labb.place_forget()
        self.frame_titre.grid(row=0, sticky='w', padx=15)
        self.frame_row1.grid(row=1)
        self.frame_gauche.grid(row=1, column=0, padx=5, pady=5)
        self.frame_stats.grid(row=1, column=0, padx=10, pady=10)
        self.frame_coordonnees.grid(row=1, column=1)
        self.frame_canva.grid(row=1, column=1, padx=10, pady=10)
        self.canv.grid(row=3, column=0)

    def main(self):
        # on crée le robot en 150 100
        for rob in self.env.robots:
            self.create_robot_rect(rob) 
            rob.robot_vec = self.canv.create_line(rob.posx, rob.posy, rob.posx+(75*rob.direction[0]), rob.posy+(75*rob.direction[1]))
        # Slider de vitesse
        btn_vitesse = Scale(self.frame_stats, from_=1, to=100,  orient=HORIZONTAL, label="Vitesse", command=self.env.robots[self.env.robotSelect].setVitesse)
        btn_vitesse.set(self.env.robots[self.env.robotSelect].speed) # permet d'initialiser le slider a la vitesse initiale du robot
        btn_vitesse.grid(row=0, column=0, padx=5, pady=5)
        # Afficheur de coordonnées
        lab_coord_nom = Label(self.frame_coordonnees, text=("Coordonnées du robot "+self.env.robots[self.env.robotSelect].nom+" :")).grid(row=0, column=0, padx=5, pady=5)
        lab_coord_x = Label(self.frame_coordonnees, text=("x ="+str(self.env.robots[self.env.robotSelect].posx))).grid(row=1, column=0)
        lab_coord_y = Label(self.frame_coordonnees, text=("y ="+str(self.env.robots[self.env.robotSelect].posy))).grid(row=1, column=1)

        # Key binds
        self.root.bind("<Right>", self.rotationRobotD)
        self.root.bind("<Left>", self.rotationRobotG)
        self.root.bind("<space>", self.avancerRobot)
        
        
        self.root.mainloop()

    def rotationRobotD(self, event):
        """fonction callback pour bind avec tkinter
        possede un argument event car demandé par tkinter
        mais pas utilisé
        """
        self.rotationRobot(math.pi/10)
    def rotationRobotG(self, event):
        """fonction callback pour bind avec tkinter
        l'argument event est obligatoire pour récupérer l'evenement
        mais il nous est pas utile
        """
        self.rotationRobot(-math.pi/10)

    def avancerRobot(self, event):
        """Fonction callback qui fait avancer notre robot"""
        robot = self.env.robots[self.env.robotSelect]
        robot.avancerDirection()
        self.refresh_position_robot_visuel(robot)

    def create_robot_rect(self, robot):
        """crée le polygone qui représente notre robot sur l'interface graphique"""
        robot.points = [robot.posx-(robot.width/2), robot.posy-(robot.height/2),
                        robot.posx+(robot.width/2), robot.posy-(robot.height/2),
                        robot.posx+(robot.width/2), robot.posy+(robot.height/2),
                        robot.posx-(robot.width/2), robot.posy+(robot.height/2)]
        robot.rect = self.canv.create_polygon(robot.points, fill="orange")

    def rotationVecteur(self, v, angle):
        """fonction qui fais une rotation du vecteur2D <v> de <angle>"""
        x, y = v
        return (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle))

    def rotate_robot_rect(self, robot, angle):
        """fait une rotation du rectangle qui représente le robot"""
        for i in range(0, 8, 2):
            v = self.rotationVecteur((robot.points[i]-robot.posx, robot.points[i+1]-robot.posy), angle)
            robot.points[i] = v[0] + robot.posx
            robot.points[i+1] = v[1] + robot.posy
        self.cnv.coords(robot.rect, robot.points)

    def refresh_position_robot_visuel(self, robot):
        """Update la position du visuel du robot"""

        for i in range(0,8,2):
            robot.points[i] = robot.points[i]+robot.speed*robot.direction[0]
            robot.points[i+1] = robot.points[i+1]+robot.speed*robot.direction[1]
        self.canv.coords(robot.rect, robot.points)
        self.canv.coords(self.robot_vec, robot.posx, robot.posy, robot.posx+(75*robot.direction[0]), robot.posy+(75*robot.direction[1]))
    
    def rotationRobot(self, angle):
        """fait une rotation de notre robot de <angle>
            et refresh le visuel de la direction de notre robot
        """
        self.env.robots[0].rotation(angle)
        r = self.env.robots[self.env.robotSelect]
        self.canv.coords(r.robot_vec, r.posx, r.posy, r.posx+(75*r.direction[0]), r.posy+(75*r.direction[1]))
        self.rotate_robot_rect(self, r, angle)

# Frames

#  ----------
# |titre     |
#  ----------
# |g   ||c   |
#  ----------



# -------------------------------------------------------
# Test de la visualisation du vecteur directeur du robot
# -------------------------------------------------------

# on crée le visuel pour le vecteur directeur de ce robot





