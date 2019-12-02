# NO_UNITTEST
# This code is in the Public Domain
# -----------------------------------------------------------------------------
# This source file is part of Python-Ogre
# For the latest info, see http://python-ogre.org/
#
# It is likely based on original code from OGRE
# For the latest info, see http://www.ogre3d.org/
#
# You may use this sample code for anything you like, it is not covered by the
# LGPL.
# -----------------------------------------------------------------------------
import sys

import time


import ogre.renderer.OGRE as ogre 
import ogre.io.OIS as OIS
import ogre.gui.CEGUI as CEGUI
import math

from dagger import Mesh
import json


class LocalListener ( ogre.FrameListener, OIS.MouseListener, OIS.KeyListener ):
    def __init__ (self, win, cam, sm, app):
		ogre.FrameListener.__init__(self)
		OIS.KeyListener.__init__(self)
		OIS.MouseListener.__init__(self)
		self.app = app
		self.sceneManager = sm
		self.mWindow = win
		self.camera=cam
		self.mShutdownRequested = False
		self.mLMBDown=False
		self.mRMBDown=False
		self.mProcessMovement=False
		self.mUpdateMovement=False
		self.mMoveFwd=False
		self.mMoveBck=False
		self.mMoveLeft=False
		self.mMoveRight=False
		self.mLastMousePositionSet=False
		self.mAvgFrameTime = 0.01
		self.mWriteToFile = False
		self.mTranslateVector = ogre.Vector3().ZERO 
		self.mQuit = False
		self.bReload = False
		self.mSkipCount = 0
		self.mUpdateFreq=10
		self.mRotX = 0 
		self.mRotY = 0 

		windowHnd = self.mWindow.getCustomAttributeInt("WINDOW")
		self.mInputManager = OIS.createPythonInputSystem([("WINDOW",str(windowHnd))])
		
		##Create all devices (We only catch joystick exceptions here, as, most people have Key/Mouse)
		self.Keyboard = self.mInputManager.createInputObjectKeyboard( OIS.OISKeyboard, True )
		self.Mouse = self.mInputManager.createInputObjectMouse( OIS.OISMouse, True )

		# width, height, depth, left, top = self.mWindow.getMetrics()

		##Set Mouse Region.. if window resizes, we should alter this to reflect as well
		# ms = self.Mouse.getMouseState() 
		# ms.width = width 
# #         ms.height = height 

		self.Mouse.setEventCallback(self) 
		self.Keyboard.setEventCallback(self) 
 

		self.mMoveSpeed = 400.0 

		
##--------------------------------------------------------------------------
    def frameStarted( self, evt):
		# print('frame started')
		self.Mouse.capture() 
		self.Keyboard.capture() 
		if( self.mWindow.isActive() == False ):
			return False 

		if (self.mQuit):
			return False 
		else:
			if self.bReload:
				self.app.s_root.removeAndDestroyAllChildren()
				self.app._build_scene()
				self.bReload = False
				
			self.mSkipCount+=1 
			if (self.mSkipCount >= self.mUpdateFreq):
				self.mSkipCount = 0 
		# # #                 self.updateStats() 
			## update movement process
			if(self.mProcessMovement or self.mUpdateMovement):
				if self.mMoveLeft:
					self.mTranslateVector.x += self.mAvgFrameTime * -self.mMoveSpeed
				if self.mMoveRight:
					self.mTranslateVector.x += self.mAvgFrameTime * self.mMoveSpeed
				if self.mMoveFwd:
					self.mTranslateVector.z += self.mAvgFrameTime * -self.mMoveSpeed
				if self.mMoveBck: 
					self.mTranslateVector.z += self.mAvgFrameTime * self.mMoveSpeed 

				self.camera.yaw(ogre.Degree(self.mRotX)) 
				self.camera.pitch(ogre.Degree(self.mRotY)) 
				self.camera.moveRelative(self.mTranslateVector) 

				self.mUpdateMovement = False 
				self.mRotX = 0 
				self.mRotY = 0 
				self.mTranslateVector = ogre.Vector3().ZERO 

			if(self.mWriteToFile):
				self.mNumScreenShots +=1
				self.mWindow.writeContentsToFile("frame_" +
					str(self.mNumScreenShots) + ".png") 
			return True 

    def frameEnded( self, evt):
        if (self.mShutdownRequested):
            return False 
        else:
            return True


