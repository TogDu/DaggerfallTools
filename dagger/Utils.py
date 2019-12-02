import struct
import math

class Point:
	def __init__(self, f):
		self.Parse(f)
		
	def Parse(self, f):
		self.X, self.Y, self.Z = struct.unpack('3i', f.read(12))
		return 
		
	def Dump(self):
		print('Point')
		print('\t X : %x'%self.X)
		print('\t Y : %x'%self.Y)
		print('\t Z : %x'%self.Z)
		
class Vector:
	def __init__(self, f=None):
		if f:
			self.X, self.Y, self.Z = struct.unpack('3i', f.read(12))
			self.normalize()
		else:
			self.X = 0
			self.Y = 0
			self.Z = 0
	
		
	def add(self, v):
		self.X += v.X
		self.Y += v.Y
		self.Z += v.Z
		
	def normalize(self):
		norm = math.sqrt(self.X*self.X +self.Y*self.Y + self.Z*self.Z)
		if norm != 0:
			self.X = self.X/norm
			self.Y = self.Y/norm
			self.Z = self.Z/norm
		