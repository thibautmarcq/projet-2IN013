from robot2IN013 import Robot2IN013
import math

WHEEL_BASE_WIDTH         = 117  # distance (mm) de la roue gauche a la roue droite.
WHEEL_DIAMETER           = 66.5 #  diametre de la roue (mm)
WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi # perimetre du cercle de rotation (mm)
WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * math.pi # perimetre de la roue (mm)

class Adaptateur(Robot2IN013) :
    """
    Classe d'adaptation du robot réel qui hérite de la classe mockupRobot
    """
    def __init__(self) :
        """
        Constructeur de la classe Adaptateur qui va créer un objet de la classe mockupRobot
        """
        Robot2IN013.__init__(self)
        self.estCrash = False
        self.estSousControle = False
        self.MOTOR_LEFT_RIGHT = self.MOTOR_LEFT + self.MOTOR_RIGHT # Port 3 correspond aux deux roues

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
        return self.get_distance()
    
    def distance_parcourue(self) :
        ang_g, ang_d = self.get_motor_position()
        self.offset_motor_encoder(self.MOTOR_LEFT_RIGHT, 0)
        dist_g = (ang_g/360) * WHEEL_CIRCUMFERENCE
        dist_d = (ang_d/360) * WHEEL_CIRCUMFERENCE
        return (dist_g + dist_d)/2
    
    def angle_parcouru(self) :
        ang_g, ang_d = self.get_motor_position()
        self.offset_motor_encoder(self.MOTOR_LEFT_RIGHT, 0)
        dist_d = (ang_d/360) * math.pi * WHEEL_CIRCUMFERENCE
        dist_g = (ang_g/360) * math.pi * WHEEL_CIRCUMFERENCE
        return math.degrees((dist_g-dist_d)/WHEEL_BASE_WIDTH)


