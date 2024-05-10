from logging import getLogger
from math import cos, pi, sin, sqrt

from src import getAngleFromVect, getDistanceFromPts, normaliserVecteur

from .adapt import Adaptateur


class Robot :
	"""Robot - Objet aux coordonnées continues, se place dans l'environnement, avance selon une direction"""

	def __init__(self, nom, x, y, width, length, height, rayonRoue, couleur):

		""" Initialise le robot grâce avec les paramètres passés en argument
			Initialise la direction du robot à (0, -1), donc vers le bas
			:param nom: nom du robot
			:param x: coordonnée x à laquelle on veut initialiser le robot
			:param y: coordonnée y à laquelle on veut initialiser le robot
			:param width: la largeur du robot
			:param length: la longueur du robot
			:param height: la hauteur du robot (utilisé dans l'interface 3D)
			:param rayonRoue: la taille des roue
			:returns: ne retourne rien, ça initalise seulement le robot
		"""
		self.logger = getLogger(self.__class__.__name__)

		self.nom = nom
		self.x = x
		self.y = y
		self.width = width
		self.length = length
		self.height = height
		self.rayonRoue = rayonRoue # taille des roues en m donc 1 m = 1/100 cm
		self.couleur = couleur

		self.direction = (0,-1) # vecteur directeur du robot
		self._vitAngG = 0 # Vitesses angulaires des deux roues initialisées à 0
		self._vitAngD = 0 

		self.estSousControle = False 	# permet de savoir si notre robot est controlé par le controleur
		self.estCrash = False  			# Nous permet de savoir si le robot s'est crash et ne pas refresh le robot

	def refresh(self, duree):

		""" Méthode de update du robot, qui va modifier les coordonnées du robot et son vecteur directeur en fonction des vitesses angulaires des roues et du temps qui s'est écoulé depuis la dernière update.
			:param duree: le temps qui s'est écoulé depuis la dernière mise à jour du robot
			:returns: ne retourne rien, on met juste à jour le robot
		"""

		vitesse = self.getVitesse() # on récupère la vitesse du centre du robot 
		dirBasex, dirBasey = self.direction

		# on récupère les coordonnées des deux roues sous la forme de point

		vecteurOrtogonal = [dirBasex*cos(pi/2)-dirBasey*sin( pi/2),
				dirBasex*sin(pi/2)+dirBasey*cos( pi/2)]
		coordRG = (self.x-(vecteurOrtogonal[0]*(self.width/2)), self.y-(vecteurOrtogonal[1]*(self.width/2)))
		coordRD = (self.x+vecteurOrtogonal[0]*(self.width/2), self.y+vecteurOrtogonal[1]*(self.width/2))

		# on calcule le vecteur vitesse de chaque roue
		vg = self.getVitesseG()
		vg = (vg*dirBasex*duree, vg*dirBasey*duree)
		vd = self.getVitesseD()
		vd = (vd*dirBasex*duree, vd*dirBasey*duree)

		# on obtient les points qui sont au bout des vecteurs vitesse des roues
		newg = (coordRG[0] + vg[0], coordRG[1] + vg[1])
		newd = (coordRD[0] + vd[0], coordRD[1] + vd[1])

		# ce qui nous permet d'obtenir la pente entre ces deux points 
		pente = ((newg[1] - newd[1])/(newg[0] - newd[0]))

		# ceci nous permet de regler le probleme de saut lorsqu'on passe dans le cadran du bas [pi, 2pi]
		if newg[0] > newd[0]:
			pente = [-1, -pente]
		else:
			pente = [1, pente]

		# on trouve le vecteur ortogonal a notre pente
		penteOrto = [pente[0]*cos((3*pi)/2)-pente[1]*sin((3*pi)/2),
				pente[0]*sin((3*pi)/2)+pente[1]* cos((3*pi)/2)]
		penteOrto = normaliserVecteur(penteOrto) # on le normalise

		self.direction = penteOrto # il devient notre nouvelle direction

		# et on fait notre déplacement
		self.x += self.direction[0]*vitesse*duree
		self.y += self.direction[1]*vitesse*duree
	

	# Fonctions de manipulation des vitesses angulaires des roues 
 
	@property
	def vitAngG(self):
		return self._vitAngG
	

	@vitAngG.setter
	def vitAngG(self, vit):

		""" Setter de vitesse angulaire de la roue gauche
			:param vit: la vitesse anngulaire qu'on veut donner à la roue gauche
			:returns: ne retourne rien, on met juste à jour la vitesse angulaire de la roue gauche
		"""
		self._vitAngG = vit
		self.logger.debug("Vitesse roueG set à %d (%s)", vit, self.nom)

	@property
	def vitAngD(self):
		return self._vitAngD

	@vitAngD.setter
	def vitAngD(self, vit) :

		""" Setter de vitesse angulaire de la roue droite
			:param vit: vitesse angulaire que l'on veut donner à la roue droite
			:returns: ne retourne rien, on change juste la vitesse angulaire de la roue droite
		"""
		self._vitAngD = vit
		self.logger.debug("Vitesse roueD set à %d (%s)", vit, self.nom)

	def setVitAng(self, vit) :

		""" Setter qui va donner aux roues gauche et droite une certaine vitesse angulaire
			:param vit: la vitesse angulaire qu'on veut donner aux roues droite et gauche
			:returns: ne retourne rien, on met à jour les vitesses angulaires des roues
		"""
		self.vitAngD = vit
		self.vitAngG = vit
		self.logger.debug("Vitesse globale set à %d (%s)", vit, self.nom)

	def changeVitAngG(self, quant) :
		""" Setter qui ajoute quant à la vitesse angulaire de la roue gauche
			:quant: la quantite que l'on veut rajouter à la vitesse angulaire de la roue gauche
			:returns: rien, on change juste la vitesse angulaire de la roue gauche
		"""
		self.vitAngG += quant

	def changeVitAngD(self, quant) :
		""" Setter qui ajoute quant à la vitesse angulaire de la roue droite
			:quant: la quantite que l'on veut rajouter à la vitesse angulaire de la roue droite
			:returns: rien, on change juste la vitesse angulaire de la roue droite
		"""
		self.vitAngD += quant

	def changeVitAng(self, quant) :
		""" Setter qui ajoute quant aux vitesses angulaires des deux roues
			:param quant: la quantite que l'on veut rajouter aux vitesses angulaires des deux roues
			:returns: ne retourne rien, on modifie les vitesses angulaires des roues
		"""
		self.changeVitAngG(quant)
		self.changeVitAngD(quant)

	def getVitesseG(self) :
		""" Getter qui renvoir la vitesse d'un point qui serait sur la roue gauche
			:returns: la vitesse d'un point sur la roue gauche
		"""
		return self.vitAngG*self.rayonRoue
	
	def getVitesseD(self) :
		""" Getter qui renvoie la vitesse d'un point qui serait sur la roue droite
			:returns: la vitesse d'un point sur la roue droite
		"""
		return self.vitAngD*self.rayonRoue
	
	def getVitesse(self) :
		""" Getter de la vitesse du point central du robot
			:returns: la vitesse du robot en son centre
		"""
		return (self.getVitesseD() + self.getVitesseG())/2
	
	def getDistance(self, env):
		"""
		Capteur de distance du robot, donne la distance entre le pt milieu avant du robot (tete) et l'obstacle devant lui
		:returns: retourne la distance entre la tete du robot et l'obstacle le plus proche devant lui
		"""
		x1, y1 = (self.x+self.direction[0]*(self.length/2), self.y+self.direction[1]*(self.length/2))
		(x2, y2) = (x1, y1) # Le pt d'avancement est, au début, au pt de départ
		dirNorm = normaliserVecteur(self.direction)

		while ((int(y2/env.scale), int(x2/env.scale)) not in env.dicoObs):
			x2, y2 = (x2+dirNorm[0], y2+dirNorm[1]) # on avance en case suivant le vect dir

		return sqrt((x2 - x1)**2 + (y2 - y1)**2)

