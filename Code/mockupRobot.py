


class mockupRobot():
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
    def __inti(self) :
        mockupRobot.__init__(self)

    def setVitAngD(self, dps) :
        print("setVitAngD =", dps)
        self.set_motor_dps(self.MOTOR_RIGHT, dps)

    def setVitAngG(self, dps) :
        print("setVitAngG =", dps)
        self.set_motor_dps(self.MOTOR_LEFT, dps)

    def setVitAng(self, dps) :
        print("setVitAng =", dps)
        self.set_motor_dps(self.MOTOR_RIGHT + self.MOTOR_LEFT, dps)

    def changeVitAngG(self, quant) :
        print("changeVitAngG +=", quant)
        vit = self.get_motor_position()[0]
        self.set_motor_dps(self.MOTOR_LEFT, vit + quant)

    def changeVitAngD(self, quant) :
        print("changeVitAngD +=", quant)
        vit = self.get_motor_position()[1]
        self.set_motor_dps(self.MOTOR_RIGHT, vit + quant)

    def changeVitAng(self, quant) :
        print("changeVitAng +=", quant)
        vitG = self.get_motor_position()[0]
        vitD = self.get_motor_position()[1]
        self.changeVitAngG(vitG + quant)
        self.changeVitAngD(vitD +quant)
    
    def getVitesseG(self) :
        print("getVitesseG")
        return self.get_motor_position()[0]
    
    def getVitesseD(self) :
        print("getVitesseD")
        return self.get_motor_position()[1]
    
    def getVitesse(self) :
        print("getVitesse")
        vit = self.get_motor_position()[0] + self.get_motor_position()[1]
        return vit/2

    def capteurDistance(self) :
        print("capteurDistance")
        return self.get_distance()
    
# mockupRobot = Adaptateur()
# mockupRobot.setVitAngG(20)