import logging
import math
from src.constantes import *

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
        self.logger.debug("get_image")

    def get_images(self):
        self.logger.debug("get_images")

    def set_motor_dps(self, port, dps):
        self.logger.debug("set_motor_dps %d %d", port, dps)
        if(port == 1 or port == 3):
            self.angleg = dps
        if(port == 2 or port == 3):
            self.angled = dps

    def get_motor_position(self):
        self.logger.debug("get_motor_position : %d %d", self.angleg, self.angled)
        return (self.angleg, self.angled)


    def offset_motor_encoder(self, port, offset):
        pass
        

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
