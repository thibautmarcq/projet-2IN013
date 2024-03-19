import math

# ------------------------------  CONSTANTES DE TEMPS  ------------------------------
TIC_SIMULATION = 1/2000
TIC_CONTROLEUR = 1/(2**30)
TIC_INTERFACE = 1000/60


# --------------------  CONSTANTES POUR LE MOCKUP DU ROBOT REEL  --------------------

WHEEL_BASE_WIDTH         = 117  # distance (mm) de la roue gauche a la roue droite.
WHEEL_DIAMETER           = 66.5 #  diametre de la roue (mm)
WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi # perimetre du cercle de rotation (mm)
WHEEL_CIRCUMFERENCE      = WHEEL_DIAMETER   * math.pi # perimetre de la roue (mm)


# -----------------------------  CONSTANTES DE VITESSE  -----------------------------
VIT_ANG_AVAN = 5
VIT_ANG_TOUR = 1