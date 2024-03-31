from logging import getLogger
from math import degrees, pi
from .adapt import Adaptateur

WHEEL_BASE_WIDTH         = 117  # distance (mm) de la roue gauche a la roue droite.
WHEEL_DIAMETER           = 66.5 #  diametre de la roue (mm)
WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * pi # perimetre du cercle de rotation (mm)
WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * pi # perimetre de la roue (mm)

class mockupRobot():
    """
    Classe de simulation du robot réel
    """
    def __init__(self):
        self.logger = getLogger(self.__class__.__name__)
        self.dpsg = 0
        self.dpsd = 0
        self.angled = 0
        self.angleg = 0

    def stop(self):
        pass

    def get_image(self):
        self.logger.debug("get_image")

    def get_images(self):
        self.logger.debug("get_images")

    def set_motor_dps(self, port, dps):
        self.logger.debug("set_motor_dps %d %d", port, dps)
        if(port == 1 or port == 3):
            self.dpsg = dps
        if(port == 2 or port == 3):
            self.dpsd = dps

    def get_motor_position(self):
        self.angled += self.dpsd
        self.angleg += self.dpsg
        self.logger.debug("get_motor_position : %d %d", self.angleg, self.angled)
        return (self.angleg, self.angled)


    def offset_motor_encoder(self, port, offset):
        if(port == 1 or port == 3):
            self.angleg = offset
        if(port == 2 or port == 3):
            self.angled = offset
        

    def get_distance(self):
        self.logger.debug("get_distance")
        return 15

    def servo_rotate(self,position):
        self.logger.debug("servo_rotate = %d", position)

    def start_recording(self):
        self.logger.debug("start_recording")

    def _stop_recording(self):
        self.logger.debug("_stop_recording")

    def _start_recording(self):
        self.logger.debug("_start_recording")

    def __getattr__(self,attr):
        pass

class Adaptateur_reel(Adaptateur) :
    """
    Classe d'adaptation du robot réel qui hérite de la classe mockupRobot
    """
    def __init__(self) :
        """
        Constructeur de la classe Adaptateur qui va créer un objet de la classe mockupRobot
        """
        self.robot = mockupRobot()
        self.MOTOR_LEFT = 1     # Port 1 correspond à la roue gauche
        self.MOTOR_RIGHT = 2    # Port 2 correspond à la roue droite
        self.MOTOR_LEFT_RIGHT = self.MOTOR_LEFT + self.MOTOR_RIGHT # Port 3 correspond aux deux roues
        
        self.robot.estCrash = False
        self.robot.estSousControle = False
        
    def initialise(self) :
        self.robot.offset_motor_encoder(self.MOTOR_LEFT_RIGHT, 0)

    def setVitAngDA(self, dps) :
        """
        Setter de la roue droite, elle va donner la vitesse angulaire dps à la roue droite
        :param dps: vitesse angulaire que l'on veut donner à la roue droite
        """
        self.robot.set_motor_dps(self.MOTOR_RIGHT, dps)

    def setVitAngGA(self, dps) :
        """
        Setter de la roue gauche, elle va donner la vitesse angulaire dps à la roue gauche
        :param dps: vitesse angulaire que l'on veut donner à la roue gauche
        """
        self.robot.set_motor_dps(self.MOTOR_LEFT, dps)

    def setVitAngA(self, dps) :
        """
        Setter qui va donner aux roues gauche et droite une certaine vitesse angulaire dps
        :param dps: la vitesse angulaire qu'on veut donner aux roues droite et gauche
        """
        self.robot.set_motor_dps(self.MOTOR_RIGHT + self.MOTOR_LEFT, dps)

    def capteurDistanceA(self) :
        """
        Getter qui renvoie la distance mesurée par le capteur de distance
        :returns: la distance mesurée par le capteur de distance
        """
        return self.robot.get_distance()

    def distance_parcourue(self) :
        ang_g, ang_d = self.robot.get_motor_position()
        dist_g = (ang_g/360) * WHEEL_CIRCUMFERENCE
        dist_d = (ang_d/360) * WHEEL_CIRCUMFERENCE
        return (dist_g + dist_d)/2

    def angle_parcouru(self) :
        ang_g, ang_d = self.robot.get_motor_position()
        dist_d = (ang_d/360) * pi * WHEEL_CIRCUMFERENCE
        dist_g = (ang_g/360) * pi * WHEEL_CIRCUMFERENCE
        return degrees((dist_g-dist_d)/WHEEL_BASE_WIDTH)