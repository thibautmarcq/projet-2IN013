import math
import logging

WHEEL_BASE_WIDTH         = 117  # distance (mm) de la roue gauche a la roue droite.
WHEEL_DIAMETER           = 66.5 #  diametre de la roue (mm)
WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi # perimetre du cercle de rotation (mm)
WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * math.pi # perimetre de la roue (mm)


class mockupRobot():
    """
    Classe de simulation du robot réel
    """

    def __init__(self, ):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.estSousControle = False
        self.estCrash = False
        self.angled = 0
        self.angleg = 0

    def stop(self):
        pass

    def get_image(self):
        print("get_image")

    def get_images(self):
        print("get_images")

    def set_motor_dps(self, port, dps):
        self.logger.debug("set_motor_dps %d %d", port, dps)
        self.angled += dps
        self.angleg += dps

    def get_motor_position(self):
        self.logger.debug("get_motor_position : %d %d", self.angleg, self.angled)
        return (self.angleg, self.angled)


    def offset_motor_encoder(self, port, offset):
        self.logger.debug("offset_motor_encoder %d %d", port, offset)
        

    def get_distance(self):
        self.logger.debug("get_distance")
        return 15

    def servo_rotate(self,position):
        print("servo_rotate", position)

    def start_recording(self):
        print("start_recording")

    def _stop_recording(self):
        print("_stop_recording")

    def _start_recording(self):
        print("_start_recording")

    def __getattr__(self,attr):
        print("getattr", attr)

class Adaptateur(mockupRobot) :
    """
    Classe d'adaptation du robot réel qui hérite de la classe mockupRobot
    """
    def __init__(self) :
        """
        Constructeur de la classe Adaptateur qui va créer un objet de la classe mockupRobot
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        mockupRobot.__init__(self)
        self.MOTOR_LEFT = 1     # Port 1 correspond à la roue gauche
        self.MOTOR_RIGHT = 2    # Port 2 correspond à la roue droite
        self.MOTOR_LEFT_RIGHT = self.MOTOR_LEFT + self.MOTOR_RIGHT # Port 3 correspond aux deux roues

    def setVitAngDA(self, dps) :
        """
        Setter de la roue droite, elle va donner la vitesse angulaire dps à la roue droite
        :param dps: vitesse angulaire que l'on veut donner à la roue droite
        """
        print("setVitAngD =", dps)
        self.set_motor_dps(self.MOTOR_RIGHT, dps)

    def setVitAngGA(self, dps) :
        """
        Setter de la roue gauche, elle va donner la vitesse angulaire dps à la roue gauche
        :param dps: vitesse angulaire que l'on veut donner à la roue gauche
        """
        print("setVitAngG =", dps)
        self.set_motor_dps(self.MOTOR_LEFT, dps)

    def setVitAngA(self, dps) :
        """
        Setter qui va donner aux roues gauche et droite une certaine vitesse angulaire dps
        :param dps: la vitesse angulaire qu'on veut donner aux roues droite et gauche
        """
        print("setVitAng =", dps)
        self.set_motor_dps(self.MOTOR_RIGHT + self.MOTOR_LEFT, dps)

    def capteurDistanceA(self) :
        """
        Getter qui renvoie la distance mesurée par le capteur de distance
        :returns: la distance mesurée par le capteur de distance
        """
        print("capteurDistance")
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
        dist_d = (ang_d/360) * WHEEL_CIRCUMFERENCE
        return (dist_d)/WHEEL_BASE_WIDTH

    
# mockupRobot = Adaptateur()
# mockupRobot.setVitAngG(20)
# print(mockupRobot.estSousControle)
# print(mockupRobot.estCrash)
