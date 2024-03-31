# pip install panda3d==1.10.14

from src.Robot.robot import Robot
from src.constantes import LONGUEUR_ROBOT, LARGEUR_ROBOT, TAILLE_ROUE, DICO_COULEURS

from direct.showbase.ShowBase import ShowBase
from direct.task import Task 
from panda3d.core import Point3, load_prc_file, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexWriter, Vec3, GeomNode

from math import *

load_prc_file('config.prc')

class Interface3D(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        
        self.createRobot("moulinex3D", 4, 5, LARGEUR_ROBOT, LONGUEUR_ROBOT, 15, TAILLE_ROUE, "lightblue")
        
        # self.taskMgr.add(self.spinCameraTask, "spinCameraTask")
        self.taskMgr.add(self.updateCameraTask, "updateCameraTask")

    
    def createRobot(self, nom, x, y, width, length, height, rayonRoue, couleur):
        """Crée un robot en 3D (rectangle)
        """
        self.robot = Robot(nom, x, y, width, length, rayonRoue, couleur)
        self.robot.height = height
        format = GeomVertexFormat.getV3()
        vdata = GeomVertexData("rectangle", format, Geom.UHDynamic) # UHDynamic car les sommets vont devoir être bougés quand le robot va bouger
        vertex = GeomVertexWriter(vdata, "vertex")

        # Définition des sommets du robot | leur indice en comm (voir fiche thibo)
        vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)-(self.robot.length/2), 0)  # 0 dèrrière bas gauche
        vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)-(self.robot.length/2), 0)  # 1 derriere bas droit
        vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)+(self.robot.length/2), 0)  # 2 devant bas droit
        vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)+(self.robot.length/2), 0)  # 3 devant bas gauche
        vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)-(self.robot.length/2), self.robot.height)  # 4 derriere haut gauche
        vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)-(self.robot.length/2), self.robot.height)  # 5 derriere haut droit
        vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)+(self.robot.length/2), self.robot.height)  # 6 devant haut droit
        vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)+(self.robot.length/2), self.robot.height)  # 7 devant haut gauche

        # Création de l'objet (composition de triangles)
        rectangle = GeomTriangles(Geom.UHDynamic)

        # Ajout des faces du carré
        # Bottom
        rectangle.addVertices(0, 1, 2)
        rectangle.addVertices(2, 3, 0)
        # Top
        rectangle.addVertices(4, 5, 6)
        rectangle.addVertices(6, 7, 4)
        # Front
        rectangle.addVertices(0, 1, 5)
        rectangle.addVertices(5, 4, 0)
        # Back
        rectangle.addVertices(3, 2, 6)
        rectangle.addVertices(6, 7, 3)
        # Left
        rectangle.addVertices(0, 4, 7)
        rectangle.addVertices(7, 3, 0)
        # Right
        rectangle.addVertices(1, 2, 6)
        rectangle.addVertices(6, 5, 1)
        
        # Créer un objet Geom pour contenir les triangles (=les faces)
        geom = Geom(vdata)
        geom.addPrimitive(rectangle)

        # Créer un nœud pour contenir le Geom
        node = GeomNode("rectangle")
        node.addGeom(geom)

        # Créer un nœud de scène parent pour le nœud de géométrie
        np = self.render.attachNewNode(node) # np est le noeud de l'objet (=un ptr) dans le moteur graphique
        np.setPos(0, 0, 0)  # Déplacer le triangle pour le voir
        
        self.robot.vectcouleur = DICO_COULEURS[self.robot.couleur]
        np.setColor(self.robot.vectcouleur[0], self.robot.vectcouleur[1], self.robot.vectcouleur[2], self.robot.vectcouleur[3]) # RGB + transparence | COULEUR
        np.setTwoSided(True) # pour render toutes les faces
    
    
    
    # Task pour faire rotate la camera
    def spinCameraTask(self, task):
        print(task.time)
        angleDegrees = task.time * 60.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.lookAt(Point3(0, 0, 0))
        return Task.cont
    
    # Task pour suivre le robot
    def updateCameraTask(self, task):
        # Set the camera position relative to the robot's position
        self.camera.setPos(self.robot.x - 150, self.robot.y - 200, 150)
        self.camera.lookAt(Point3(self.robot.x, self.robot.y, 0))
        
        return Task.cont  # Continue the task indefinitely

app = Interface3D()
app.run()