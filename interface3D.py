# pip install panda3d==1.10.14

from src.Robot.robot import Robot
from src.constantes import LONGUEUR_ROBOT, LARGEUR_ROBOT, TAILLE_ROUE, DICO_COULEURS

from direct.showbase.ShowBase import ShowBase
from direct.task import Task 
from panda3d.core import Point3, load_prc_file, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexWriter, Vec3, GeomNode

from math import *

load_prc_file('src/Interface3D/config.prc')

class Interface3D(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.nbRobots = 0
        
        self.createRobot("moulinex3D", 4, 5, LARGEUR_ROBOT, LONGUEUR_ROBOT, 15, TAILLE_ROUE, "lightblue")
        
        # self.taskMgr.add(self.spinCameraTask, "spinCameraTask")
        self.taskMgr.add(self.updateCameraTask, "updateCameraTask")

    
    def createRobot(self, nom, x, y, width, length, height, rayonRoue, couleur):
        """Crée un robot en 3D (rectangle)
        """
        self.robot = Robot(nom, x, y, width, length, rayonRoue, couleur)
        self.robot.height = height
        self.robot.num = self.nbRobots
        self.nbRobots+=1
        
        # toutes les variables sont reliées à un robot, d'où le self.robot
        self.robot.format = GeomVertexFormat.getV3() # type des sommets
        self.robot.vdata = GeomVertexData("rectangle", self.robot.format, Geom.UHDynamic) # UHDynamic car les sommets vont devoir être bougés quand le robot va bouger
        self.robot.vertex = GeomVertexWriter(self.robot.vdata, "vertex")

        # Définition des sommets du robot | leur indice en comm (voir fiche thibo)
        self.robot.vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)-(self.robot.length/2), 0)  # 0 dèrrière bas gauche
        self.robot.vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)-(self.robot.length/2), 0)  # 1 derriere bas droit
        self.robot.vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)+(self.robot.length/2), 0)  # 2 devant bas droit
        self.robot.vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)+(self.robot.length/2), 0)  # 3 devant bas gauche
        self.robot.vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)-(self.robot.length/2), self.robot.height)  # 4 derriere haut gauche
        self.robot.vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)-(self.robot.length/2), self.robot.height)  # 5 derriere haut droit
        self.robot.vertex.addData3f((self.robot.x)+(self.robot.width/2), (self.robot.y)+(self.robot.length/2), self.robot.height)  # 6 devant haut droit
        self.robot.vertex.addData3f((self.robot.x)-(self.robot.width/2), (self.robot.y)+(self.robot.length/2), self.robot.height)  # 7 devant haut gauche

        # Création de l'objet (composition de triangles)
        self.robot.rectangle = GeomTriangles(Geom.UHDynamic)

        # Ajout des faces du carré
        # Bottom
        self.robot.rectangle.addVertices(0, 1, 2)
        self.robot.rectangle.addVertices(2, 3, 0)
        # Top
        self.robot.rectangle.addVertices(4, 5, 6)
        self.robot.rectangle.addVertices(6, 7, 4)
        # Front
        self.robot.rectangle.addVertices(0, 1, 5)
        self.robot.rectangle.addVertices(5, 4, 0)
        # Back
        self.robot.rectangle.addVertices(3, 2, 6)
        self.robot.rectangle.addVertices(6, 7, 3)
        # Left
        self.robot.rectangle.addVertices(0, 4, 7)
        self.robot.rectangle.addVertices(7, 3, 0)
        # Right
        self.robot.rectangle.addVertices(1, 2, 6)
        self.robot.rectangle.addVertices(6, 5, 1)
        
        # Créer un objet Geom (=l'objet du robot) pour contenir les triangles (=les faces)
        self.robot.geom = Geom(self.robot.vdata)
        self.robot.geom.addPrimitive(self.robot.rectangle)

        # Créer un nœud pour contenir le Geom
        self.robot.node = GeomNode("rectangle")
        self.robot.node.addGeom(self.robot.geom)

        # Créer un nœud de scène parent pour le nœud de géométrie
        self.robot.np = self.render.attachNewNode(self.robot.node) # np est le noeud de l'objet (=un ptr) dans le moteur graphique
        self.robot.np.setPos(0, 0, 0)  # Déplacer le triangle pour le voir
        
        self.robot.vectcouleur = DICO_COULEURS[self.robot.couleur]
        self.robot.np.setColor(self.robot.vectcouleur[0], self.robot.vectcouleur[1], self.robot.vectcouleur[2], self.robot.vectcouleur[3]) # RGB + transparence | COULEUR
        self.robot.np.setTwoSided(True) # pour render toutes les faces
    
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