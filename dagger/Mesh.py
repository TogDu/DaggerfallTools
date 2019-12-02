from . import Utils
import struct 

class Header:
	def __init__(self, f):
		self.Parse(f)
		
	def Parse(self, f):
		self.version, self.pointCount, self.planeCount, self.radius, self.field10, self.planeDataOff, self.objDataOff, self.objDataCount, self.field24, self.field28, self.pointListOff, self.normalListOff, self.field38, self.planeListOff = struct.unpack('<4sIIIQIIIIQIIII', f.read(0x40))

			
	def Print(self):
		print('Header')
		print('\t version %s'%self.version)
		print('\t pointCount %d'%self.pointCount)
		print('\t planeCount %d'%self.planeCount)
		print('\t radius %d'%self.radius)
		print('\t field10 %d'%self.field10)
		print('\t planeDataOff %d'%self.planeDataOff)
		print('\t objDataOff %d'%self.objDataOff)
		print('\t objDataCount %d'%self.objDataCount)
		print('\t field24 %d'%self.field24)
		print('\t field28 %d'%self.field28)
		print('\t pointListOff %d'%self.pointListOff)
		print('\t normalListOff %d'%self.normalListOff)
		print('\t field38 %d'%self.field38)
		print('\t planeListOff %d'%self.planeListOff)

class PlanePoint:
	def __init__(self, f,bv25):
		self.bv25 = bv25
		self.Parse(f)
		
		
	def Parse(self, f):
		self.offset, self.u, self.v = struct.unpack('<IHH', f.read(8))
		if self.bv25:
			self.id = int(self.offset/4)
		else:
			self.id = int(self.offset/0xC)
	def Print(self):
		print('PlanePoint')
		print('\t id : %d'%self.id)
		print('\t U : %d'%self.u)
		print('\t V : %d'%self.v)
		
		
class Plane:
	def __init__(self, f, bv25):
		self.bv25 = bv25
		self.Parse(f)
		
		
	def Parse(self, f):
		self.pointCount, self.field1, self.texture, self.field4 = struct.unpack('<BBHI', f.read(8))
		self.points = []
		for i in range(self.pointCount):
			self.points.append(PlanePoint(f, self.bv25))
			
	def Print(self):
		print('Plane')
		print('\t pointCount : %d'%self.pointCount)
		print('\t field1 : %d'%self.field1)
		print('\t texture : %d'%self.texture)
		print('\t field4 : %d'%self.field4)
		
		for i in range(self.pointCount):
			self.points[i].Print()
		
		
class Mesh:		
	def Parse(self, f):
		self.header = Header(f)
		if self.header.version == "v2.5":
			bv25 = True
		else:
			bv25 = False
			
		f.seek(self.header.pointListOff)
		self.points = []
		self.pointNormals = []
		for i in range(self.header.pointCount):
			self.points.append(Utils.Point(f))
			self.pointNormals.append(Utils.Vector())
			
		f.seek(self.header.planeListOff)
		self.planes = []
		for i in range(self.header.planeCount):
			self.planes.append(Plane(f, bv25))
			
		f.seek(self.header.normalListOff)
		self.normals = []
		for i in range(self.header.planeCount):
			self.normals.append(Utils.Vector(f))
		
	def CalculatePointsNormal(self):
		for i in range(self.header.planeCount):
			for p in self.planes[i].points:
				n = self.pointNormals[p.id]
				# self.pointNormals[p.id] = self.normals[i]
				n.add(self.normals[i])
				n.normalize()

			
		
	def Print(self):
		self.header.Print()
		for i in range(self.header.planeCount):
			self.planes[i].Print()