from math import acos, cos, pi, radians, sin, sqrt
import cv2
import numpy as np
import simpleaudio as sa

def normaliserVecteur(u) :
    """ Prend en argument un vecteur et un vecteur équivalent normalisé (pour avoir une longueur de 1)
        :param u: le vecteur que l'on souhaite normaliser
        :returns: un vecteur correspondant au vecteur donné en argument, mais normalisé à 1 de longueur
    """
    x, y = u
    long = sqrt(x**2 + y**2) # la longueur du vecteur tel quel
    if (long==0): # Cas où le vecteur à normaliser est nul
        return (0,0)
    return (x/long, y/long) # on divise chacune des coordonnées par la longueur du vecteur, de cette manière le vecteur sera de norme 1


def norme(u) :    
    """ Calcule la norme d'un vecteur
        :param u: le vecteur dont on veut calculer la norme
        :returns: la norme du vecteur passé en argument
    """
    x, y = u
    return sqrt(x*x + y*y)


def prodScalaire(u, v) :
    """ Calcule le produit scalaire de deux vecteurs
        :param u: premier vecteur qu'on utilise pour calculer le produit scalaire
        :param v: deuxième vecteur qu'on utilise pour calculer le produit scalaire
        :returns: le produit scalaire des vecteurs u et v
    """
    x1, y1 = u
    x2, y2 = v
    return x1*x2 + y1*y2


def getAngleFromVect(u, v) :
    """ Calcule l'angle entre deux vecteurs
        :param u: le premier des deux vecteurs entre lesquels on veut calculer l'angle
        :param v: le deuxième des deux vecteurs entre lesquels on veut calculer l'angle
        :returns: l'angle entre les vecteurs u et v 
    """
    # On s'assure que la valeur qu'on va donner en argument de la fonction acos est bien comprise entre -1 et 1
    cos_theta = min(1, max(-1, prodScalaire(u, v) / (norme(u) * norme(v))))
    return acos(cos_theta) * 180 / pi # On multiplie le résultat par 180/pi pour avoir une valeur de retour en degré et non en radians


def getDistanceFromPts(p1, p2) :
    """ Calcule la distance entre deux points p1 et p2
        :param p1: premier point 
        :param p2: deuxième point
        :returns: retourne la distance entre les deux points passés en argument
    """
    x1, y1 = p1
    x2, y2 = p2
    return sqrt((x2-x1)**2 + (y2-y1)**2)


def getVectFromAngle(vect, alpha):
    """ Calcule le vecteur obtenu avec un angle depuis un vecteur de départ
        :param vect: l'angle dont on veut calculer le changement
        :alpha: la valeur de rotation souhaitée
        :returns: un vecteur d'angle <alpha>
    """
    a = radians(alpha) # l'angle alpha est en radians
    x, y = vect
    x_prime = cos(a)*x - sin(a)*y
    y_prime = sin(a)*x + cos(a)*y
    return [x_prime, y_prime]


def rotationVecteur(v, angle):
    """ Fonction qui fait une rotation du vecteur2D <v> de <angle>
		:param v: le vecteur de direction de départ
		:param angle: l'angle par lequel on veut tourner le robot
		:returns: le nouveau vecteur directeur
	"""
    x, y = v
    return (x*cos(angle)-y*sin(angle), x*sin(angle)+y*cos(angle))


def contientBalise(image):
    """ Détermine si une image contient la balise
        :param image: l'image où on souhaite détecter la balise
        :returns: True si la balise se trouve dans l'image, False sinon
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    x, y = 0, 0

    for color in ["red", "blue", "green", "yellow"]:
        scope = get_limits(color)
        mask = cv2.inRange(hsv, scope[0], scope[1])
        moments = cv2.moments(mask)
        if moments["m00"] != 0:
            cX = int(moments["m10"] / moments["m00"])
            cY = int(moments["m01"] / moments["m00"])
        else:
            return (False, 0)
        x += cX
        y += cY

    x = int(x/4)
    y = int(y/4)
    return (True, (x-(image.shape[0]/2)))


def get_limits(color):
	""" Donne les nuances max et min de la couleur en paramètre """
	if "blue" == color: 
		lower_limit = np.array([100,84,46])
		upper_limit = np.array([110,255,255])
	elif "red" == color:
		lower_limit = np.array([0,150,100])
		upper_limit = np.array([10,255,255])
	elif "green" == color:
		lower_limit = np.array([59,57,57])
		upper_limit = np.array([70,255,255])
	elif "yellow" == color:
		lower_limit = np.array([20,128,93])
		upper_limit = np.array([39,255,255])
	elif "white" == color:
		lower_limit = np.array([3,26,99])
		upper_limit = np.array([36,71,165])

	return lower_limit, upper_limit


def play_audio_with_volume(filename, volume):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    audio_data = np.frombuffer(wave_obj.audio_data, dtype=np.int16)
    audio_data = (audio_data * volume).astype(np.int16)
    wave_obj = sa.WaveObject(audio_data.tobytes(), wave_obj.num_channels, wave_obj.bytes_per_sample, wave_obj.sample_rate)
    play_obj = wave_obj.play()
    play_obj.wait_done()