


class mockupRobot():
    def stop(self):
        pass

    def get_image(self):
        pass

    def get_images(self):
        pass

    def set_motor_dps(self, port, dps):
        print("set_motor_dps", port, dps)
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

class Adaptateur(mockupRobot) :
    def __inti(self) :
        mockupRobot.__init__(self)

    def setVitAngD(self, dps) :
        self.set_motor_dps(self.MOTOR_RIGHT, dps)

    def setVitAngG(self, dps) :
        print("setVitAngG", dps)
        self.set_motor_dps(self.MOTOR_LEFT, dps)

    def setVitAng(self, dps) :
        self.set_motor_dps(self.MOTOR_RIGHT + self.MOTOR_LEFT, dps)

    def changeVitAngG(self, quant) :
        vit = self.get_motor_position()[0]
        self.set_motor_dps(self.MOTOR_LEFT, vit + quant)

    def changeVitAngD(self, quant) :
        vit = self.get_motor_position()[1]
        self.set_motor_dps(self.MOTOR_RIGHT, vit + quant)

    def changeVitAng(self, quant) :
        vitG = self.get_motor_position()[0]
        vitD = self.get_motor_position()[1]
        self.changeVitAngG(vitG + quant)
        self.changeVitAngD(vitD +quant)
    
    def getVitesseG(self) :
        return self.get_motor_position()[0]
    
    def getVitesseD(self) :
        return self.get_motor_position()[1]
    
    def getVitesse(self) :
        vit = self.get_motor_position()[0] + self.get_motor_position()[1]
        return vit/2

    def capteurDistance(self) :
        return self.get_distance()
    
# mockupRobot = Adaptateur()
# mockupRobot.setVitAngG(20)