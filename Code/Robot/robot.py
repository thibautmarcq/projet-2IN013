import logging
import math
import time
from Code.outil import *


class Robot :
	"""Robot - Objet aux coordonnées continues, se place dans l'environnement, avance selon une direction"""

	def __init__(self, nom, x, y, width, length, rayonRoue):

		""" Initialise le robot grâce avec les paramètres passés en argument
			Initialise la direction du robot à (0, -1), donc vers le bas
			:param nom: nom du robot
			:param x: coordonnée x à laquelle on veut initialiser le robot
			:param y: coordonnée y à laquelle on veut initialiser le robot
			:param width: la largeur du robot
			:param length: la longueur du robot
			:param rayonRoue: la taille des roue
			:returns: ne retourne rien, ça initalise seulement le robot
		"""
		self.logger = logging.getLogger(self.__class__.__name__)

		self.nom = nom
		self.x = x
		self.y = y
		self.width = width
		self.length = length
		self.rayonRoue = rayonRoue # taille des roues en m donc 1 m = 1/100 cm

		self.direction = (0,-1) # vecteur directeur du robot
		self.vitAngG = 0 # Vitesses angulaires des deux roues initialisées à 0
		self.vitAngD = 0 

		self.estSousControle = False 	# permet de savoir si notre robot est controler par le controleur
		self.estCrash = False  			# Nous permet de savoir si le robot s'est crash et ne pas refresh le robot


	def refresh(self, duree):

		""" Méthode de update du robot, qui va modifier les coordonnées du robot et son vecteur directeur en fonction des vitesses angulaires des roues et du temps qui s'est écoulé depuis la dernière update.
			:param duree: le temps qui s'est écoulé depuis la dernière mise à jour du robot
			:returns: ne retourne rien, on met juste à jour le robot
		"""

		vit = self.getVitesse() # on récupère la vitesse du centre du robot 
		dirBasex, dirBasey = self.direction

		# on récupère les coordonnées des deux roues sous la forme de point

		orto = [dirBasex*math.cos(math.pi/2)-dirBasey*math.sin(math.pi/2),
				dirBasex*math.sin(math.pi/2)+dirBasey*math.cos(math.pi/2)]
		coordRG = (self.x-(orto[0]*(self.width/2)), self.y-(orto[1]*(self.width/2)))
		coordRD = (self.x+orto[0]*(self.width/2), self.y+orto[1]*(self.width/2))

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
		penteOrto = [pente[0]*math.cos((3*math.pi)/2)-pente[1]*math.sin((3*math.pi)/2),
				pente[0]*math.sin((3*math.pi)/2)+pente[1]*math.cos((3*math.pi)/2)]
		penteOrto = normaliserVecteur(penteOrto) # on le normalise

		self.direction = penteOrto # il devient notre nouvelle direction

		# et on fait notre déplacement
		self.x += self.direction[0]*vit*duree
		self.y += self.direction[1]*vit*duree
	

	# Fonctions de manipulation des vitesses angulaires des roues 

	def setVitAngG(self, vit) :

		""" Setter de vitesse angulaire de la roue gauche
			:param vit: la vitesse anngulaire qu'on veut donner à la roue gauche
			:returns: ne retourne rien, on met juste à jour la vitesse angulaire de la roue gauche
		"""
		self.vitAngG = vit
		self.logger.debug("Vitesse roueG set à %d (%s)", vit, self.nom)

	def setVitAngD(self, vit) :

		""" Setter de vitesse angulaire de la roue droite
			:param vit: vitesse angulaire que l'on veut donner à la roue droite
			:returns: ne retourne rien, on change juste la vitesse angulaire de la roue droite
		"""
		self.vitAngD = vit
		self.logger.debug("Vitesse roueD set à %d (%s)", vit, self.nom)

	def setVitAng(self, vit) :

		""" Setter qui va donner aux roues gauche et droite une certaine vitesse angulaire
			:param vit: la vitesse angulaire qu'on veut donner aux roues droite et gauche
			:returns: ne retourne rien, on met à jour les vitesses angulaires des roues
		"""
		self.setVitAngD(vit)
		self.setVitAngG(vit)
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
	
	def capteurDistance(self, env):
		"""
		Capteur de distance du robot, donne la distance entre le pt milieu avant du robot (tete) et l'obstacle devant lui
		:param env: l'environnement dans lequel se trouve le robot
		:returns: retourne la distance entre la tete du robot et l'obstacle le plus proche devant lui
		"""
		x1, y1 = (self.x+self.direction[0]*(self.length/2), self.y+self.direction[1]*(self.length/2))
		mat = env.matrice
		(x2, y2) = (x1, y1) # Le pt d'avancement est, au début, au pt de départ
		dirNorm = normaliserVecteur(self.direction)

		while (mat[int(y2/env.scale)][int(x2/env.scale)]!=2): # Condition de boucle : tant qu'on est pas sur un obstacle
			x2, y2 = (x2+dirNorm[0], y2+dirNorm[1]) # on avance en case suivant le vect dir

		return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
	
class Adaptateur_simule(Robot) :
	""" Classe d'adaptation du robot simulé, qui hérite de la classe Robot
	"""

	def __init__(self, nom, x, y, width, length, rayonRoue) :
		Robot.__init__(self, nom, x, y, width, length, rayonRoue)
		self.last_point = (x, y)
		self.last_dir = self.direction

	def setVitAngDA(self, vit):
		""" Setter de vitesse angulaire de la roue droite depuis l'adaptateur
			:param vit: la vitesse angulaire que l'on veut donner à la roue droite
			:returns: ne retourne rien
		"""
		self.setVitAngD(vit)

	def setVitAngGA(self, vit) :
		""" Setter de vitesse angulaire de la roue droite depuis l'adaptateur
			:param vit: la vitesse angulaire que l'on veut donner aux roues
			:returns: ne retourne rien
		"""
		self.setVitAngG(vit)

	def setVitAngA(self, vit) :
		""" Setter de vitesse angulaire des roues gauche et droite depuis l'adaptateur
			:param vit: la vitesse angulaire que l'on veut donner aux roues
			:returns: ne retourne rien
		"""
		self.setVitAng(vit)

	def capteurDistanceA(self) :
		""" Capteur de distance du robot simulé depuis l'adaptateur
			:returns: la distance à l'obstacle le plus proche en regardant tout droit
		"""
		return self.capteurDistance()

	def distance_parcourue(self) :
		""" La distance parcourue entre le point précédent et le point actuel
			:returns: la distance parcourue depuis la dernière visite à cette fonction
		"""
		pos_actuelle = (self.x, self.y)
		pos_prec = self.last_point
		self.last_point = pos_actuelle
		self.last_dir = self.direction
		return distance(pos_actuelle, pos_prec)
	
	def angle_parcouru(self) :
		""" Getter de l'angle parcouru entre le dernier point enregistré et la position actuelle du robot
			:returns: l'angle entre les deux points
		"""
		dir_actuelle = self.direction
		dir_prec = self.last_dir
		self.last_dir = dir_actuelle
		self.last_point = (self.x, self.y)
		return getAngleFromVect(dir_prec, dir_actuelle)
	
