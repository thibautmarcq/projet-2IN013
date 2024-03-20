# Main à lancer sur le robot pour exécuter des stratégies/actions

from src.Controleur.controleur import Controler
from src.Controleur.Strategies import *
from src.Robot.gopigo import *

#On crée un controleur
controleur = Controler()

# Ajoute le premier robot
reel = Adaptateur()

def menu() :
    global RUNNING
    print("0 - Quitter")
    print("1 - Tracer un carré")
    print("2 - Avancer vers le mur sans se crasher")
    print("3 - Stratégie séquentielle")
    cmd = int(input("Veuillez choisir une action :\n"))
    match cmd :
        case 0:
            RUNNING = False
        case 1:
            long = float(input("Quelle largeur voulez-vous pour le carré ? \n"))
            carre = setStrategieCarre(reel, long)
            controleur.lancerStrategie(carre)
        case 2:
            long = float(input("A quelle distance doit-on s'arrêter du mur ?"))
            mur = setStrategieArretMur(reel, long, None)
            controleur.lancerStrategie(mur)
        case 3:
            pass
        case _:
            print("Numéro non disponible")

RUNNING = True
while RUNNING:
    menu()