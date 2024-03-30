from robot2IN013 import Robot2IN013 # Import de l'API, supposée être sur le robot ?
from math import degrees, pi

class Adaptateur_reel:
    """
    Classe d'adaptation du robot réel qui hérite de la classe mockupRobot
    """
    def __init__(self) :
        """
        Constructeur de la classe Adaptateur qui va créer un robot réel
        """
        self.robot = Robot2IN013()
        self.robot.estCrash = False
        self.robot.estSousControle = False
        self.robot.MOTOR_LEFT_RIGHT = self.robot.MOTOR_LEFT + self.robot.MOTOR_RIGHT # Port 3 correspond aux deux roues

        
    # def initialise(self) :
    #     self.offset_motor_encoder(self.MOTOR_LEFT_RIGHT, 0)

    def setVitAngDA(self, dps) :
        """
        Setter de la roue droite, elle va donner la vitesse angulaire dps à la roue droite
        :param dps: vitesse angulaire que l'on veut donner à la roue droite
        """
        self.set_motor_dps(self.MOTOR_RIGHT, dps)

    def setVitAngGA(self, dps) :
        """
        Setter de la roue gauche, elle va donner la vitesse angulaire dps à la roue gauche
        :param dps: vitesse angulaire que l'on veut donner à la roue gauche
        """
        self.set_motor_dps(self.MOTOR_LEFT, dps)

    def setVitAngA(self, dps) :
        """
        Setter qui va donner aux roues gauche et droite une certaine vitesse angulaire dps
        :param dps: la vitesse angulaire qu'on veut donner aux roues droite et gauche
        """
        self.set_motor_dps(self.MOTOR_RIGHT + self.MOTOR_LEFT, dps)

    def capteurDistanceA(self) :
        """
        Getter qui renvoie la distance mesurée par le capteur de distance
        :returns: la distance mesurée par le capteur de distance
        """
        return self.robot.get_distance()
    
    def distance_parcourue(self) :
        ang_g, ang_d = self.robot.get_motor_position()
        self.robot.offset_motor_encoder(self.robot.MOTOR_LEFT_RIGHT, 0)
        dist_g = (ang_g/360) * WHEEL_CIRCUMFERENCE
        dist_d = (ang_d/360) * WHEEL_CIRCUMFERENCE
        return (dist_g + dist_d)/2
    
    def angle_parcouru(self) :
        ang_g, ang_d = self.robot.get_motor_position()
        self.robot.offset_motor_encoder(self.robot.MOTOR_LEFT_RIGHT, 0)
        dist_d = (ang_d/360) * pi * WHEEL_CIRCUMFERENCE
        dist_g = (ang_g/360) * pi * WHEEL_CIRCUMFERENCE
        return degrees((dist_g-dist_d)/WHEEL_BASE_WIDTH)


