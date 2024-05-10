# pip install panda3d==1.10.14

from math import cos, pi, sin
from sys import exit
from threading import Thread
from time import sleep

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import (Filename, Geom, GeomNode,
						  GeomTriangles, GeomVertexData, GeomVertexFormat,
						  GeomVertexWriter, OmniBoundingVolume, PNMImage,
						  Point3, Texture, load_prc_file, LineSegs, NodePath)
from src import (DICO_COULEURS, TIC_SIMULATION, StrategieAvancer,
				 StrategieBoucle, StrategieCond, StrategieSeq,
				 StrategieTourner, setStrategieArretMur, setStrategieCarre,
				 verifDistanceSup, StrategieSuivreBalise)

import numpy as np

load_prc_file('src/interface3D/source/config.prc')

class Interface3D(ShowBase):
	""" Classe Interface 3D - Ensemble de méthodes définies pour créer et gérer des objets dans une interface en 3D """

	def __init__(self, env, controleur):
		ShowBase.__init__(self)
		self.env = env
		self.controleur = controleur
		self.createAllRobots()
		self.createAllObstacles()
		self.createEnvironnement()
		self.running = True

		self.createBalise(Balise(250, 250, 80, 53))

		# Bind quitter la fenêtre
		self.accept('escape', exit)

		self.son = self.loader.loadSfx("src/interface3D/source/secret.mp3")
		self.secret = False

		self.taskMgr.add(self.upCameraTask, "upCameraTask")
		# self.taskMgr.add(self.frontCameraTask, "frontCameraTask")
		# self.taskMgr.add(self.spinCameraTask, "spinCameraTask")
		# self.taskMgr.add(self.backCameraTask, "backCameraTask")

		self.setDraw()

		self.camLens.setFar(100000) # Pour ne pas avoir de problème de distance de vue
		T_tictac = Thread(target=self.ticTac, daemon=True)
		T_tictac.start()

	def binds(self):
		""" Bind les touches pour les déplacements des robots """
		# -------------------------------------------------------------------		-------------
		# 								BINDS,										| a | z | e |
		#           Modèle : (<touche>, <fonction>, <liste params>)		            | q | s | d |
		# -------------------------------------------------------------------		-------------
		self.accept('a', self.env.listeRobots[self.env.robotSelect].robot.changeVitAngG, [1])
		self.accept('q', self.env.listeRobots[self.env.robotSelect].robot.changeVitAngG, [-1])
		self.accept('z', self.env.listeRobots[self.env.robotSelect].robot.changeVitAng, [1])
		self.accept('s', self.env.listeRobots[self.env.robotSelect].robot.changeVitAng, [-1])
		self.accept('e', self.env.listeRobots[self.env.robotSelect].robot.changeVitAngD, [1])
		self.accept('d', self.env.listeRobots[self.env.robotSelect].robot.changeVitAngD, [-1])
		self.accept('x', self.env.addRobotSelect, [1])
		self.accept('w', self.env.addRobotSelect, [-1])
		self.accept('shift-m', self.mystere)
		# Switch entre les vues
		self.accept('arrow_up', self.taskMgr.add, [self.upCameraTask, "upCameraTask"])
		self.accept('arrow_right', self.taskMgr.add, [self.frontCameraTask, "frontCameraTask"])
		self.accept('arrow_down', self.taskMgr.add, [self.backCameraTask, "backCameraTask"])

		self.accept('5', self.taskMgr.add, [self.takePic, "takePicture"])

		self.accept('c', lambda:self.choisirStrategie(1, 120))
		self.accept('m', lambda:self.choisirStrategie(2, 20))
		self.accept('p', lambda:self.choisirStrategie(3, 15))
		self.accept('o', lambda:self.choisirStrategie(4, 120))
		self.accept('b', lambda:self.choisirStrategie(5, 0))

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
			robA.robot.draw = True
			self.controleur.lancerStrategie(carre)
			T_draw = Thread(target=self.drawOpti, daemon=True)
			T_draw.start()
			print("start")
		elif strat==2:
			arret_mur = setStrategieArretMur(robA, distance)
			self.controleur.lancerStrategie(arret_mur)
		elif strat==3:
			arret_mur2 = StrategieCond(robA, StrategieAvancer(robA,400), lambda: verifDistanceSup(robA, distance))
			self.controleur.lancerStrategie(arret_mur2)
		elif strat==4:
			carre2 = StrategieBoucle(robA, StrategieSeq([StrategieAvancer(robA, distance), StrategieTourner(robA, 90)], robA), 4)
			self.controleur.lancerStrategie(carre2)
		elif strat==5:
			balise = StrategieSuivreBalise(robA)
			self.controleur.lancerStrategie(balise)


	# -------------------- Création des objets en 3D --------------------

	def createAllRobots(self):
		""" Crée tous les robots présents dans l'environnement
		:returns: rien, va seulement créer tous les robots de l'environnement (en attribut de l'interface)
		"""
		for robA in self.env.listeRobots:
			self.createRobot(robA)

	def createRobot(self, robotA):
		"""Crée un robot en 3D (rectangle) dans l'interface
		:param robotA: adaptateur de robot
		:returns: ne retourne rien, ça initalise seulement le robot dans l'interface 3d
		"""
		robot = robotA.robot

		# toutes les variables sont reliées à un robot
		robot.format = GeomVertexFormat.getV3() # type des sommets
		robot.vdata = GeomVertexData("rectangle", robot.format, Geom.UHDynamic) # UHDynamic car les sommets vont devoir être bougés quand le robot va bouger
		robot.vertex = GeomVertexWriter(robot.vdata, "vertex")

		# Définition des sommets du robot | leur indice en comm (voir fiche thibo)
		robot.vertex.addData3f((robot.x)-(robot.width/2), self.env.length - (robot.y)-(robot.length/2), 0)  # 0 dèrrière bas gauche
		robot.vertex.addData3f((robot.x)+(robot.width/2), self.env.length - (robot.y)-(robot.length/2), 0)  # 1 derriere bas droit
		robot.vertex.addData3f((robot.x)+(robot.width/2), self.env.length - (robot.y)+(robot.length/2), 0)  # 2 devant bas droit
		robot.vertex.addData3f((robot.x)-(robot.width/2), self.env.length - (robot.y)+(robot.length/2), 0)  # 3 devant bas gauche
		robot.vertex.addData3f((robot.x)-(robot.width/2), self.env.length - (robot.y)-(robot.length/2), robot.height)  # 4 derriere haut gauche
		robot.vertex.addData3f((robot.x)+(robot.width/2), self.env.length - (robot.y)-(robot.length/2), robot.height)  # 5 derriere haut droit
		robot.vertex.addData3f((robot.x)+(robot.width/2), self.env.length - (robot.y)+(robot.length/2), robot.height)  # 6 devant haut droit
		robot.vertex.addData3f((robot.x)-(robot.width/2), self.env.length - (robot.y)+(robot.length/2), robot.height)  # 7 devant haut gauche

		# Création de l'objet (composition de triangles)
		robot.rectangle = GeomTriangles(Geom.UHDynamic)

		# Ajout des faces du carré
		# Bottom
		robot.rectangle.addVertices(0, 1, 3)
		robot.rectangle.addVertices(3, 2, 0)
		# Top
		robot.rectangle.addVertices(4, 5, 7)
		robot.rectangle.addVertices(7, 6, 4)
		# Back
		robot.rectangle.addVertices(0, 1, 5)
		robot.rectangle.addVertices(5, 4, 0)
		# Front
		robot.rectangle.addVertices(2, 3, 7)
		robot.rectangle.addVertices(7, 6, 2)
		# Left
		robot.rectangle.addVertices(0, 4, 6)
		robot.rectangle.addVertices(6, 2, 0)
		# Right
		robot.rectangle.addVertices(1, 3, 7)
		robot.rectangle.addVertices(7, 5, 1)

		# Créer un objet Geom (=l'objet du robot) pour contenir les triangles (=les faces)
		robot.geom = Geom(robot.vdata)
		robot.geom.addPrimitive(robot.rectangle)

		# Créer un nœud pour contenir le Geom
		robot.node = GeomNode("rectangle")
		robot.node.addGeom(robot.geom)

		# Créer un nœud de scène parent pour le nœud de géométrie
		robot.np = self.render.attachNewNode(robot.node) # np est le noeud de l'objet (=un ptr) dans le moteur graphique
		robot.np.setPos(0, 0, 0)  # Déplacer le triangle pour le voir

		robot.vectcouleur = DICO_COULEURS[robot.couleur]
		robot.np.setColor(robot.vectcouleur[0], robot.vectcouleur[1], robot.vectcouleur[2], robot.vectcouleur[3]) # RGB + transparence | COULEUR
		robot.np.setTwoSided(True) # pour render toutes les faces
		robot.np.node().setBounds(OmniBoundingVolume())
		robot.np.node().setFinal(True)

	def updateRobot(self, robotA):
		""" Update le visuel d'un robot dans l'interface
		:param robotA: le robotA pour lequel on veut update l'affichage
		:returns: rien, recalcule seulement les coo des sommets et update le visuel d'un robot
		"""
		robot = robotA.robot
		dx, dy = robot.direction

		robot.vertex.setRow(0)
		robot.vertex.setData3f(robot.x-(robot.width/2)*(-dy)-(robot.length/2)*dx, self.env.length - (robot.y-(robot.width/2)*(dx)-(robot.length/2)*dy), 0)  # 0 dèrrière bas gauche
		robot.vertex.setRow(1)
		robot.vertex.setData3f(robot.x+(robot.width/2)*(-dy)-(robot.length/2)*dx, self.env.length - (robot.y+(robot.width/2)*(dx)-(robot.length/2)*dy), 0)  # 1 derriere bas droit
		robot.vertex.setRow(3)
		robot.vertex.addData3f(robot.x+(robot.width/2)*(-dy)+(robot.length/2)*dx, self.env.length - (robot.y+(robot.width/2)*(dx)+(robot.length/2)*dy), 0)  # 2 devant bas droit
		robot.vertex.setRow(2)
		robot.vertex.setData3f(robot.x-(robot.width/2)*(-dy)+(robot.length/2)*dx, self.env.length - (robot.y-(robot.width/2)*(dx)+(robot.length/2)*dy), 0)  # 3 devant bas gauche
		robot.vertex.setRow(4)
		robot.vertex.setData3f(robot.x-(robot.width/2)*(-dy)-(robot.length/2)*dx, self.env.length - (robot.y-(robot.width/2)*(dx)-(robot.length/2)*dy), robot.height)  # 4 derriere haut gauche
		robot.vertex.setRow(5)
		robot.vertex.setData3f(robot.x+(robot.width/2)*(-dy)-(robot.length/2)*dx, self.env.length - (robot.y+(robot.width/2)*(dx)-(robot.length/2)*dy), robot.height)  # 5 derriere haut droit
		robot.vertex.setRow(7)
		robot.vertex.setData3f(robot.x+(robot.width/2)*(-dy)+(robot.length/2)*dx, self.env.length - (robot.y+(robot.width/2)*(dx)+(robot.length/2)*dy), robot.height)  # 6 devant haut droit
		robot.vertex.setRow(6)
		robot.vertex.setData3f(robot.x-(robot.width/2)*(-dy)+(robot.length/2)*dx, self.env.length - (robot.y-(robot.width/2)*(dx)+(robot.length/2)*dy), robot.height)  # 7 devant haut gauche

		if robot.draw and not robot.estSousControle:	# on est en train de dessiner, mais on a fini la méthode
			robot.draw = False

	def createEnvironnement(self):
		""" Crée le visuel de l'environnement dans l'interface
		:returns: rien, crée simplement l'environnement en 3D
		"""
		self.env.format = GeomVertexFormat.getV3t2()
		self.env.vdata = GeomVertexData("envi", self.env.format, Geom.UHStatic)
		self.env.vertex = GeomVertexWriter(self.env.vdata, "vertex")
		self.env.texcoord = GeomVertexWriter(self.env.vdata, "texcoord")

		# Définition des sommets et des coordonnées de texture
		self.env.vertex.addData3f(0, 0, -1)  # 0 bas gauche
		self.env.texcoord.addData2f(0, 0)
		self.env.vertex.addData3f(self.env.width, 0, -1)  # 1 bas droite
		self.env.texcoord.addData2f(1, 0)
		self.env.vertex.addData3f(0, self.env.length, -1)  # 2 haut gauche
		self.env.texcoord.addData2f(0, 1)
		self.env.vertex.addData3f(self.env.width, self.env.length, -1)  # 3 haut droit
		self.env.texcoord.addData2f(1, 1)
		# Création de l'objet + ajout du plan
		self.env.plan = GeomTriangles(Geom.UHStatic)
		self.env.plan.addVertices(0, 1, 2)
		self.env.plan.addVertices(1, 3, 2)
		# Link des données
		self.env.geom = Geom(self.env.vdata)
		self.env.geom.addPrimitive(self.env.plan)
		# Création noeud + ajout noeud dans le render
		self.env.node = GeomNode("envi")
		self.env.node.addGeom(self.env.geom)
		self.env.np = self.render.attachNewNode(self.env.node)
		self.env.np.setPos(0,0,0)
		self.env.np.setTwoSided(True)
		texture = Texture()
		texture.read("src/interface3D/source/envi.png")
		self.env.np.setTexture(texture)

	def drawOpti(self):
		"""
		Dessine la trace du robot de manière optimisée (éviter le stack overflow).
		Trace des lignes partielles à chaque pas jusqu'à tracer une vraie ligne quand il tourne.
		Chaque ligne partielle est libérée à chaque fois.
		A lancer en thread pour se faire en simultané du robot.
		"""

		def libereTabNodes(tabNodes):
			for node in tabNodes:
				node.removeNode()
		
		robot = self.env.listeRobots[self.env.robotSelect].robot
		tabDir = [robot.direction]

		tabNodesLines = [] # tab des nodes des lignes (côté entier du carré), plus tard supprimé
		tabPts = [(robot.x, self.env.length-robot.y)] # utilisé pour repérer les 4 coins du carré

		tabNodesLinesPartial = [] # tableau des lignes pas finies, plus tard supprimé
		ptsDraw = 0

		while (robot.draw and not robot.estCrash): # tant qu'on dessine
			while (((tabDir[0][0] == robot.direction[0]) or (tabDir[0][1] == robot.direction[1])) and robot.draw and not robot.estCrash): # tant que la direction ne change pas
				ptsDraw += 1
				self.drawLine((tabPts[len(tabPts)-1]), (robot.x, self.env.length-robot.y), tabNodesLinesPartial)
				# print("drawPoint")
				node = tabNodesLinesPartial.pop()
				node.removeNode()
				sleep(TIC_SIMULATION*1.5)
			
			# quand on tourne > trace la ligne complète  + on enregistre le point
			# print("draw full ligne")
			self.drawLine((tabPts[len(tabPts)-1]), (robot.x, self.env.length-robot.y), tabNodesLines) # on trace une ligne entre le dernier point et le pt actuel
			tabPts.append((robot.x, self.env.length-robot.y))

			tabDir.pop() # supprime les anciennes directions
			tabDir.append(robot.direction)

		# On supprime les lignes et les points restants à la fin du carré
		print("Suppression du tracé")
		libereTabNodes(tabNodesLines)
		libereTabNodes(tabNodesLinesPartial)
		print("Fin Tracer Carré ! youhouu")
		return


	def drawLine(self, pt1, pt2, tabNodesLines):
		"""
		Trace une ligne en 2D entre pt1 et pt2
		:param pt1: pt de départ
		:param pt2: pt d'arrivé
		"""
		# crée un objet ligne
		line = LineSegs()
		line.moveTo(pt1[0], pt1[1], 0)  # Move to the start point
		line.drawTo(pt2[0], pt2[1], 0)  # Draw to the end point

		# crée un node et lui rattache la ligne
		line_node = line.create()
		line_node_path = NodePath(line_node)

		# render le node + l'ajoute à la liste des nodes
		line_node_path.reparentTo(self.render)
		tabNodesLines.append(line_node_path)
		# print("jai ligne")

	def createAllObstacles(self):
		for obs in self.env.listeObs:
			self.createObstacle(obs, 40)

	def createObstacle(self, obs, height):
		""" Crée un obstacle en 3D à partir de ses points dans l'interface
		:param obs: obstacle
		:param height: sa hauteur
		:returns: ne retourne rien, initialise seulement un obstacle dans l'interface 3D
		"""
		obs.format = GeomVertexFormat.getV3() # type des sommets
		obs.vdata = GeomVertexData("obstacle", obs.format, Geom.UHStatic)
		obs.vertex = GeomVertexWriter(obs.vdata, "vertex")
		obs.forme = GeomTriangles(Geom.UHStatic)

		# Calcule le point central de la figure 
		x_coords = [point[0] for point in obs.lstPoints]
		y_coords = [self.env.length - point[1] for point in obs.lstPoints]
		center_x = sum(x_coords)/len(obs.lstPoints)
		center_y = sum(y_coords)/len(obs.lstPoints)
		obs.vertex.addData3f(center_x, center_y, 0)
		obs.vertex.addData3f(center_x, center_y, height)
		# Le premier sommet a donc comme indice 2 
	
		idS = 1
		for sommet in obs.lstPoints :
			# numéro pair => sommet du bas, impair => sommet du haut
			# on crée les faces directement après l'ajout dans le tableau de sommets
			obs.vertex.addData3f(sommet[0], self.env.length - sommet[1], 0) # idS-1
			obs.vertex.addData3f(sommet[0], self.env.length - sommet[1], height) # idS
			idS+=2
			if idS >=3:
				# Cotés
				obs.forme.addVertices(idS-3, idS-1, idS)
				obs.forme.addVertices(idS-3, idS-2, idS)
				# Toit
				obs.forme.addVertices(1, idS, idS-2)
		# Ferme la figure
		obs.forme.addVertices(2, 3, idS-1)
		obs.forme.addVertices(idS-1, 3, idS)
		obs.forme.addVertices(idS, 1, 2)
			
		obs.geom = Geom(obs.vdata)
		obs.geom.addPrimitive(obs.forme)
		obs.node = GeomNode("obstacle")
		obs.node.addGeom(obs.geom)

		obs.np = self.render.attachNewNode(obs.node)

		obs.vectcouleur = DICO_COULEURS["grey"]
		obs.np.setColor(obs.vectcouleur[0], obs.vectcouleur[1], obs.vectcouleur[2], obs.vectcouleur[3]) # RGB + transparence | COULEUR
		obs.np.setTwoSided(True) # pour render toutes les faces
		obs.np.node().setBounds(OmniBoundingVolume())
		obs.np.node().setFinal(True)

	def createBalise(self, balise): # Renvoie un NodePath
		"""
		Crée une balise (objet) aux coordonnées de la mouse
		:param balise: la balise que l'on souhaite créer
		:returns: le NodePath vers la balise crée (objet3D)
		"""
		self.balise = balise

		robot = self.env.listeRobots[self.env.robotSelect].robot
		# dir orthogonale à celle du rob
		self.balise.dir[1] = robot.direction[0]
		self.balise.dir[0] = robot.direction[1]

		winWidth = self.win.getXSize()
		winHeight = self.win.getYSize()

		if self.mouseWatcherNode.hasMouse(): # si la souris est déjà sur l'écran
			self.balise.x = (self.mouseWatcherNode.getMouseX() + 0.65) * winWidth / 2
			self.balise.y = (1.25- self.mouseWatcherNode.getMouseY()) * winHeight / 2
		else :
			print("Pas de souris à l'écran!")
			self.balise.x = (robot.x+1000)*self.balise.dir[0]
			self.balise.y = (robot.y+1000)*self.balise.dir[1]

		# print(self.balise.x, " ", self.balise.x)
		# print(xdir, ydir)
		
		# Define the vertex format to include texture coordinates
		self.balise.format = GeomVertexFormat.getV3t2()
		self.balise.vdata = GeomVertexData("balise", self.balise.format, Geom.UHDynamic)

		# Create writers for the vertices and texture coordinates
		self.balise.vertexBal = GeomVertexWriter(self.balise.vdata, "vertex")
		self.balise.texcoord = GeomVertexWriter(self.balise.vdata, "texcoord")

		# Add vertices and texture coordinates
		self.balise.vertexBal.addData3f(self.balise.x-self.balise.width/2*(self.balise.dir[0]), winHeight-self.balise.y-self.balise.width/2*(self.balise.dir[1]), 0)
		self.balise.texcoord.addData2f(1, 0)

		self.balise.vertexBal.addData3f(self.balise.x+self.balise.width/2*(self.balise.dir[0]), winHeight-self.balise.y+self.balise.width/2*(self.balise.dir[1]), 0)
		self.balise.texcoord.addData2f(0, 0)

		self.balise.vertexBal.addData3f(self.balise.x-self.balise.width/2*(self.balise.dir[0]), winHeight-self.balise.y-self.balise.width/2*(self.balise.dir[1]), self.balise.height)
		self.balise.texcoord.addData2f(1, 1)

		self.balise.vertexBal.addData3f(self.balise.x+self.balise.width/2*(self.balise.dir[0]), winHeight-self.balise.y+self.balise.width/2*(self.balise.dir[1]), self.balise.height)
		self.balise.texcoord.addData2f(0, 1)

		# The rest of your code...
		self.balise.balise = GeomTriangles(Geom.UHDynamic)
		self.balise.balise.addVertices(0,1,2)
		self.balise.balise.addVertices(1,2,3)

		self.balise.geom = Geom(self.balise.vdata)
		self.balise.geom.addPrimitive(self.balise.balise)

		node = GeomNode("balise")
		node.addGeom(self.balise.geom)

		self.balise.np = self.render.attachNewNode(node)
		self.balise.np.setTwoSided(True) # pour render toutes les faces
		self.balise.np.node().setBounds(OmniBoundingVolume())
		self.balise.np.node().setFinal(True)
		
		texture = Texture()
		texture.read("src/interface3D/source/balise.jpg")
		# self.balise.np.setTexScale(TextureStage.getDefault(), 0.5, 0.5)		
		self.balise.np.setTexture(texture)
		# print("balise crée")
		return self.balise.np

	def updateBalise(self):
		"""
		Méthode d'affichage et de suppression de la balise régulièrement.
		Temporaire, le temps de faire de bons updates
		Méthode lancée en threading."""

		robot = self.env.listeRobots[self.env.robotSelect].robot
		self.balise.dir[1] = robot.direction[0]
		self.balise.dir[0] = robot.direction[1]

		winWidth = self.win.getXSize()
		winHeight = self.win.getYSize()

		init = None
		if self.mouseWatcherNode.hasMouse():
			self.balise.x = (self.mouseWatcherNode.getMouseX() + 0.65) * winWidth / 2
			self.balise.y = (1.25- self.mouseWatcherNode.getMouseY()) * winHeight / 2
			init = True
			# print("update ", init)
		else :
			# print("Pas de souris à l'écran!")
			pass

		# print(self.balise.x, " ", self.balise.y)
		if init==True and self.balise.vertexBal!=None:
			self.balise.vertexBal.setRow(0)
			self.balise.vertexBal.setData3f(self.balise.x-self.balise.width/2*(self.balise.dir[0]), winHeight-self.balise.y-self.balise.width/2*(self.balise.dir[1]), 0) # 0 
			self.balise.vertexBal.setRow(1)
			self.balise.vertexBal.setData3f(self.balise.x+self.balise.width/2*(self.balise.dir[0]), winHeight-self.balise.y+self.balise.width/2*(self.balise.dir[1]), 0) # 1
			self.balise.vertexBal.setRow(2)
			self.balise.vertexBal.setData3f(self.balise.x-self.balise.width/2*(self.balise.dir[0]), winHeight-self.balise.y-self.balise.width/2*(self.balise.dir[1]), self.balise.height) # 2
			self.balise.vertexBal.setRow(3)
			self.balise.vertexBal.setData3f(self.balise.x+self.balise.width/2*(self.balise.dir[0]), winHeight-self.balise.y+self.balise.width/2*(self.balise.dir[1]), self.balise.height) # 3

	def deleteNode(self, node):
		"""
		Supprime un objet (node) de l'interface
		:param node: le node a supprimer de l'interface
		"""
		if node is not None:
			node.removeNode()

	# -------------------- Tasks pour la camera --------------------

	def spinCameraTask(self, task):
		""" Effectue une rotation de la caméra autour du robot pendant qu'il avance """
		self.camLens.setFov(45)
		robot = self.env.listeRobots[self.env.robotSelect].robot
		angleDegrees = task.time * 30.0
		angleRadians = angleDegrees * (pi / 180.0)
		radius = 300
		camera_x = robot.x + radius * cos(angleRadians)
		camera_y = robot.y + radius * sin(angleRadians)
		self.camera.setPos(camera_x, camera_y, 200)
		self.camera.lookAt(Point3(robot.x, robot.y, 0))
		return Task.cont

	def backCameraTask(self, task):
		""" Set la caméra derrière le robot et le suit lorsqu'il avance """
		self.camLens.setFov(45)
		robot = self.env.listeRobots[self.env.robotSelect].robot
		dx, dy = robot.direction
		camera_x = robot.x - 500 * dx
		camera_y = robot.y - 500 * dy
		camera_z = 500
		self.camera.setPos(camera_x, self.env.length - camera_y, camera_z)
		self.camera.lookAt(Point3(robot.x, self.env.length - robot.y, 0))
		return Task.cont

	def frontCameraTask(self, task):
		""" Set la caméra devant le robot (comme la vraie caméra) """
		robot = self.env.listeRobots[self.env.robotSelect].robot
		dx, dy = robot.direction
		camera_x = robot.x + robot.width * dx
		camera_y = self.env.length-(robot.y + robot.length * dy)
		camera_z = robot.height
		self.camera.setPos(camera_x, camera_y, camera_z)
		self.camera.lookAt(Point3(robot.x + 100 *(dx), self.env.length-(robot.y + 100 *(dy)), robot.height))
		self.camLens.setFov(140) # Réglage du FOV (champ de vision)

		return Task.cont

	def upCameraTask(self, task):
		""" Set la caméra au dessus de l'environnement (reproduction interface 2D) """
		self.camLens.setFov(90)
		cam_x = (self.env.length/2+100)
		cam_y = (self.env.width/2-100)
		cam_z = (self.env.length)
		self.camera.setPos(cam_x, cam_y, cam_z)
		self.camera.lookAt(Point3(cam_x, cam_y, 0))
		return Task.cont


	# -------------------- Méthodes liées à l'update  de l'interface --------------------


	def ticTac(self):
		""" Méthode pour update la simulation à chaque tic"""
		while self.running:
			for adapt in self.env.listeRobots:
				self.updateRobot(adapt)
			self.binds()
			self.updateBalise()
			# win = self.win

			# if self.mouseWatcherNode.hasMouse():
			# 	mouseX = self.mouseWatcherNode.getMouseX() * win.getXSize()
			# 	mouseY = win.getYSize() - self.mouseWatcherNode.getMouseY() * win.getYSize()
			# 	print(mouseX, mouseY)

			# winWidth = self.win.getXSize()
			# winHeight = self.win.getYSize()

			# print("Window size: ", winWidth, "x", winHeight)

			# self.updateCreateBalise()
			sleep(TIC_SIMULATION)

	def setDraw(self) :
		for robot in self.env.listeRobots:
			robot.robot.draw = False

	def mystere(self):
		""" Méthode secrète """
		if self.secret==False:
			self.son.play()
			self.secret=True
			print("play")
		else :
			self.son.stop()
			self.secret=False
			print("stop")


	# -------------------- Méthodes pour get les images de la caméra --------------------

	def renderToPNM(self):
		"""
		Prend une image de l'interface (vue initiale)
		:returns: une image au format PNM (+-=array)
		"""
		self.graphicsEngine.renderFrame()

		image = PNMImage()
		dr = self.camNode.getDisplayRegion(0)
		dr.getScreenshot(image)

		return image
	
	def takePic(self, task):
		"""
		Tache permettant de prendre en photo l'interface
		:option: touche '8' pour arrêter la tache
		:returns: rien, prend une photo de la scène très fréquemment et la save
		"""
		self.renderToPNM().write(Filename('src/interface3D/source/img.jpg'))
		def fin(task):
			self.taskMgr.remove('takePicture')
			print("Fin du recording")
			return Task.done

		self.accept('8', self.taskMgr.add, [fin, "finImages"])
		return Task.cont
	
	def getImage(self):
		"""
		Prend en photo l'interface 3D
		:returns: un array du screenshot de la fenêtre
		"""
		image = np.array(self.renderToPNM(), np.uint8)
		return image
	

	# --------------------------------------------------------------

class Balise:

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.dir = [0,0]