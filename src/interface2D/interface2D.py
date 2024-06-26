from tkinter import LEFT, Canvas, Label, LabelFrame, PhotoImage, Tk
from src import TIC_INTERFACE, rotationVecteur
from src.controleur import (StrategieAvancer, StrategieBoucle, StrategieCond,
                            StrategieSeq, StrategieTourner,
                            setStrategieArretMur, setStrategieCarre,
                            verifDistanceSup)


class Interface:

	def __init__(self, env, controleur):
		""" Constructeur de la classe interface, avec l'initialisation de la fenêtre et de ses composants
			:param env: l'environnement dans lequel on initialise l'interface
			:param controleur: le contrôleur de l'environnement:returns: ne retourne rien, initialise seulement l'interface
		"""
		self.env = env  # notre environnement a représenter graphiquement
		self.controleur = controleur # contient l'instance du controleur

		# Config fenêtre
		self.root=Tk()
		self.root.geometry(str(self.env.width+500)+"x"+str(max(600,self.env.length+100))) # Adapatation de la taille de la fenetre en fct de celle de l'environnement
		self.root.title("Simulation - Robocar Poli")

		# ------------------------ Initialisation des frames, modèle ----------------------------------
		#								  -------------------
		#								 |titre              |
		#								  -------------------
		#								 |  vitesse ||       |
		#								 |  coords  || canva |
		#								  ---------- |       |
		#								 |   tuto   ||       | 
		#							 	  -------------------
		# ---------------------------------------------------------------------------------------------

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
		self.tutorial_image = PhotoImage(file="src/interface2D/source/tuto_fr.png").subsample(2,2)
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


	# ------------------------- Création des robots et des obstacles ---------------------------------------

	def createRobotRect(self, robot):
		""" Crée le polygone qui représente notre robot sur l'interface graphique
			:param robot: le robot qu'on veut représenter sur l'interface graphique
			:returns: ne retourne rien
		"""
		robot.points = [robot.x-(robot.width/2), robot.y-(robot.length/2),
						robot.x+(robot.width/2), robot.y-(robot.length/2),
						robot.x+(robot.width/2), robot.y+(robot.length/2),
						robot.x-(robot.width/2), robot.y+(robot.length/2)]
		robot.rect = self.canv.create_polygon(robot.points, fill=(robot.couleur))


	def createObs(self):
		""" Crée le polygone qui représente notre obstacle sur l'interface graphique
			:returns: ne retourne rien
		"""
		for obs in self.env.listeObs:
			self.canv.create_polygon(obs.lstPoints, fill=('grey'))


	# --------------------------------------- Choix de la stratégie ---------------------------------------

	def choisirStrategie(self, strat, distance) :
		""" Choisis la strategie à lancer
			:param strat: 1 pour la strategie carré, 2 pour la strategie arret mur, 3 pour la conditionnelle mur, 4 pour la boucle carré
			:param distance: la taille du coté du carré ou la distance d'arret du robot pour la strat arretmur 
		
		"""
		robA = self.env.listeRobots[self.env.robotSelect]
		if robA.robot.estCrash:
			print("Impossible de contrôler ce robot, il est crash.")
			return
		elif robA.robot.estSousControle:
			print("Impossible de contrôler ce robot, il est déjà sous contrôle.")
			return

		if strat==1:
			carre = setStrategieCarre(robA, distance)
			self.controleur.lancerStrategie(carre)
			robA.robot.draw = True
			robA.robot.firstDrawPoint = (robA.robot.x, robA.robot.y)
		elif strat==2:
			arret_mur = setStrategieArretMur(robA, distance)
			self.controleur.lancerStrategie(arret_mur)
		elif strat==3:
			arret_mur2 = StrategieCond(robA, StrategieAvancer(robA,400), lambda: verifDistanceSup(robA, distance))
			self.controleur.lancerStrategie(arret_mur2)
		elif strat==4:
			carre2 = StrategieBoucle(robA, StrategieSeq([StrategieAvancer(robA, distance), StrategieTourner(robA, 90)], robA), 4)
			self.controleur.lancerStrategie(carre2)
					

#  ----------------------- Méthodes liées à l'update de l'interface -------------------------------------

	def updateStatsAffichage(self):
		""" Met à jour l'affichage des coordonnées dans l'affichage (implémenter chaque avancement)
			:returns: ne retourne rien, fait juste l'affichage à jour des coordonnées
		"""

		# Update labels coordonnees
		self.lab_coord_nom.config(text=("Coordonnées du robot "+self.env.listeRobots[self.env.robotSelect].robot.nom+" :"))
		self.lab_coord_x.config(text=("x ="+str(round(self.env.listeRobots[self.env.robotSelect].robot.x, 2))))
		self.lab_coord_y.config(text=("y ="+str(round(self.env.listeRobots[self.env.robotSelect].robot.y, 2))))
		self.lab_vitesse.config(text=("Vitesse globale : "+str(round(self.env.listeRobots[self.env.robotSelect].robot.getVitesse()))))
		self.lab_vitesseG.config(text=("Vitesse roue G : "+str(round(self.env.listeRobots[self.env.robotSelect].robot.getVitesseG()))))
		self.lab_vitesseD.config(text=("Vitesse roue D : "+str(round(self.env.listeRobots[self.env.robotSelect].robot.getVitesseD()))))

		# Update label distance
		self.lab_distance.config(text=("Obstacle dans : "+str(round(self.env.listeRobots[self.env.robotSelect].getDistanceA(), 2))))


	def refreshPositionRobotVisuel(self, canvas, robot): 

		""" Update la position du visuel du robot
			:param canvas: la fenêtre visuelle sur laquelle on est et qu'on veut mettre à jour
			:param robot: le robot dont on veut mettre à jour la représentation sur le canva
			:returns: rien, on met juste à jour la fenêtre de représentation du robot et de l'environnement
		"""
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


	def rotateRobotRect(self, canvas, robot, angle):
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


	def dessinePoint(self, pos, couleur) :
		""" Dessine un point d'une certaine couleur à une position donnée
			:param pos: coordonées du point que l'on veut dessiner
			:param couleur: couleur que l'on veut donner au point
		"""
		x, y = pos
		self.canv.create_line(x-1, y-1, x+1, y+1, fill=couleur)