class Adaptateur_simule(Adaptateur) :
	""" Classe d'adaptation du robot simulé, qui hérite de la classe Robot
	"""

	def __init__(self, robot, env) :
		self.robot = robot
		self.last_point = (self.robot.x, self.robot.y)
		self.last_dir = self.robot.direction
		self.env = env
		
		self.dist_parcourA = 0
		self.angle_parcourA = 0
		self.run = True

	def initialise(self):
		""" Méthode qui initialise les moteurs du robot et les variables de distance et d'angle parcourus à 0"""
		self.last_point = (self.robot.x, self.robot.y)
		self.last_dir = self.robot.direction
		self.dist_parcourA = 0
		self.angle_parcourA = 0

	def setVitAngDA(self, vit):
		""" Setter de vitesse angulaire de la roue droite depuis l'adaptateur
			:param vit: la vitesse angulaire que l'on veut donner à la roue droite
			:returns: ne retourne rien
		"""
		self.robot.vitAngD = vit

	def setVitAngGA(self, vit) :
		""" Setter de vitesse angulaire de la roue droite depuis l'adaptateur
			:param vit: la vitesse angulaire que l'on veut donner aux roues
			:returns: ne retourne rien
		"""
		self.robot.vitAngG = vit

	def setVitAngA(self, vit) :
		""" Setter de vitesse angulaire des roues gauche et droite depuis l'adaptateur
			:param vit: la vitesse angulaire que l'on veut donner aux roues
			:returns: ne retourne rien
		"""
		self.robot.setVitAng(vit)

	def getDistanceA(self) :
		""" Capteur de distance du robot simulé depuis l'adaptateur
			:returns: la distance à l'obstacle le plus proche en regardant tout droit
		"""
		return self.robot.getDistance(self.env)

	def getDistanceParcourue(self) :
		""" La distance parcourue entre le point précédent et le point actuel
			:returns: la distance parcourue depuis la dernière visite à cette fonction
		"""
		pos_actuelle = (self.robot.x, self.robot.y)
		pos_prec = self.last_point
		return getDistanceFromPts(pos_actuelle, pos_prec)
	
	def getAngleParcouru(self) :
		""" Getter de l'angle parcouru entre le dernier point enregistré et la position actuelle du robot
			:returns: l'angle entre les deux points
		"""
		dir_actuelle = self.robot.direction
		dir_prec = self.last_dir
		return getAngleFromVect(dir_prec, dir_actuelle)