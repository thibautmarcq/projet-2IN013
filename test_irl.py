# Main à lancer sur le robot pour exécuter des stratégies/actions

from logging import DEBUG, basicConfig

from robot2IN013 import Robot2IN013
from src.Controleur import (Controler, StrategieAvancer, StrategieTourner,
                            setStrategieArretMur)
from src.robots.gopigo import Adaptateur_reel

basicConfig(filename='logs.log', 
                    level=DEBUG, 
                    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s', 
                    datefmt='%d/%m/%y %H:%M:%S', 
                    encoding='UTF-8') # niveaux : DEBUG INFO WARNING ERROR CRITICAL

#On crée un controleur
controleur = Controler()
rob = Robot2IN013()
# Ajoute le premier robot
reel = Adaptateur_reel(rob)

def menu() :
    global RUNNING
    print("0 - Quitter")
    print("1 - Avancer")
    print("2 - Avancer jusqu'au mur")
    print("3 - Tourner")
    cmd = int(input("Veuillez choisir une action :\n"))
    if cmd==0:
        RUNNING = False
    elif cmd== 1:
        avancer = StrategieAvancer(reel, 500)
        controleur.lancerStrategie(avancer)
    elif cmd==2:
        mur = setStrategieArretMur(reel, 1500)
        controleur.lancerStrategie(mur)
    elif cmd==3:
        tourner = StrategieTourner(reel, 90)
        controleur.lancerStrategie(tourner)
    else:
        print("Numéro non disponible")

RUNNING = True
while RUNNING:
    menu()