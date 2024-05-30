from logging import getLogger
from math import pi


class MockupRobot():
    """ Classe de simulation du robot réel """
    def __init__(self):

        self.WHEEL_BASE_WIDTH         = 117  # distance (mm) de la roue gauche a la roue droite.
        self.WHEEL_DIAMETER           = 66.5 #  diametre de la roue (mm)
        self.WHEEL_BASE_CIRCUMFERENCE = self.WHEEL_BASE_WIDTH * pi # perimetre du cercle de rotation (mm)
        self.WHEEL_CIRCUMFERENCE      = self.WHEEL_DIAMETER   * pi # perimetre de la roue (mm)
        self.MOTOR_LEFT = 1     # Port 1 correspond à la roue gauche
        self.MOTOR_RIGHT = 2    # Port 2 correspond à la roue droite
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
        if(port == 1 or port == 3):
            self.dpsg = dps
        if(port == 2 or port == 3):
            self.dpsd = dps

    def get_motor_position(self):
        self.angled += self.dpsd/2
        self.angleg += self.dpsg/2
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