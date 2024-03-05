import math
import threading
from time import *
from tkinter import *

from Code.environnement import Environnement
from Code.Robot.robot import Robot
from tkinter import Label, Tk

from Code.Controleur.controleur import *

class Interface:

	def __init__(self, env, controleur):
		""" Constructeur de la classe interface, avec l'initialisation de la fenêtre et de ses composants
			:param width: largeur de l'environnement
			:param length; longueur de l'environnement
			:param scale: echelle de l'environnement (permet de passer de l'environnement à la matrice) = nbr de cases de matrice par coté d'environnement
			:returns: ne retourne rien, initialise seulement l'interface
		"""
		self.env = env# notre environnement a représenter graphiquement

		self.controleur = controleur # contient l'instance du controleur

		# Config fenêtre
		self.root=Tk()
		self.root.geometry(str(self.env.width+500)+"x"+str(max(600,self.env.length+100))) # Adapatation de la taille de la fenetre en fct de celle de l'environnement
		self.root.title("Simulation - Robocar Poli")


		# Initialisation des frames, modèle :
		#  --------------
		# |titre         |
		#  --------------
		# |g  up ||can   |
		# | tuto ||   va |
		#  --------------
		self.frame_titre = LabelFrame(self.root, bd=-1)
		self.frame_titre.grid(row=0, sticky='w', padx=15)

		self.frame_row1 = LabelFrame(self.root, bd=0)
		self.frame_row1.grid(row=1)

		self.frame_gauche = LabelFrame(self.frame_row1, width=400, height=425, bd=0)
		self.frame_gauche.grid(row=1, column=0, padx=5, pady=5)

		self.frame_up = LabelFrame(self.frame_gauche, bd=0)
		self.frame_up.grid(row=0)

		self.frame_vitesses = LabelFrame(self.frame_up, text='Vitesses', width=200, height=100) # btn_vitesse + coordonnées
		self.frame_vitesses.grid_propagate(False)
		self.frame_vitesses.grid(row=0, column=0, padx=10, pady=10)

		self.frame_coordonnees = LabelFrame(self.frame_up, text='Coordonnées', width= 20, height=100)
		self.frame_vitesses.grid_propagate(False)
		self.frame_coordonnees.grid(row=1, column=0)

		self.frame_dist_obstacle = LabelFrame(self.frame_up, text='Distance obstacle')
		self.frame_dist_obstacle.grid(row=2, column=0)
	
		self.frame_tutorial = LabelFrame(self.frame_gauche, text="Tutorial", bd=1)
		self.frame_tutorial.grid(row=1)
		self.tutorial_image = PhotoImage(file="Code/Interface/source/new-switch-carre.png").subsample(2,2)
		self.tutorial = Label(self.frame_tutorial, image=self.tutorial_image)
		self.tutorial.grid(row=1, column=1)

		self.frame_canva = LabelFrame(self.frame_row1, padx=10, pady=10)
		self.frame_canva.grid(row=1, column=1, padx=10, pady=10)

		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_rowconfigure(2, weight=1)
		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_columnconfigure(2, weight=1)

		# Initialisation du titre
		self.lab = Label(self.frame_titre, text="Robocar Poli - Simulation Robot 2D", font=('Helvetica', 20), justify=LEFT).pack()

		# Création du canva
		self.canv = Canvas(self.frame_canva, width=self.env.width , height=self.env.length, bg="white" ) # Le canva prend en compte la taille de l'environnement
		self.canv.grid(row=3, column=0)


	def create_robot_rect(self, robot):
		""" Crée le polygone qui représente notre robot sur l'interface graphique
			:param robot: le robot qu'on veut représenter sur l'interface graphique
			:returns: ne retourne rien
		"""
		robot.points = [robot.x-(robot.width/2), robot.y-(robot.length/2),
						robot.x+(robot.width/2), robot.y-(robot.length/2),
						robot.x+(robot.width/2), robot.y+(robot.length/2),
						robot.x-(robot.width/2), robot.y+(robot.length/2)]
		robot.rect = self.canv.create_polygon(robot.points, fill=(robot.couleur))

	def create_obs(self):
		""" Crée le polygone qui représente notre obstacle sur l'interface graphique
			:param env: le robot qu'on veut représenter sur l'interface graphique
			:returns: ne retourne rien
		"""
		for obs in self.env.listeObs:
			self.canv.create_polygon(obs.lstPoints, fill=('grey'))
		
	def choisir_strategie(self, strat, distance) :
		""" Choisis la strategie à lancer
			:param strat: 1 pour la strategie carré et 2 pour la strategie arret mur
			:param distance: la taille du coté du carré ou la distance d'arret du robot pour la strat arretmur 
		
		"""
		rob = self.env.robots[self.env.robotSelect]
		if rob.estCrash:
			print("Impossible de controller ce robot il est crash")
			return
		elif rob.estSousControle:
			print("Impossible de controller ce robot il est déjà sous controle")
			return

		if strat==1:
			Controler.setStategieCarre(self.controleur,rob, distance)

		if strat==2:
			Controler.setStrategieArretMur(self.controleur,rob, distance, self.env)
		
		


	def update_stats_affichage(self):
		""" Met à jour l'affichage des coordonnées dans l'affichage (implémenter chaque avancement)
			:returns: ne retourne rien, fait juste l'affichage à jour des coordonnées
		"""

		# Update labels coordonnees
		self.lab_coord_nom.config(text=("Coordonnées du robot "+self.env.robots[self.env.robotSelect].nom+" :"))
		self.lab_coord_x.config(text=("x ="+str(round(self.env.robots[self.env.robotSelect].x, 2))))
		self.lab_coord_y.config(text=("y ="+str(round(self.env.robots[self.env.robotSelect].y, 2))))
		self.lab_vitesse.config(text=("Vitesse globale : "+str(round(self.env.robots[self.env.robotSelect].getVitesse()))))
		self.lab_vitesseG.config(text=("Vitesse roue G : "+str(round(self.env.robots[self.env.robotSelect].getVitesseG()))))
		self.lab_vitesseD.config(text=("Vitesse roue D : "+str(round(self.env.robots[self.env.robotSelect].getVitesseD()))))
		# Update label distance
		self.lab_distance.config(text=("Obstacle dans : "+str(round(self.env.robots[self.env.robotSelect].capteurDistance(self.env), 2))))

	def rotationVecteur(self, v, angle):

		""" Fonction qui fait une rotation du vecteur2D <v> de <angle>
			:param v: le vecteur de direction de départ
			:param angle: l'angle par lequel on veut tourner le robot
			:returns: le nouveau vecteur directeur
		"""

		x, y = v
		return (x*math.cos(angle)-y*math.sin(angle), x*math.sin(angle)+y*math.cos(angle))


	def rotate_robot_rect(self, canvas, robot, angle):

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
		canvas.coords(robot.rect, robot.points)


	def refresh_position_robot_visuel(self, canvas, robot): 

		""" Update la position du visuel du robot
			:param canvas: la fenêtre visuelle sur laquelle on est et qu'on veut mettre à jour
			:param robot: le robot dont on veut mettre à jour la représentation sur le canva
			:returns: rien, on met juste à jour la fenêtre de représentation du robot et de l'environnement
		"""
		"""for i in range(0,8,2):
			robot.points[i] = robot.points[i]+robot.vitesse*robot.direction[0]
			robot.points[i+1] = robot.points[i+1]+robot.vitesse*robot.direction[1]"""
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
		canvas.coords(robot.robot_vec, robot.x, robot.y, robot.x+(75*robot.direction[0]), robot.y+(75*robot.direction[1]))
		#root.after(1000/60, refresh_position_robot_visuel(canv, robot))

	def dessine_point(self, canva, pos, couleur) :
		x, y = pos
		canva.create_line(x-1, y-1, x+1, y+1, fill=couleur)

	def tic_tac(self):
		self.update_stats_affichage()
		for robot in self.env.robots:
			self.refresh_position_robot_visuel(self.canv, robot)
		self.root.after(int(1000/60), self.tic_tac)
			# self.dessine_point(self.canv, (self.env.robots[self.env.robotSelect].x, self.env.robots[self.env.robotSelect].y), self.env.robots[self.env.robotSelect].couleur)


	def mainloop(self):
		""" Initialise toutes les fonctionnalités en lien avec le robot (dans l'env et dans tkinter)
			:returns: rien
		"""
		#bob = self.env.robots[self.env.robotSelect]
		#self.robot_vec = self.canv.create_line(bob.x, bob.y, bob.x+(75*bob.direction[0]), bob.y+(75*bob.direction[1]))
		for rob in self.env.robots:
			self.create_robot_rect(rob)
			rob.robot_vec = self.canv.create_line(rob.x, rob.y, rob.x+(75*rob.direction[0]), rob.y+(75*rob.direction[1]))
		
		self.create_obs()
	

		# ---------------------------
		# Afficheur de coordonnées du robot
		self.lab_coord_nom = Label(self.frame_coordonnees, text=("Coordonnées du robot "+self.env.robots[self.env.robotSelect].nom+" :"))
		self.lab_coord_nom.grid(row=0, column=0, padx=5, pady=5)
		self.lab_coord_x = Label(self.frame_coordonnees, text=("x ="+str(self.env.robots[self.env.robotSelect].x)))
		self.lab_coord_x.grid(row=1, column=0)
		self.lab_coord_y = Label(self.frame_coordonnees, text=("y ="+str(self.env.robots[self.env.robotSelect].y)))
		self.lab_coord_y.grid(row=2, column=0)

		# Affichage données capteur distance
		self.lab_distance = Label(self.frame_dist_obstacle, text=("Obstacle dans : "+str(round(self.env.robots[self.env.robotSelect].capteurDistance(self.env), 2))))
		self.lab_distance.grid(row=0, column=0)

		# -------------------------------------------------------------------		-------------
		# 								BINDS,										| a | z | e |
		# Le lambda event permet de ne pas avoir de fct avec 'event' en param		| q | s | d |
		# -------------------------------------------------------------------		-------------
		self.root.bind('a', lambda event: self.env.robots[self.env.robotSelect].changeVitAngG(1)) # + gauche
		self.root.bind('q', lambda event: self.env.robots[self.env.robotSelect].changeVitAngG(-1)) # - gauche
		self.root.bind('z', lambda event: self.env.robots[self.env.robotSelect].changeVitAng(1)) # + tout
		self.root.bind('s', lambda event: self.env.robots[self.env.robotSelect].changeVitAng(-1)) # - tout
		self.root.bind('e', lambda event: self.env.robots[self.env.robotSelect].changeVitAngD(1)) # + droit
		self.root.bind('d', lambda event: self.env.robots[self.env.robotSelect].changeVitAngD(-1)) # - droit


		self.root.bind('c', lambda event: self.choisir_strategie(1, 120)) # Fait tracer le carré au robot
		self.root.bind('m', lambda event: self.choisir_strategie(2, 20))


		self.root.bind("x", lambda event: self.env.addRobotSelect(1))
		self.root.bind("w", lambda event: self.env.addRobotSelect(-1))
		# -------------------------------------------------------------------
		# 						NOUVEAUX AFFICHAGES							
		# -------------------------------------------------------------------
		self.lab_vitesse = Label(self.frame_vitesses, text=("Vitesse globale : "+str(self.env.robots[self.env.robotSelect].getVitesse())))
		self.lab_vitesse.grid(row=0, column=0, padx=5, pady=2)
		self.lab_vitesseG = Label(self.frame_vitesses, text=("Vitesse roue G : "+str(self.env.robots[self.env.robotSelect].getVitesseG())))
		self.lab_vitesseG.grid(row=1, column=0, padx=5, pady=2)
		self.lab_vitesseD = Label(self.frame_vitesses, text=("Vitesse roue D : "+str(self.env.robots[self.env.robotSelect].getVitesseD())))
		self.lab_vitesseD.grid(row=2, column=0, padx=5, pady=2)

		# Lancement du tic tac
		self.tic_tac()
		# Boucle de la fenètre principale
		self.root.mainloop()