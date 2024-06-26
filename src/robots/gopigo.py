from math import degrees

from .adapt import Adaptateur
from src import play_audio_with_volume, DICO_COULEURS_ROBOCAR, VOL

from time import time, sleep
import numpy as np

class Adaptateur_reel(Adaptateur):
    """ Classe d'adaptation du robot réel qui hérite de la classe mockupRobot """

    def __init__(self,rob) :
        """ Constructeur de la classe Adaptateur qui va créer un robot réel """
        self.robot = rob
        self.robot.estCrash = False
        self.robot.estSousControle = False
        self.MOTOR_LEFT_RIGHT = self.robot.MOTOR_LEFT + self.robot.MOTOR_RIGHT # Port 3 correspond aux deux roues
        
        self.dist_parcourA = 0
        self.angle_parcourA = 0
        self.run = True

        self.lastDist = self.robot.get_distance()
        self.lastRefresh = time()
        
        
    def initialise(self) :
        """ Méthode qui va initialiser les moteurs du robot et les variables de distance et d'angle parcourus à 0 """
        self.robot.offset_motor_encoder(self.robot.MOTOR_LEFT, self.robot.get_motor_position()[0])
        self.robot.offset_motor_encoder(self.robot.MOTOR_RIGHT, self.robot.get_motor_position()[1])
        self.run = True
        self.dist_parcourA = 0
        self.angle_parcourA = 0


    # ------------------------ Setters de l'adaptateur ---------------------------------------

    def setVitAngDA(self, dps) :
        """ Setter de la roue droite, elle va donner la vitesse angulaire dps à la roue droite
            :param dps: vitesse angulaire que l'on veut donner à la roue droite
        """
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, dps*100)


    def setVitAngGA(self, dps) :
        """ Setter de la roue gauche, elle va donner la vitesse angulaire dps à la roue gauche
            :param dps: vitesse angulaire que l'on veut donner à la roue gauche
        """
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, dps*100)


    def setVitAngA(self, dps) :
        """ Setter qui va donner aux roues gauche et droite une certaine vitesse angulaire dps
            :param dps: la vitesse angulaire qu'on veut donner aux roues droite et gauche
        """
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT + self.robot.MOTOR_RIGHT, dps*100)


    def tourne(self, gauche, droite):
        """ Méthode qui permet de faire tourner le robot sur lui-même avec des vitesses de roues données
            :param gauche: la vitesse que l'on veut donner à la roue gauche
            :param droite: la vitesse que l'on veut donner à la roue droite
        """
        self.robot.steer(gauche, droite)


    # ------------------------ Getters de l'adaptateur ------------------------

    def getDistanceA(self) :
        """ Getter qui renvoie la distance mesurée par le capteur de distance
            :returns: la distance mesurée par le capteur de distance
        """
        tmps = time()
        if (tmps-self.lastRefresh<0.06):
            return self.lastDist
        
        self.lastDist = self.robot.get_distance()
        self.lastRefresh = tmps
        return self.lastDist
    

    def getDistanceParcourue(self) :
        """ La distance parcourue entre le point précédent et le point actuel
			:returns: la distance parcourue depuis la dernière visite à cette fonction
		"""
        ang_g, ang_d = self.robot.get_motor_position()
        print("angle dist :", ang_g, ang_d)
        dist_g = (ang_g/360) * self.robot.WHEEL_CIRCUMFERENCE
        dist_d = (ang_d/360) * self.robot.WHEEL_CIRCUMFERENCE
        print("distance dist: ", (dist_d+dist_g)/2)
        return (dist_g + dist_d)/2
    

    def getAngleParcouru(self) :
        """ Calcule l'angle parcouru par le robot
            :returns: l'angle parcouru par le robot
        """
        ang_g, ang_d = self.robot.get_motor_position()
        print("angle angle:", ang_g, ang_d)
        dist_d = (ang_d/360) * self.robot.WHEEL_CIRCUMFERENCE
        dist_g = (ang_g/360) * self.robot.WHEEL_CIRCUMFERENCE
        print("distance angle: ", degrees((dist_g-dist_d)/self.robot.WHEEL_BASE_WIDTH))
        return degrees((dist_g-dist_d)/self.robot.WHEEL_BASE_WIDTH)
    

    def get_imageA(self):
        """ Récupère la dernière image prise par le robot
            :returns: la dernière image de la cam du robot
        """
        return self.robot.get_image()
    

# ------------------------ Changement de couleur du robot ------------------------

    def changeCouleur(self, coul):
        rgb = DICO_COULEURS_ROBOCAR[coul]
        r,g,b = rgb
        self.robot._gpg.set_led(self.robot.LED_LEFT_BLINKER+self.robot.LED_LEFT_EYE+self.robot.LED_LEFT_BLINKER+self.robot.LED_RIGHT_EYE+self.robot.LED_WIFI,r, g, b)


# ------------------------ Faire jouer un son ------------------------

    def playSound(self, sound):
        play_audio_with_volume(sound, VOL)


