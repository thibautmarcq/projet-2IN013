
# ------------------------------  CONSTANTES DE TEMPS  ------------------------------
TIC_SIMULATION = 1/2000
TIC_CONTROLEUR = 1/(2**30)
TIC_ADAPT = 1/(2**30)
TIC_INTERFACE = 1000/60


# -----------------------------  CONSTANTES DE VITESSE  -----------------------------
VIT_ANG_AVAN = 2
VIT_ANG_TOUR = 1

# --------------------------  CONSTANTES DE LA SIMULATION  --------------------------
# L'emplacement des obstacles est prédefini par ces points càd on place des points qui représente l'emplacements et la forme de l'obstacle
LIST_PTS_OBS_TRIANGLE = [(400,400),(450,450),(350,450)]
LIST_PTS_OBS_CARRE = [(300,300),(350,300),(350,350), (300,350)]
LIST_PTS_OBS_COEUR = [(100,140),(170,55),(160,30), (130,30), (100,50), (70,30), (40,30), (30,55)]

TAILLE_ROUE = 20
LONGUEUR_ROBOT = 55
LARGEUR_ROBOT = 30

LONGUEUR_ENV = 550
LARGEUR_ENV = 750
SCALE_ENV_1 = 1

# --------------------------  CONSTANTES DE L'INTERFACE 3D  --------------------------
#Dico pour associer un code RGBA à la couleur str d'un robot
DICO_COULEURS = {
    "red": (1, 0, 0, 1),
    "green": (0, 1, 0, 1),
    "blue": (0, 0, 1, 1),
    "white": (1, 1, 1, 1),
    "black": (0, 0, 0, 1),
    "lightblue": (0.678, 0.847, 0.902, 1)
}