import struct
import json

import dagger.Utils

class Action:
	def __init__(self, f):
		self.Parse(f)
	
	def Parse(self, f):
		self.axis, self.duration, self.mvtQuantity, target, self.type = struct.unpack('<BHHiB', f.read(0xA))
		if target > 0:
			self.target = target
		return 
		
	def Dump(self):
		print('\t\tAction')
		print('\t\t\t axis %x'%self.axis)
		print('\t\t\t duration %x'%self.duration)
		print('\t\t\t mvtQuantity %x'%self.mvtQuantity)
		print('\t\t\t target %x'%self.target)
		print('\t\t\t type %x'%self.type)
		

		
		
class Model:
	def __init__(self, f, base):
		self.base = base
		self.Parse(f)
	
	def Parse(self, f):
		self.rotation = Utils.Point(f)
		
		self.modelID, self.fieldE, self.field10, self.field12, action = struct.unpack('<3HBi', f.read(11))
		
		if action > 0:
			pos = f.tell()
			f.seek(self.base+action)
			self.action = Action(f)
			f.seek(pos)
			
		del(self.base)
		
	def Dump(self):
		print('\tModel')
		self.rotation.Dump()
		print('\t\tmodel : %x'%self.modelID)
		print('\t\tfieldE %x'%self.fieldE)
		print('\t\tfield10 %x'%self.field10)
		print('\t\tfield12 %x'%self.field12)
		if hasattr(obj, 'action'):
			self.action.Dump()
		
class Light:
	def __init__(self, f):
		self.Parse(f)
	
	def Parse(self, f):
		self.field0, self.field2, self.field4, self.field8 = struct.unpack('2HIH', f.read(10))
		return 
		
	def Dump(self):
		print('\tLight')
		print('\t\t%x'%self.field0)
		print('\t\t%x'%self.field2)
		print('\t\t%x'%self.field4)
		print('\t\t%x'%self.field8)
		
class Flat:
	def __init__(self, f):
		self.Parse(f)
		
	def Parse(self, f):
		self.texture, self.field2, self.field4, self.field6, self.fieldA = struct.unpack('<HHHIB', f.read(11))
		
		self.findex = self.texture >> 7
		self.type = self.texture & 0x1F
	
	def Dump(self):
		print('\tFlat')
		print('\t\t texture %x (%d:%d)'%(self.texture, self.findex, self.type))
		print('\t\t field2 %x'%self.field2)
		print('\t\t field4 %x'%self.field4)
		print('\t\t field6 %x'%self.field6)
		print('\t\t fieldA %x'%self.fieldA)
		print('\t\t fieldA %x'%self.fieldA)
		
class BSARDBObject:
	def __init__(self, base):
		self.base = base
		
	def Parse(self, f):
		self.id = f.tell() - self.base 
		next, prev =  struct.unpack('<ii', f.read(8))
		self.position = Utils.Point(f)
		self.type, self.data = struct.unpack('<BI', f.read(5))
		
		
		if self.type == 1:
			self.data = Model(f, self.base)
		elif self.type == 2:
			self.data = Light(f)
		elif self.type == 3:
			self.data = Flat(f)
		else:
			print('ERR :unknown type %d'%self.type)
	
		if next > 0:
			f.seek(self.base+ next)
			self.next = BSARDBObject(self.base)
			self.next.Parse(f)
				
		del(self.base)
		
	def Dump(self):
		self.position.Dump()
		self.data.Dump()
		# print('')
		
		# if self.next != None:
			# self.next.Dump()

class RDBObjectHeader:
	def __init__(self, f):
		self.Parse(f)
	
	def Parse(self, f):
		self.offest, self.field4, self.field8, self.fieldC, self.size, field14, self.field34, field38 = struct.unpack('<5I32s4s456s', f.read(0x200))	
		return 
		
	def Dump(self):
		print('ObjectHeader')
		print('\t offset  %08x'%self.offest)
		print('\t field4  %08x'%self.field4)
		print('\t field8  %08x'%self.field8)
		print('\t fieldC  %08x'%self.fieldC)
		print('\t size    %08x'%self.size)
		print('\t field34 %s'%self.field34)
		
		