##--------------------------------------------------------------------------
    def mouseMoved (self, e):
        self.handleMouseMove(e) 
        # CEGUI.System.getSingleton().injectMouseWheelChange(e.get_state().Z.rel) 
        return True 


##--------------------------------------------------------------------------
    def mousePressed ( self, e, _id):
		self.handleMouseButtonDown(_id)
		return True 


##--------------------------------------------------------------------------
    def mouseReleased ( self,e, _id):
		self.handleMouseButtonUp(_id)
		return True 


##--------------------------------------------------------------------------
    def keyPressed ( self, e):
		# print('key pressed %d'%e.key)
		## give 'quitting' priority
		if (e.key == OIS.KC_ESCAPE):
			self.mQuit = True 
			return False 
			
		self.CheckMovementKeys( e.key , True) 
		
		return True 


##--------------------------------------------------------------------------
    def keyReleased ( self, e):
		self.CheckMovementKeys( e.key , False) 
		return True 

##--------------------------------------------------------------------------
    def handleMouseMove( self,  e):
		s = e.get_state()
		if( self.mLMBDown and not self.mRMBDown):
			## rotate camera
			# print('test mouse moved')
			self.mRotX += -s.X.rel * self.mAvgFrameTime * self.mMoveSpeed/10
			self.mRotY += -s.Y.rel * self.mAvgFrameTime * self.mMoveSpeed/10
			# CEGUI.MouseCursor.getSingleton().setPosition( self.mLastMousePosition ) 
			self.mUpdateMovement = True 
		else:
			if( self.mRMBDown and not self.mLMBDown):
				## translate camera
				self.mTranslateVector.x +=  s.X.rel * self.mAvgFrameTime * self.mMoveSpeed
				self.mTranslateVector.y += -s.Y.rel * self.mAvgFrameTime * self.mMoveSpeed 
				##self.mTranslateVector.z = 0 
				# CEGUI.MouseCursor.getSingleton().setPosition( self.mLastMousePosition ) 
				self.mUpdateMovement = True 
			else:
				if( self.mRMBDown and self.mLMBDown):
					self.mTranslateVector.z += (s.X.rel + s.Y.rel) * self.mAvgFrameTime * self.mMoveSpeed 
					# CEGUI.MouseCursor.getSingleton().setPosition( self.mLastMousePosition ) 
					self.mUpdateMovement = True 

		return True 

##--------------------------------------------------------------------------
    def handleMouseButtonUp( self, e):
		##Window* wndw = (( WindowEventArgs&)e).window 
		if e == CEGUI.LeftButton:
			self.mLMBDown = False 

		elif e == CEGUI.RightButton:
			self.mRMBDown = False 
		if( not self.mLMBDown and not self.mRMBDown ):
			# CEGUI.MouseCursor.getSingleton().show() 
			if self.mLastMousePositionSet:
				# CEGUI.MouseCursor.getSingleton().setPosition( self.mLastMousePosition ) 
				self.mLastMousePositionSet = False 
			# self.rootGuiPanel.releaseInput() 

		return True 

##--------------------------------------------------------------------------
    def handleMouseButtonDown( self, e):
		# print(e)
		##Window* wndw = (( WindowEventArgs&)e).window 
		if( e == CEGUI.LeftButton ):
			self.mLMBDown = True 

		if( e == CEGUI.RightButton ):
			self.mRMBDown = True 

		if( self.mLMBDown or self.mRMBDown ):
			# CEGUI.MouseCursor.getSingleton().hide() 
			if (not self.mLastMousePositionSet):
				# self.mLastMousePosition = CEGUI.MouseCursor.getSingleton().getPosition() 
				self.mLastMousePositionSet = True 
			# self.rootGuiPanel.captureInput() 

		return True 


