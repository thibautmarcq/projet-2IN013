# Main à lancer sur le robot pour exécuter des stratégies/actions

from src.Controleur.controleur import Controler
from src.Controleur.Strategies import *
from Robot.gopigo import *

#On crée un controleur
controleur = Controler()

# Ajoute le premier robot
reel = Adaptateur()

# def menu() :
#     print("0 - Quitter")
#     print("1 - Tracer un carré")
#     print("2 - Avancer vers le mur sans se crasher")
#     cmd = input("Veuillez choisir une action parmi celles proposées : \n")
#     match cmd :
#         case 1:
#             long = float(input("Quelle largeur voulez-vous pour le carré ? \n"))
#             carre = setStrategieCarre(reel, long)
#             controleur.lancerStrategie(carre)
#         case 2:
#           pass  
#         case 3:
#             pass
        
long = float(input("Quelle largeur voulez-vous pour le carré ? \n"))
carre = setStrategieCarre(reel, long)
controleur.lancerStrategie(carre)