from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt3DCore import *

from PyQt5.Qt3DRender import QCamera, QCameraLens, QRenderAspect , QGeometryRenderer, QGeometry, QBuffer, QAttribute, QTextureLoader
from PyQt5.Qt3DInput import QInputAspect
from PyQt5.Qt3DExtras import QForwardRenderer, QDiffuseSpecularMaterial, QTextureMaterial , Qt3DWindow, QFirstPersonCameraController , QCuboidMesh , QSphereMesh


import math
import struct

from dagger import Mesh, Utils, Consts
from . import RDBTreeWidget
from .objects import lineObject, meshObject

class DaggerMainView(QWidget):
	def __init__(self, rdb, dbg_wire, dbg_normals):
		super(DaggerMainView, self).__init__()
		self.rdb = rdb
		self.dbg_wire = dbg_wire
		self.dbg_normals = dbg_normals
		
		self.view = Qt3DWindow()
		self.container = self.createWindowContainer(self.view)

		vboxlayout = QHBoxLayout()
		self.treeView = RDBTreeWidget.RDBTreeWidget(self, rdb)
		self.treeView.setFixedWidth(300)
		vboxlayout.addWidget(self.treeView)
		
		vboxlayout.addWidget(self.container)
		self.setLayout(vboxlayout)
		
		self.scene = QEntity()
		self.createScene()

		# Camera.
		self.initialiseCamera(self.view)
		
		self.view.defaultFrameGraph().setClearColor(QColor(50,50,50))
		self.view.setRootEntity(self.scene)
		
	def flushRendering(self):
		new = QEntity()
		self.view.setRootEntity(new)
		camController = QFirstPersonCameraController(new)
		
		self.scene = new
		self.createScene()
		
		
		camController.setLinearSpeed(500.0)
		camController.setLookSpeed(180.0)
		camController.setCamera(self.camera)
		
	def initialiseCamera(self, view):
		# Camera.
		self.camera = view.camera()
		self.camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000000.0)
		self.camera.setPosition(QVector3D(100,100,100))
		self.camera.setViewCenter(QVector3D(0.0, 0.0, 0.0))

		# For camera controls.
		camController = QFirstPersonCameraController(self.scene)
		camController.setLinearSpeed(500.0)
		camController.setLookSpeed(300.0)
		camController.setCamera(self.camera)
	
	def findObjByID(self, id):
		for row in self.rdb["objRoot"]:
			for col in row:
				if col == None:
					continue
				for obj in col:
					if obj["id"] == id:
						return obj
		return None
	
	def getMarker(self, x=20, y=20):
		obj = QCuboidMesh()
		obj.setXExtent(x)
		obj.setYExtent(y)
		obj.setZExtent(0)
		return obj
		
	def createScene(self):
		for row in self.rdb["objRoot"]:
			for col in row:
				if col == None:
					continue
				for obj in col:
					pos = obj["position"]
					node = QEntity(self.scene)
					nodeTransform = QTransform()
					nodeTransform.setTranslation(QVector3D(pos["X"], -pos["Y"], pos["Z"]))
					if obj["type"]== Consts.MODEL_TYPE:
						#model objects
						try:
							model = self.rdb["modelsRef"][obj["data"]["modelID"]]
							modelID = int(model['type']+model['id'])
							
							
							rot = obj["data"]["rotation"]
							nodeTransform.setRotationX( (rot["X"]/512)*90)
							nodeTransform.setRotationY( -(rot["Y"]/512)*90)
							nodeTransform.setRotationZ( (rot["Z"]/512)*90)
							
							node.addComponent(meshObject.meshObject(modelID))
							material = QDiffuseSpecularMaterial(self.scene )
							if int(model['type']) == Consts.MODEL_TYPE_DOOR: #door
								#door are green
								material.setDiffuse(QColor(0,240,0, 255))
								material.setAmbient(QColor(0,240,0, 255))
							elif "action" in obj["data"]:
								#actionables are red
								material.setDiffuse(QColor(240,0,0, 255))
								material.setAmbient(QColor(240,0,0, 255))
							else:
								#everything else is light grey
								material.setDiffuse(QColor(240,240,240, 255))
								material.setAmbient(QColor(240,240,240, 255))
								
							if self.dbg_wire :
								#draw wireframes
								wireNode = QEntity(self.scene )
								nodeTransform2 = QTransform()
								nodeTransform2.setMatrix(nodeTransform.matrix())
								wireNode.addComponent(nodeTransform2)	
								material2 = QDiffuseSpecularMaterial(self.scene )
								
								if self.treeView.highlightedID == obj['id']:
									material2.setAmbient(QColor(255,0,0, 255))
									material2.setDiffuse(QColor(255,0,0, 255))
								else:
									material2.setAmbient(QColor(0,0,0, 255))
									material2.setDiffuse(QColor(0,0,0, 255))
								wireNode.addComponent(material2)	
								wireNode.addComponent(meshObject.meshWireframe(modelID))	
							if self.dbg_normals :
								meshObject.addMeshNormals(self.scene, modelID, nodeTransform)
							
						except Exception as e:
							import traceback
							print(traceback.format_exc())
							continue
					elif obj['type'] == Consts.LIGHT_TYPE:
						# light marker
						mesh = QSphereMesh()
						mesh.setRadius(10)
						node.addComponent(mesh)		
						material = QDiffuseSpecularMaterial(self.scene )
						material.setDiffuse(QColor(0,0,240, 255))
						material.setAmbient(QColor(0,0,240, 255))
					else:
						#skip billboard painting
						continue
					
					node.addComponent(nodeTransform)		
					node.addComponent(material)				
					
		#bilboard should be rendered after solids to avoid alpha blending oddities
		for row in self.rdb["objRoot"]:
			for col in row:
				if col == None:
					continue
				for obj in col:
					pos = obj["position"]
					node = QEntity(self.scene )
					nodeTransform = QTransform()
					nodeTransform.setTranslation(QVector3D(pos["X"], -pos["Y"], pos["Z"]))
					if obj['type'] == 3:
						# flat marker
						with open('media/textures/%d/%d-0.PNG'%(obj['data']['findex'], obj['data']['type']), 'rb') as img:
							img.seek(0x10)
							x, y = struct.unpack('>ii', img.read(8))
							mesh = self.getMarker(x,y)
							
							material = QTextureMaterial(self.scene )
							texture = QTextureLoader(mesh)
							texture.setSource(QUrl().fromLocalFile('media/textures/%d/%d-0.PNG'%(obj['data']['findex'], obj['data']['type'])))
							material.setTexture(texture)
							# material.setAlphaBlendingEnabled(True)
					else:
						continue
					node.addComponent(nodeTransform)		
					node.addComponent(material)	
					node.addComponent(mesh)		

		return 
