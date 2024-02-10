from tkinter import *
import math

from Code.environnement import Environnement

class Interface:

    def __init__(self, width, length, scale):

        """ Constructeur de la classe interface, avec l'initialisation de la fenêtre 
            :param width: largeur de l'environnement
            :param length; longueur de l'environnement
            :param scale: echelle de l'environnement (permet de passer de l'environnement à la matrice) = nbr de cases de matrice par coté d'environnement
            :returns: ne retourne rien, initialise seulement l'interface
        """

        self.env = Environnement(width, length, scale) # notre environnement a représenter graphiquement

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

        """ Initialisation de la fenetre avec les différentes cadres la composant
            :returns: ne retourne rien, on prépare la strcture de notre interface graphique
        """

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
        """ Mise en place du layout et du positionnement des widget dans la fenêtre
            :returns: ne retourne rien
        """
        self.labb.place_forget()
        self.frame_titre.grid(row=0, sticky='w', padx=15)
        self.frame_row1.grid(row=1)
        self.frame_gauche.grid(row=1, column=0, padx=5, pady=5)
        self.frame_stats.grid(row=1, column=0, padx=10, pady=10)
        self.frame_coordonnees.grid(row=1, column=1)
        self.frame_canva.grid(row=1, column=1, padx=10, pady=10)
        self.canv.grid(row=3, column=0)

    def main(self):

        """ Fonction main qui permet de créer le robot et ajouter les différents outils dans la fenêtre
            :returns: ne retourne rien
        """

        self.env.createRobot("Bob", 550, 45, 30, 55, 0)

        # on crée le robot en 150 100
        for rob in self.env.robots:
            self.create_robot_rect(rob) 
            rob.robot_vec = self.canv.create_line(rob.x, rob.y, rob.x+(75*rob.direction[0]), rob.y+(75*rob.direction[1]))
        # Slider de vitesse
        btn_vitesse = Scale(self.frame_stats, from_=1, to=100,  orient=HORIZONTAL, label="Vitesse", command=self.env.robots[self.env.robotSelect].setVitesse)
        btn_vitesse.set(self.env.robots[self.env.robotSelect].vitesse) # permet d'initialiser le slider a la vitesse initiale du robot
        btn_vitesse.grid(row=0, column=0, padx=5, pady=5)
        # Afficheur de coordonnées
        lab_coord_nom = Label(self.frame_coordonnees, text=("Coordonnées du robot "+self.env.robots[self.env.robotSelect].nom+" :")).grid(row=0, column=0, padx=5, pady=5)
        lab_coord_x = Label(self.frame_coordonnees, text=("x ="+str(self.env.robots[self.env.robotSelect].x))).grid(row=1, column=0)
        lab_coord_y = Label(self.frame_coordonnees, text=("y ="+str(self.env.robots[self.env.robotSelect].y))).grid(row=1, column=1)

        # Key binds
        self.root.bind("<Right>", self.rotationRobotD)
        self.root.bind("<Left>", self.rotationRobotG)
        self.root.bind("<space>", self.avancerRobot)
        
        
        self.root.mainloop()

    def rotationRobotD(self, event):

        """ Fonction callback pour bind avec tkinter
            :param event: argument demandé par tkinter mais pas utilisé
            :returns: ne retourne rien
        """

        self.rotationRobot(math.pi/10)


    def rotationRobotG(self, event):

        """ Fonction callback pour bind avec tkinter
            :param event: argument demandé par tkinter mais pas utilisé
            :returns: ne retourne rien
        """

        self.rotationRobot(-math.pi/10)

    def avancerRobot(self, event):

        """ Fonction callback qui fait avancer notre robot
            :param event: argument demandé par tkinter mais pas utilisé
            :returns: ne retourne rien
        """
        
        robot = self.env.robots[self.env.robotSelect]
        robot.avancerDirection()
        self.refresh_position_robot_visuel(robot)

    def create_robot_rect(self, robot):
        """ Crée le polygone qui représente notre robot sur l'interface graphique
            :param robot: le robot qu'on veut représenter sur l'interface graphique
            :returns: ne retourne rien
        """
        robot.points = [robot.x-(robot.width/2), robot.y-(robot.length/2),
                        robot.x+(robot.width/2), robot.y-(robot.length/2),
                        robot.x+(robot.width/2), robot.y+(robot.length/2),
                        robot.x-(robot.width/2), robot.y+(robot.length/2)]
        robot.rect = self.canv.create_polygon(robot.points, fill="orange")

    def rotationVecteur(self, v, angle):
        
        """ Fonction qui fait une rotation du vecteur2D <v> de <angle>
            :param v: le vecteur de direction de départ
            :param angle: l'angle par lequel on veut tourner le robot
            :returns: le nouveau vecteur directeur
        """

        x, y = v
        return (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle))

    def rotate_robot_rect(self, robot, angle):
            
        """ Fait une rotation du rectangle qui représente le robot
            :param canvas: le canva dans lequel on est placé
            :param robot: le robot qu'on veut représenter graphiquement
            :param angle: l'angle de rotation du robot
            :returns: ne retourne rien, fait juste une modification sur le canva
        """

        for i in range(0, 8, 2):
            v = self.rotationVecteur((robot.points[i]-robot.x, robot.points[i+1]-robot.y), angle)
            robot.points[i] = v[0] + robot.x
            robot.points[i+1] = v[1] + robot.y
        self.canv.coords(robot.rect, robot.points)

    def refresh_position_robot_visuel(self, robot):
        
        """ Update la position du visuel du robot
            :param canvas: la fenêtre visuelle sur laquelle on est et qu'on veut mettre à jour
            :param robot: le robot dont on veut mettre à jour la représentation sur le canva
            :returns: rien, on met juste à jour la fenêtre de représentation du robot et de l'environnement
        """

        for i in range(0,8,2):
            robot.points[i] = robot.points[i]+robot.speed*robot.direction[0]
            robot.points[i+1] = robot.points[i+1]+robot.speed*robot.direction[1]
        self.canv.coords(robot.rect, robot.points)
        self.canv.coords(robot.robot_vec, robot.x, robot.y, robot.x+(75*robot.direction[0]), robot.y+(75*robot.direction[1]))
    
    def rotationRobot(self, angle):

        """ Fait une rotation de notre robot de <angle> et refresh le visuel de la direction de notre robot
            :param angle: l'angle de rotation pour le robot
            :returns: rien, on tourne le robot et on change son affichage
        """
       
        self.env.robots[0].rotation(angle)
        r = self.env.robots[self.env.robotSelect]
        self.canv.coords(r.robot_vec, r.x, r.y, r.x+(75*r.direction[0]), r.y+(75*r.direction[1]))
        self.rotate_robot_rect(r, angle)

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





