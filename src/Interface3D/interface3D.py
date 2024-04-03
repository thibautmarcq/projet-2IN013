# pip install panda3d==1.10.14

from ..constantes import DICO_COULEURS, TIC_SIMULATION
from ..environnement import Environnement

from direct.showbase.ShowBase import ShowBase
from direct.task import Task 
from panda3d.core import (Point3, load_prc_file, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, 
                          GeomVertexWriter, GeomNode, OmniBoundingVolume, Texture)

from math import sin, cos, pi
from time import sleep
from threading import Thread
from sys import exit
from time import sleep

load_prc_file('src/Interface3D/source/config.prc')

class Interface3D(ShowBase):

	def __init__(self, env):
		ShowBase.__init__(self)
		self.env = env
		self.createAllRobots()
		self.createEnvironnement()
		
		# Bind quitter la fenêtre
		self.accept('escape', exit)
		# Bind changement de robot
		self.accept('x', self.env.addRobotSelect, [1])
		self.accept('w', self.env.addRobotSelect, [-1])

		self.son = self.loader.loadSfx("src/Interface3D/source/secret.mp3")
		self.secret = False

		# self.taskMgr.add(self.cameraUpTask, "cameraUpTask")
		self.taskMgr.add(self.spinCameraTask, "spinCameraTask")
		# self.taskMgr.add(self.updateCameraTask, "updateCameraTask")

		self.camLens.setFar(100000) # Pour ne pas avoir de problème de distance de vue
		T_tictac = Thread(target=self.ticTac, daemon=True)
		T_tictac.start()

	def binds(self):
		""" Bind les touches pour les déplacements des robots """
		# -------------------------------------------------------------------		-------------
		# 								BINDS,										| a | z | e |
		#           Modèle : (<touche>, <fonction>, <liste params>)		            | q | s | d |
		# -------------------------------------------------------------------		-------------
		self.accept('a', self.env.listeRobots[self.env.robotSelect].robot.changeVitAngG, [-1])
		self.accept('q', self.env.listeRobots[self.env.robotSelect].robot.changeVitAngG, [1])
		self.accept('z', self.env.listeRobots[self.env.robotSelect].robot.changeVitAng, [-1])
		self.accept('s', self.env.listeRobots[self.env.robotSelect].robot.changeVitAng, [1])
		self.accept('e', self.env.listeRobots[self.env.robotSelect].robot.changeVitAngD, [-1])
		self.accept('d', self.env.listeRobots[self.env.robotSelect].robot.changeVitAngD, [1])
		self.accept('x', self.env.addRobotSelect, [1])
		self.accept('w', self.env.addRobotSelect, [-1])
		self.accept('shift-m', self.mystere)


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
		robot.vertex.addData3f((robot.x)-(robot.width/2), (robot.y)-(robot.length/2), 0)  # 0 dèrrière bas gauche
		robot.vertex.addData3f((robot.x)+(robot.width/2), (robot.y)-(robot.length/2), 0)  # 1 derriere bas droit
		robot.vertex.addData3f((robot.x)+(robot.width/2), (robot.y)+(robot.length/2), 0)  # 2 devant bas droit
		robot.vertex.addData3f((robot.x)-(robot.width/2), (robot.y)+(robot.length/2), 0)  # 3 devant bas gauche
		robot.vertex.addData3f((robot.x)-(robot.width/2), (robot.y)-(robot.length/2), robot.height)  # 4 derriere haut gauche
		robot.vertex.addData3f((robot.x)+(robot.width/2), (robot.y)-(robot.length/2), robot.height)  # 5 derriere haut droit
		robot.vertex.addData3f((robot.x)+(robot.width/2), (robot.y)+(robot.length/2), robot.height)  # 6 devant haut droit
		robot.vertex.addData3f((robot.x)-(robot.width/2), (robot.y)+(robot.length/2), robot.height)  # 7 devant haut gauche

		# Création de l'objet (composition de triangles)
		robot.rectangle = GeomTriangles(Geom.UHDynamic)

		# Ajout des faces du carré
		# Bottom
		robot.rectangle.addVertices(0, 1, 2)
		robot.rectangle.addVertices(2, 3, 0)
		# Top
		robot.rectangle.addVertices(4, 5, 6)
		robot.rectangle.addVertices(6, 7, 4)
		# Back
		robot.rectangle.addVertices(0, 1, 5)
		robot.rectangle.addVertices(5, 4, 0)
		# Front
		robot.rectangle.addVertices(3, 2, 6)
		robot.rectangle.addVertices(6, 7, 3)
		# Left
		robot.rectangle.addVertices(0, 4, 7)
		robot.rectangle.addVertices(7, 3, 0)
		# Right
		robot.rectangle.addVertices(1, 2, 6)
		robot.rectangle.addVertices(6, 5, 1)
		
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
		robot.vertex.setData3f(robot.x-(robot.width/2)*(-dy)-(robot.length/2)*dx, robot.y-(robot.width/2)*(dx)-(robot.length/2)*dy, 0)  # 0 dèrrière bas gauche
		robot.vertex.setRow(1)
		robot.vertex.setData3f(robot.x+(robot.width/2)*(-dy)-(robot.length/2)*dx, robot.y+(robot.width/2)*(dx)-(robot.length/2)*dy, 0)  # 1 derriere bas droit
		robot.vertex.setRow(2)
		robot.vertex.addData3f(robot.x+(robot.width/2)*(-dy)+(robot.length/2)*dx, robot.y+(robot.width/2)*(dx)+(robot.length/2)*dy, 0)  # 2 devant bas droit
		robot.vertex.setRow(3)
		robot.vertex.setData3f(robot.x-(robot.width/2)*(-dy)+(robot.length/2)*dx, robot.y-(robot.width/2)*(dx)+(robot.length/2)*dy, 0)  # 3 devant bas gauche
		robot.vertex.setRow(4)
		robot.vertex.setData3f(robot.x-(robot.width/2)*(-dy)-(robot.length/2)*dx, robot.y-(robot.width/2)*(dx)-(robot.length/2)*dy, robot.height)  # 4 derriere haut gauche
		robot.vertex.setRow(5)
		robot.vertex.setData3f(robot.x+(robot.width/2)*(-dy)-(robot.length/2)*dx, robot.y+(robot.width/2)*(dx)-(robot.length/2)*dy, robot.height)  # 5 derriere haut droit
		robot.vertex.setRow(6)
		robot.vertex.setData3f(robot.x+(robot.width/2)*(-dy)+(robot.length/2)*dx, robot.y+(robot.width/2)*(dx)+(robot.length/2)*dy, robot.height)  # 6 devant haut droit
		robot.vertex.setRow(7)
		robot.vertex.setData3f(robot.x-(robot.width/2)*(-dy)+(robot.length/2)*dx, robot.y-(robot.width/2)*(dx)+(robot.length/2)*dy, robot.height)  # 7 devant haut gauche


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
		texture.read("src/Interface3D/source/envi.png")
		self.env.np.setTexture(texture)
		
	def ticTac(self):
		while True:
			for adapt in self.env.listeRobots:
				# print('oui')
				self.updateRobot(adapt)
			self.binds()
			sleep(TIC_SIMULATION)

	# Task pour faire rotate la camera
	def spinCameraTask(self, task):
		""" Effectue une rotation de la caméra autour du robot pendant qu'il avance """
		robot = self.env.listeRobots[self.env.robotSelect].robot
		angleDegrees = task.time * 30.0
		angleRadians = angleDegrees * (pi / 180.0)
		radius = 300
		camera_x = robot.x + radius * cos(angleRadians)
		camera_y = robot.y + radius * sin(angleRadians)
		self.camera.setPos(camera_x, camera_y, 200) 
		self.camera.lookAt(Point3(robot.x, robot.y, 0))
		return Task.cont

	# Task pour suivre le robot
	def updateCameraTask(self, task):
		""" Set la caméra derrière le robot et le suit pendant qu'il avance """
		robot = self.env.listeRobots[self.env.robotSelect].robot
		dx, dy = robot.direction
		camera_x = float(dx)*(robot.x - 150)
		camera_y = float(dy)*(robot.y - 200)
		camera_z = 500
		self.camera.setPos(camera_x, camera_y, camera_z)
		self.camera.lookAt(Point3(robot.x, robot.y, 0))
		return Task.cont
	
	def cameraUpTask(self, task):
		""" Set la caméra tout en haut de l'environnement et suit le robot """
		robot = self.env.listeRobots[self.env.robotSelect].robot

		cam_x = (self.env.length/2)
		cam_y = (self.env.width/2)
		cam_z = (self.env.length)
		self.camera.setPos(cam_x, cam_y, 750)
		# self.camera.lookAt(Point3(cam_x, cam_y, 0))
		self.camera.lookAt(Point3(robot.x, robot.y, 0))
		return Task.cont

	
	def ticTac(self):
		while True:
			for adapt in self.env.listeRobots:
				# print('oui')
				self.updateRobot(adapt)
				self.updateCameraTask(adapt)
			self.binds()
			sleep(TIC_SIMULATION)
	
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