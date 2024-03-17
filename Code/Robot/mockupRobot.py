


class mockupRobot():
    """
    Classe de simulation du robot réel
    """
    def __init__(self):
        self.estSousControle = False
        self.estCrash = False

    def stop(self):
        pass

    def get_image(self):
        print("get_image")
        pass

    def get_images(self):
        print("get_images")
        pass

    def set_motor_dps(self, port, dps):
        print("set_motor_dps", port, dps)
        pass

    def get_motor_position(self):
        print("get_motor_position")
        pass

    def offset_motor_encoder(self, port, offset):
        print("offset_motor_encoder", port, offset)
        pass

    def get_distance(self):
        print("get_distance")
        pass

    def servo_rotate(self,position):
        print("servo_rotate", position)
        pass

    def start_recording(self):
        print("start_recording")
        pass

    def _stop_recording(self):
        print("_stop_recording")
        pass

    def _start_recording(self):
        print("_start_recording")
        pass

    def __getattr__(self,attr):
        print("getattr", attr)
        pass

class Adaptateur(mockupRobot) :
    """
    Classe d'adaptation du robot réel qui hérite de la classe mockupRobot
    """
    def __init__(self) :
        """
        Constructeur de la classe Adaptateur qui va créer un objet de la classe mockupRobot
        """
        mockupRobot.__init__(self)
        self.MOTOR_LEFT = 1     # Port 1 correspond à la roue gauche
        self.MOTOR_RIGHT = 2    # Port 2 correspond à la roue droite
        self.MOTOR_LEFT_RIGHT = self.MOTOR_LEFT + self.MOTOR_RIGHT # Port 3 correspond aux deux roues

    def setVitAngD(self, dps) :
        """
        Setter de la roue droite, elle va donner la vitesse angulaire dps à la roue droite
        :param dps: vitesse angulaire que l'on veut donner à la roue droite
        """
        print("setVitAngD =", dps)
        self.set_motor_dps(self.MOTOR_RIGHT, dps)

    def setVitAngG(self, dps) :
        """
        Setter de la roue gauche, elle va donner la vitesse angulaire dps à la roue gauche
        :param dps: vitesse angulaire que l'on veut donner à la roue gauche
        """
        print("setVitAngG =", dps)
        self.set_motor_dps(self.MOTOR_LEFT, dps)

    def setVitAng(self, dps) :
        """
        Setter qui va donner aux roues gauche et droite une certaine vitesse angulaire dps
        :param dps: la vitesse angulaire qu'on veut donner aux roues droite et gauche
        """
        print("setVitAng =", dps)
        self.set_motor_dps(self.MOTOR_RIGHT + self.MOTOR_LEFT, dps)

    def capteurDistance(self) :
        """
        Getter qui renvoie la distance mesurée par le capteur de distance
        :returns: la distance mesurée par le capteur de distance
        """
        print("capteurDistance")
        return self.get_distance()
    
# mockupRobot = Adaptateur()
# mockupRobot.setVitAngG(20)
# print(mockupRobot.estSousControle)
# print(mockupRobot.estCrash)