class BSARecordDungeonBlock:
	def __init__(self, f):
		self.base = f.tell()
		self.Parse(f)
		
	def Parse(self, f):
		self.h_field0, self.width, self.height, self.objRootOffset, self.h_field10 = struct.unpack('<5I', f.read(0x14))
		
		self.modelsRef = []
		for i in range(750):
			type = f.read(3)
			id = f.read(2)
			descr = f.read(3)
			if type != '\xFF\xFF\xFF':
				self.modelsRef.append( {"type":type, "id":id, "descr":descr})
				
		self.modelData = []
		for i in range(750):
			d, = struct.unpack('<I', f.read(4))
			if d != 0:
				self.modelData.append(d)
				
		self.objectHeader = RDBObjectHeader(f)
		
		
		self.objRoot = []
		#FALL.exe only iterate over the first 2*2 matrix
		for x in range(2):
			tmp = []
			for y in range(2):
				off, = struct.unpack('I', f.read(4))
				if off  & 0xFF000000 == 0:
					curr = f.tell()
					f.seek(self.base+off)
					obj = BSARDBObject(self.base)
					obj.Parse(f)
					
					arr = [obj]
					while hasattr(obj, 'next'):
						old = obj
						obj = obj.next
						del(old.next)
						arr.append(obj)
					
					tmp.append(arr)
					f.seek(curr)
				else:
					tmp.append(None)
			#skip rest the line
			f.seek(4*(self.width-2), 1)
			self.objRoot.append(tmp)
		del(self.base)		
			
	
	def Dump(self):
		return json.dumps(self,ensure_ascii=False, indent=1, default=lambda x: x.__dict__)
		# print('Header:')
		# print('\t field0 : %08x'%self.h_field0)
		# print('\t width  : %08x'%self.width)
		# print('\t height : %08x'%self.height)
		# print('\t objOff : %08x'%self.objRootOffset)
		# print('\t field10: %08x'%self.h_field10)
		
		# print('ModelsRef')
		# for m in self.modelsRef:
			# print('\t %s/%s/%s'%( m['name'], m['unk'], m['descr']))
			
		# print('ModelsData')
		# for d in self.modelData:
			# print('\t %08x'%(d))
			
		
		
		# for x in range(self.height):
			# for y in range(self.width):
				# if self.objRoot[x][y] != None:
					# print('Object list : %d-%d'%(x,y))
					# self.objRoot[x][y].Dump()
			
		
class BSARecordDescriptor:
	def __init__(self, f, type):
		self.type = type
		self.Parse(f)
		
	def Parse(self, f):
		if self.type == 0x100:
			self.name, self.flags, self.size = struct.unpack('<12sHI', f.read(0x12))
			self.name = self.name.rstrip('\x00')
		else:
			self.id, id_h, self.flags, self.size = struct.unpack('<HBBI', f.read(8))
			self.id += id_h*0x10000
			
	def Dump(self):
		if self.type == 0x100:
			print('\t %s'%self.name)
		else:
			print('\t %d'%self.id)
		print('\t\t flags %04x'%self.flags)
		print('\t\t size  %x'%self.size)
		

class BSA:
	def Parse(self, f):
		self.recordCount, self.flags = struct.unpack('HH', f.read(4))
		self.descrs = []
		
		if self.flags == 0x100:
			f.seek(-self.recordCount* 0x12, 2)
		else:
			f.seek(-self.recordCount * 8, 2)
			
		for i in range(self.recordCount):
			self.descrs.append(BSARecordDescriptor(f, self.flags))
			
		f.seek(4)
		for d in self.descrs:
			if hasattr(d, "name"):
				if d.name[-3:] == 'RMB':
					d.record = f.read(d.size)
				elif d.name[-3:] == 'RDB':
					pos = f.tell()
					print(d.name)
					print('%x'%pos)
					d.record = BSARecordDungeonBlock(f)
					o = open('out/RDB/'+d.name, 'wb')
					o.write(d.record.Dump())
					o.close()
					f.seek(pos+d.size)
				elif d.name[-3:] == 'RDI':
					d.record = f.read(d.size)
				else:
					d.record = f.read(d.size)
			else:
				d.record = f.read(d.size)
			
				
		
	def Dump(self):
		# print()
		# print(json.dumps(self, default=lambda x: x.__dict__))
		print('Header \n'\
			  '\t RecordCount : %d\n'\
			  '\t Flags : %04x '%(self.recordCount, self.flags))
		print('Records:')
		for d in self.descrs:
			d.Dump()
			