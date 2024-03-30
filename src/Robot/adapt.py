from abc import ABC, abstractmethod
import logging

class Adaptateur:
    """ Classe abstraite d'adaptateur pour définir les méthodes des adaptateurs """
    
    @abstractmethod
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug("Initialisation du robot")
            
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
    def capteurDistanceA(self) :
        self.logger.debug("capteurDistance")
    
    @abstractmethod
    def distance_parcourue(self) :
        pass
    
    @abstractmethod
    def angle_parcouru(self) :
        pass