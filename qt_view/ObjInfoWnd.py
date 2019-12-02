from PyQt5.QtWidgets import *

from dagger import Consts

class ObjInfoWnd(QWidget):
	def __init__(self, obj, model):
		super(ObjInfoWnd, self).__init__()
		self.layout = QGridLayout()
		
		self.addText('Type', 0, 0)
		if obj['type'] ==  Consts.MODEL_TYPE:
			self.addText('Model', 0, 1)
			self.addText('%s%s (%s)'%(model['type'], model['id'], model['descr']), 0,2)
		elif obj['type'] ==  Consts.LIGHT_TYPE:
			self.addText('Light', 0, 1)
		else:
			self.addText('Bilboard', 0, 1)
			self.addText('%d-%d'%(obj['data']['findex'], obj['data']['type']), 0,2)
			
		self.addText('Position', 1, 0)
		self.addText('%d'%obj['position']['X'], 1, 1)
		self.addText('%d'%obj['position']['Y'], 1, 2)
		self.addText('%d'%obj['position']['Z'], 1, 3)
		
		if obj['type'] ==  Consts.MODEL_TYPE:
			self.addText('Rotation', 2, 0)
			self.addText('%d'%obj['data']['rotation']['X'], 2, 1)
			self.addText('%d'%obj['data']['rotation']['Y'], 2, 2)
			self.addText('%d'%obj['data']['rotation']['Z'], 2, 3)
		elif obj['type'] ==  Consts.LIGHT_TYPE:
			self.addText('Data', 2,0)
			self.addText('%d'%obj['data']['field0'], 2, 1)
			self.addText('%d'%obj['data']['field2'], 2, 2)
			self.addText('%d'%obj['data']['field4'], 2, 3)
			self.addText('%d'%obj['data']['field8'], 2, 4)
		
		if obj['type'] != Consts.LIGHT_TYPE:
			self.addText('Action', 3, 0)
			if 'action' in obj['data']:
				self.addText('type : '+Consts.ACTION_TYPE[obj['data']['action']['type']], 3, 1)
				if 'target' in obj['data']['action']:
					self.addText('target : %d'%obj['data']['action']['target'], 3, 2)
				else:
					self.addText('target : none', 3, 2)
				self.addText('axis : '+ Consts.ACTION_AXIS[obj['data']['action']['field0']], 4, 1)
				self.addText('time : %d'%obj['data']['action']['field1'], 4, 2)
				self.addText('mvt : %d'%obj['data']['action']['field3'], 4, 3)
			else:
				self.addText('none', 3, 1)
				
		self.setLayout(self.layout)
		self.setWindowTitle('obj : %d'%obj['id'])
	
	def addText(self, t, i, j):
		content = QLabel()
		content.setText(t)
		self.layout.addWidget(content, i, j)