##--------------------------------------------------------------------------
    def handleMouseWheelEvent( self, e):
        self.mTranslateVector.z += e.wheelChange * -5.0 
        self.mUpdateMovement = True 
        return True 

##--------------------------------------------------------------------------
    def CheckMovementKeys( self, scancode, state ):
		if  scancode== OIS.KC_A:
			self.mMoveLeft = state 
		elif scancode == OIS.KC_D:
				self.mMoveRight = state 
		elif scancode == OIS.KC_S:
				self.mMoveBck = state
		elif scancode == OIS.KC_W:
				self.mMoveFwd = state 	
		elif scancode == OIS.KC_R:
				self.bReload = True
		self.mProcessMovement = self.mMoveLeft or self.mMoveRight or self.mMoveFwd or self.mMoveBck 

		
	
class OGREMain(ogre.Root):
	def __init__(self, plugins_path='../plugins.cfg',resource_path='../resources.cfg'):
		ogre.Root.__init__(self, plugins_path)
		self.plugins_path = plugins_path
		# self.resource_path = resource_path
		self.sm = None #: scene manager
		self.s_root = None #: root scene node
		
		# self._load_resources(self.resource_path)
		self._choose_render_engine()
		  
		self.initialise(False)
		self.initialisePlugins()

		self.window = self.createRenderWindow("daggertool", 800, 600, False)
		
		self.sm = self.createSceneManager("TerrainSceneManager" ) #ogre.ST_GENERIC)
		self.sm.setShadowTechnique(ogre.SHADOWTYPE_STENCIL_ADDITIVE)
		self.sm.setAmbientLight((0.4, 0.4, 0.4)) 

		self.light = self.sm.createLight('light1')
		self.light.setType(ogre.Light.LT_DIRECTIONAL) 
		
		self.light.setDiffuseColour(1, 1, 1) 
		self.light.setSpecularColour(1, 1, 1)
		self.light.setCastShadows =True
		

		self.camera = self.sm.createCamera("camera")
	
		self.camera.setPosition(100,100,100)
		
		self.camera.lookAt(ogre.Vector3(40, -80, 50))
		self.camera.setNearClipDistance(1)
		self.viewport = self.window.addViewport(self.camera)
		self.viewport.setBackgroundColour(ogre.ColourValue(0.1, 0.1, 0.1))

		self._build_scene()
		self.createFrameListener()
	
	def loadMesh(self, id):
		with open('out/models/%s.3d'%id, 'rb') as f:
			m = Mesh.Mesh()
			m.Parse(f)
			m.CalculatePointsNormal()
			
			obj = self.sm.createManualObject()
			obj.begin('cubemat')
			
			for i in range(m.header.pointCount):
				p = m.points[i]
				n = m.pointNormals[i]
				obj.position(p.X/0x100, -p.Y/0x100, p.Z/0x100)
				obj.normal(n.X, -n.Y, n.Z)
				
			for i in range(m.header.planeCount):
				p = m.planes[i]
				n = m.normals[i]
				if p.pointCount == 4:
					obj.quad(p.points[3].id, p.points[2].id, p.points[1].id, p.points[0].id)
					# obj.quad(p.points[0].id, p.points[1].id, p.points[2].id, p.points[3].id)
				elif p.pointCount == 3:
					obj.triangle(p.points[2].id, p.points[1].id, p.points[0].id)
					# obj.triangle(p.points[0].id, p.points[1].id, p.points[2].id)
				else:
					
					# for i in range(p.pointCount):
						# print("%f %f %f"%(m.points[p.points[-i].id].X, m.points[p.points[-i].id].Y, m.points[p.points[-i].id].Z))
					obj.quad(p.points[3].id, p.points[2].id, p.points[1].id, p.points[0].id)
					# obj.quad(p.points[0].id, p.points[1].id, p.points[2].id, p.points[3].id)
					if p.pointCount == 5:
						obj.triangle(p.points[4].id, p.points[3].id, p.points[0].id)
						# obj.triangle(p.points[0].id, p.points[3].id, p.points[4].id)
					else:
						obj.quad(p.points[5].id, p.points[4].id, p.points[3].id, p.points[0].id)
						# obj.quad(p.points[0].id, p.points[3].id, p.points[4].id, p.points[5].id)
						for k in range(5, p.pointCount-1):
							obj.triangle(p.points[k+1].id, p.points[k].id, p.points[0].id)
						
						
				
			obj.end()
			return obj
						
	def _choose_render_engine(self):
		rend_list = self.getAvailableRenderers()
		for ren in rend_list:
			print ren.getName()
			cap = ren.getCapabilities()
			if cap:
				print "MaxPointSize:", cap.getMaxPointSize()
				print "Stencil stuff:", cap.getStencilBufferBitDepth()
				opts = ren.getConfigOptions()
				print "Opts:", opts
				print "Opts keys:",opts.keys()
				for i in opts:
					print "Key:",i.key
					print i.value.currentValue
					print i.value.name
					print i.value.immutable
					for v in i.value.possibleValues:
						print "Posible Value", v
					
				print dir(opts)
				print "Opts", opts['Video Mode']
				print"Viewo Mode:",  ren.getConfigOptions()['Video Mode']
		self.setRenderSystem(rend_list[-1])

	def _build_scene(self):
		self.s_root = self.sm.getRootSceneNode()
		
		lnode = self.s_root.createChildSceneNode()
		lnode.attachObject(self.light)
		lnode.setDirection(-1,-1,-1) 
		
		with open(sys.argv[1]) as f:
			rdb = json.loads(f.read())
			for row in rdb["objRoot"]:
				for col in row:
					if col == None:
						continue
					for obj in col:
						if obj["type"]==1:
							try:
								model = rdb["modelsRef"][obj["data"]["modelID"]]
								pos = obj["position"]
								rot = obj["data"]["rotation"]
								print(model)
								id = int(model['type']+model['id'])
								node = self.s_root.createChildSceneNode()
								# print("p : %f %f %f"%(pos["X"], -pos["Y"], pos["Z"]))
								# print("r : %f %f %f"%(rot["X"], -rot["Y"], rot["Z"]))
								
								node.setPosition(pos["X"], -pos["Y"], pos["Z"])
								node.pitch( math.radians((rot["X"]/512)*90))
								node.yaw( -math.radians((rot["Y"]/512)*90))
								node.roll( math.radians((rot["Z"]/512)*90))
								
								node.attachObject(self.loadMesh(id))
							except Exception as e:
								print('[ERR] not drawn : %s'%str(e))
								# print(obj)
								continue
				

	def createFrameListener(self):
		self.frameListener = LocalListener(self.window, self.camera, self.sm, self)  
		self.addFrameListener(self.frameListener) 


def main():
    import os
    if os.name == 'nt':
        root = OGREMain(plugins_path='plugins.cfg.nt')
    else:
        root = OGREMain(plugins_path='plugins.cfg.linux')
    weu = ogre.WindowEventUtilities()
    while not root.window.isClosed():
        weu.messagePump()
        if root.window.isActive():
			# all eyes are on us, render away
			if root.renderOneFrame() == False: 
				break
			time.sleep(.01)
        else:
            # we got minimized or de-focused, so slow it down and stop
            # rendering until we get focus back
            time.sleep(1)
    root.shutdown()
    sys.exit(0)

if __name__ == "__main__":
   main()
