from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from . import ObjInfoWnd
from dagger import Consts

class RDBTreeWidget(QTreeWidget):
	def __init__(self, view3D, rdb):
		QTreeWidget.__init__(self)
		self.setColumnCount(3)
		self.setHeaderLabels( [rdb['name'], 'type', 'id'] )
		self.itemDoubleClicked.connect(self.objDoubleClicked)
		self.itemClicked.connect(self.objClicked)
		
		self.rdb = rdb
		self.view3D = view3D
		self.highlightedID = -1
		
		self.populate()
	
	def populate(self):
		meshList =  QTreeWidgetItem(self)
		meshList.setText(0, 'meshs')
		flatList =  QTreeWidgetItem(self)
		flatList.setText(0, 'flats')
		lightList =  QTreeWidgetItem(self)
		lightList.setText(0, 'lights')
		
		meshs = {}
		flats = {}
		for row in self.rdb["objRoot"]:
			for col in row:
				if col == None:
					continue
				for obj in col:
					if obj["type"] == Consts.MODEL_TYPE:
						model = self.rdb["modelsRef"][obj["data"]["modelID"]]				
						if not model['type'] in meshs:
							meshs[model['type']] =  QTreeWidgetItem(meshList)
							meshs[model['type']].setText(0,model['type'])
							
						item =  QTreeWidgetItem(meshs[model['type']])
						item.obj = obj
						item.model = model
						item.setText(0, model['id'])
						item.setText(1, model['descr'])
						item.setText(2, '%d'%obj['id'])
					elif obj["type"] == Consts.LIGHT_TYPE:
						item =  QTreeWidgetItem(lightList)
						item.obj = obj
						item.model = None
						item.setText(0, '%d'%obj['id'])
					elif obj["type"] == Consts.BILLBOARD_TYPE:
						if not obj['data']['findex'] in flats:
							flats[obj['data']['findex']] =  QTreeWidgetItem(flatList)
							flats[obj['data']['findex']].setText(0, '%d'%obj['data']['findex'])
						item =  QTreeWidgetItem(flats[obj['data']['findex']])
						item.obj = obj
						item.model = None
						item.setText(0, '%d'%(obj['data']['type']))
		
	def objDoubleClicked(self, item, column):
		if hasattr(item, 'obj'):
			self.popup = ObjInfoWnd.ObjInfoWnd(item.obj, item.model)
			self.popup.setGeometry(QRect(200, 200, 400, 200))
			self.popup.show()
	
	def objClicked(self, item, column):
		if hasattr(item, 'obj'):
			pos = item.obj['position']
			if self.highlightedID != item.obj['id']:
				self.highlightedID = item.obj['id']
				self.view3D.camera.setPosition(QVector3D(pos['X']+100, -pos['Y']+100, pos['Z']+100))
				self.view3D.camera.setViewCenter(QVector3D(pos['X'], -pos['Y'], pos['Z']))
				self.view3D.camera.setUpVector(QVector3D(0,1,0))
				
				self.view3D.flushRendering()