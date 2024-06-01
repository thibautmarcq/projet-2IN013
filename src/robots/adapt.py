import logging
from abc import abstractmethod


class Adaptateur:
    """ Classe abstraite d'adaptateur pour définir les méthodes des adaptateurs """
    
    @abstractmethod
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Initialisation du robot")

    @abstractmethod
    def initialise(self):
        pass
            
    @abstractmethod
    def setVitAngDA(self, dps):
        self.logger.info("setVitAngD = %d", dps)
    
    @abstractmethod
    def setVitAngGA(self, dps) :
        self.logger.info("setVitAngG = %d", dps)
    
    @abstractmethod
    def setVitAngA(self, dps) :
        self.logger.info("setVitAng = %d", dps)

    @abstractmethod
    def tourne(self, gauche, droite) :
        pass
    
    @abstractmethod
    def getDistanceA(self) :
        self.logger.debug("capteurDistance")
    
    @abstractmethod
    def getDistanceParcourue(self) :
        pass
    
    @abstractmethod
    def getAngleParcouru(self) :
        pass

    @abstractmethod
    def get_imageA(self) :
        pass

    @abstractmethod
    def changeCouleur(self, coul) :
        pass

    @abstractmethod
    def playSound(self, sound) :
        pass