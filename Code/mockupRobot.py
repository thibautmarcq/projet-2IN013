from Code.robot import *

class mockupRobot():
    def stop(self):
        pass

    def get_image(self):
        pass

    def get_images(self):
        pass

    def set_motor_dps(self, port, dps):
        pass

    def get_motor_position(self):
        pass

    def offset_motor_encoder(self, port, offset):
        pass

    def get_distance(self):
        pass

    def servo_rotate(self,position):
        pass

    def start_recording(self):
        pass

    def _stop_recording(self):
        pass

    def _start_recording(self):
        pass

    def __getattr__(self,attr):
        pass