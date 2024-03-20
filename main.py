from src.Controleur.controleur import Controler
from src.Controleur.Strategies import *
from src.Robot.mockupRobot import *

#On créer un controleur
controleur = Controler()

# Ajoute le premier robot
reel = Adaptateur()

def menu() :
    print("0 - Quitter")
    print("1 - Tracer un carré")
    print("2 - Avancer vers le mur sans se crasher")
    cmd = input("Veuillez choisir une action parmi celles proposées : \n")
    match cmd :
        case 0:
            pass
        case 1:
            pass
        case 2:
          pass  
        case 3:
            pass