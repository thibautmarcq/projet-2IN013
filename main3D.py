from src.interface3D import menu3D

RUNNING = True
while RUNNING:
    print("0 - Quit (termine la simulation et arrête le programme)")
    print("1 - Lance une interface 3D ")
    print("2 - Afficher les infos de la simulation")

    cmd = input("Veuillez choisir une action:\n")
    if cmd == "0":
        RUNNING = False
    else:
        menu3D(cmd)