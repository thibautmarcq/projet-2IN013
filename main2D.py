from src.Interface.demo import menu

RUNNING = True

while RUNNING:
    print("0 - Quit (termine la simulation et arrête le programme)")
    print("1 - Lance une interface Graphique ")
    print("2 - afficher les infos de la simulation")
    print("3 - faire tracer un carré au robot réel")

    cmd = input("Veuillez choisir une action:\n")
    if cmd == "0":
        RUNNING = False
    else:
        menu(cmd)