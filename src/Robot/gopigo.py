from math import degrees, pi
from threading import Thread  

from .adapt import Adaptateur


class Adaptateur_reel(Adaptateur):
    """
    Classe d'adaptation du robot réel qui hérite de la classe mockupRobot
    """
    def __init__(self,rob) :
        """
        Constructeur de la classe Adaptateur qui va créer un robot réel
        """
        self.robot = rob
        self.robot.estCrash = False
        self.robot.estSousControle = False
        self.MOTOR_LEFT_RIGHT = self.robot.MOTOR_LEFT + self.robot.MOTOR_RIGHT # Port 3 correspond aux deux roues
        
        self.dist_parcourA = 0
        self.angle_parcourA = 0
        self.run = True
        t1 = Thread(target=self.updateDistAng, daemon=True)
        t1.start()
	
        
    def initialise(self) :
        """
        Méthode qui va initialiser les moteurs du robot et les variables de distance et d'angle parcourus à 0
        """
        self.robot.offset_motor_encoder(self.robot.MOTOR_LEFT, self.robot.get_motor_position()[0])
        self.robot.offset_motor_encoder(self.robot.MOTOR_RIGHT, self.robot.get_motor_position()[1])
        self.run = True
        self.dist_parcourA = 0
        self.angle_parcourA = 0

    def setVitAngDA(self, dps) :
        """
        Setter de la roue droite, elle va donner la vitesse angulaire dps à la roue droite
        :param dps: vitesse angulaire que l'on veut donner à la roue droite
        """
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, dps*100)

    def setVitAngGA(self, dps) :
        """
        Setter de la roue gauche, elle va donner la vitesse angulaire dps à la roue gauche
        :param dps: vitesse angulaire que l'on veut donner à la roue gauche
        """
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, dps*100)

    def setVitAngA(self, dps) :
        """
        Setter qui va donner aux roues gauche et droite une certaine vitesse angulaire dps
        :param dps: la vitesse angulaire qu'on veut donner aux roues droite et gauche
        """
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT + self.robot.MOTOR_RIGHT, dps*100)

    def capteurDistanceA(self) :
        """
        Getter qui renvoie la distance mesurée par le capteur de distance
        :returns: la distance mesurée par le capteur de distance
        """
        return self.robot.get_distance()
    
    def distanceParcourue(self) :
        """ La distance parcourue entre le point précédent et le point actuel
			:returns: la distance parcourue depuis la dernière visite à cette fonction
		"""
        ang_g, ang_d = self.robot.get_motor_position()
        dist_g = (ang_g/360) * self.robot.WHEEL_CIRCUMFERENCE
        dist_d = (ang_d/360) * self.robot.WHEEL_CIRCUMFERENCE
        return (dist_g + dist_d)/2
    
    def angleParcouru(self) :
        """
        Calcule l'angle parcouru par le robot
        :returns: l'angle parcouru par le robot
        """
        ang_g, ang_d = self.robot.get_motor_position()
        dist_d = (ang_d/360) * pi * self.robot.WHEEL_CIRCUMFERENCE
        dist_g = (ang_g/360) * pi * self.robot.WHEEL_CIRCUMFERENCE
        return degrees((dist_g-dist_d)/self.robot.WHEEL_BASE_WIDTH)


