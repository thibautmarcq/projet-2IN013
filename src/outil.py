from math import acos, cos, pi, radians, sin, sqrt
import cv2
import numpy as np

def normaliserVecteur(u) :

    """ Prend en argument un vecteur et un vecteur équivalent normalisé (pour avoir une longueur de 1)
        :param vect: le vecteur que l'on souhaite normaliser
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
    return acos(cos_theta) * 180 / pi ## on multiplie le résultat par 180/pi pour avoir une valeur de retour en degré et non en radians

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
    """ Calcule le vecteur obtenu avec un angle
        :param angle: angle du vecteur voulu
        :returns: un vecteur d'angle <angle>
    """
    a = radians(alpha) # angle alpha en radians
    x, y = vect
    x_prime = cos(a)*x - sin(a)*y
    y_prime = sin(a)*x + cos(a)*y
    return [x_prime, y_prime]

def rotationVecteur( v, angle):
    """ Fonction qui fait une rotation du vecteur2D <v> de <angle>
		:param v: le vecteur de direction de départ
		:param angle: l'angle par lequel on veut tourner le robot
		:returns: le nouveau vecteur directeur
	"""
    x, y = v
    return (x*cos(angle)-y*sin(angle), x*sin(angle)+y*cos(angle))

def contientBalise(image):
    """ Fonction qui recherche un certain pattern dans l'image passé en parametre
    :param image : un npArray réprésentant une image
    :returns: (True, décalageEnX) si la balise reconnue dans notre image
    Sinon (False, None)
    """
    print("image :", image)
    # obtenir le npArray du patern à rechercher
    balise = cv2.imread("autre/Photos_balise/template.jpg", cv2.IMREAD_UNCHANGED)
    bal = 1 # compteur de rotation de la balise
    if image is not None :
        while bal <= 4:
            # nous donne un array des % de match
            resultat = cv2.matchTemplate(image, balise, cv2.TM_CCOEFF_NORMED) 
            _, maxVal, _, maxPoint = cv2.minMaxLoc(resultat) # récupère le meilleur match
            # Si un match suffisant est trouvé 
            if maxVal >= 0.93:
                w = balise.shape[1]
                h= balise.shape[0]
                cv2.rectangle(image, maxPoint, (maxPoint[0]+w, maxPoint[1]+h), (0,0,0), 3)
                return (True, (maxPoint[0]+w/2)-image.shape[1]/2)
            
            # Sinon on fait une rotation de notre balise
            # pour rechercher notre balise sous divers rotation ( 90 ° )
            else:
                balise = np.rot90(balise, 1, (0, 1))
                bal+=1
    return (False, None)