#  ----------------------- Méthodes liées au lancement et au déroulement de l'interface -------------------------------------

	def ticTac(self):
		self.updateStatsAffichage()
		for adapt in self.env.listeRobots:
			robot = adapt.robot 
			self.refreshPositionRobotVisuel(self.canv, robot)
			if robot.draw and not robot.estCrash:
				self.dessinePoint((robot.x, robot.y),  "black")
				if not robot.estSousControle:
					robot.draw = False
		self.root.after(int(TIC_INTERFACE), self.ticTac)


	def mainloop(self):
		""" Initialise toutes les fonctionnalités en lien avec le robot (dans l'env et dans tkinter)
			:returns: rien
		"""
		for robA in self.env.listeRobots:
			rob = robA.robot
			self.createRobotRect(rob)
			rob.draw = False
			rob.robot_vec = self.canv.create_line(rob.x, rob.y, rob.x+(75*rob.direction[0]), rob.y+(75*rob.direction[1]))

		self.createObs()
	

		# -------------------------------------------------------------------		-------------
		# 								BINDS,										| a | z | e |
		# Le lambda event permet de ne pas avoir de fct avec 'event' en param		| q | s | d |
		# -------------------------------------------------------------------		-------------
		self.root.bind('a', lambda event: self.env.listeRobots[self.env.robotSelect].robot.changeVitAngG(1)) # + gauche
		self.root.bind('q', lambda event: self.env.listeRobots[self.env.robotSelect].robot.changeVitAngG(-1)) # - gauche
		self.root.bind('z', lambda event: self.env.listeRobots[self.env.robotSelect].robot.changeVitAng(1)) # + tout
		self.root.bind('s', lambda event: self.env.listeRobots[self.env.robotSelect].robot.changeVitAng(-1)) # - tout
		self.root.bind('e', lambda event: self.env.listeRobots[self.env.robotSelect].robot.changeVitAngD(1)) # + droit
		self.root.bind('d', lambda event: self.env.listeRobots[self.env.robotSelect].robot.changeVitAngD(-1)) # - droit


		self.root.bind('c', lambda event: self.choisirStrategie(1, 120)) # Fait tracer le carré au robot
		self.root.bind('m', lambda event: self.choisirStrategie(2, 20)) # fait la stratégie avancer jusqu'au mur
		self.root.bind('p', lambda event: self.choisirStrategie(3, 15)) # fait la stratégie avancer jusqu'au mur - 2ème méthode (stratégie conditionnelle)
		self.root.bind('o', lambda event: self.choisirStrategie(4, 120)) # fait la stratégie carré - 2ème méthode  (stratégie boucle)

		self.root.bind('<Escape>', lambda event: self.root.destroy())

		self.root.bind("x", lambda event: self.env.addRobotSelect(1))
		self.root.bind("w", lambda event: self.env.addRobotSelect(-1))


		# ----------------------------------- Affichages vitesses, coordonnées et capteur de distance ----------------------------------------

		self.lab_vitesse = Label(self.frame_vitesses, text=("Vitesse globale : "+str(self.env.listeRobots[self.env.robotSelect].robot.getVitesse())))
		self.lab_vitesse.grid(row=0, column=0, padx=5, pady=2)
		self.lab_vitesseG = Label(self.frame_vitesses, text=("Vitesse roue G : "+str(self.env.listeRobots[self.env.robotSelect].robot.getVitesseG())))
		self.lab_vitesseG.grid(row=1, column=0, padx=5, pady=2)
		self.lab_vitesseD = Label(self.frame_vitesses, text=("Vitesse roue D : "+str(self.env.listeRobots[self.env.robotSelect].robot.getVitesseD())))
		self.lab_vitesseD.grid(row=2, column=0, padx=5, pady=2)

		self.lab_coord_nom = Label(self.frame_coordonnees, text=("Coordonnées du robot "+self.env.listeRobots[self.env.robotSelect].robot.nom+" :"))
		self.lab_coord_nom.grid(row=0, column=0, padx=5, pady=5)
		self.lab_coord_x = Label(self.frame_coordonnees, text=("x ="+str(self.env.listeRobots[self.env.robotSelect].robot.x)))
		self.lab_coord_x.grid(row=1, column=0)
		self.lab_coord_y = Label(self.frame_coordonnees, text=("y ="+str(self.env.listeRobots[self.env.robotSelect].robot.y)))
		self.lab_coord_y.grid(row=2, column=0)

		self.lab_distance = Label(self.frame_dist_obstacle, text=("Obstacle dans : "+str(round(self.env.listeRobots[self.env.robotSelect].getDistanceA(), 2))))
		self.lab_distance.grid(row=0, column=0)


		# Lancement du tic tac
		self.ticTac()
		# Boucle de la fenètre principale
		self.root.mainloop()