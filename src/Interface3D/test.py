# pip install panda3d==1.10.14

from direct.showbase.ShowBase import ShowBase
from direct.task import Task 
from direct.actor.Actor import Actor # modèles animés
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, load_prc_file, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexWriter, Vec3, GeomNode
import simplepbr
from math import *

load_prc_file('config.prc')

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        
        self.createRobot()
        
        # self.taskMgr.add(self.spinCameraTask, "spinCameraTask")
        self.camera.lookAt(Point3(0, 0, 0))
    
    def createRobot(self):
        """TEMPORAIRE : Crée un cube dans l'interface
        """
        format = GeomVertexFormat.getV3()
        vdata = GeomVertexData("rectangle", format, Geom.UHDynamic) # UHDynamic car les sommets vont devoir être bougés quand le robot va bouger
        vertex = GeomVertexWriter(vdata, "vertex")

        # Définition des sommets du rectangle | leur indice en comm
        vertex.addData3f(0, 0, 0)  # 0
        vertex.addData3f(1, 0, 0)  # 1
        vertex.addData3f(1, 1, 0)  # 2
        vertex.addData3f(0, 1, 0)  # 3
        vertex.addData3f(0, 0, 1)  # 4
        vertex.addData3f(1, 0, 1)  # 5
        vertex.addData3f(1, 1, 1)  # 6
        vertex.addData3f(0, 1, 1)  # 7

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
        np.setColor(1, 0, 0, 1) # RGB + transparence | COULEUR
        np.setTwoSided(True) # pour render toutes les faces
    
    
    
    # Task pour faire rotate la camera
    def spinCameraTask(self, task):
        print(task.time)
        angleDegrees = task.time * 60.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.lookAt(Point3(0, 0, 0))
        return Task.cont

app = MyApp()
app.run()