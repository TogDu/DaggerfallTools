from PyQt5.QtGui import *
from PyQt5.Qt3DCore import *

from PyQt5.Qt3DRender import QGeometryRenderer, QGeometry, QBuffer, QAttribute
from PyQt5.Qt3DExtras import  QDiffuseSpecularMaterial


import struct

from dagger import Mesh, Utils
from . import lineObject

MODEL_PATH = 'media/models/%s.3d'

def addMeshNormals(scene, id, transform):
	with open('media/models/%s.3d'%id, 'rb') as f:
		m = Mesh.Mesh()
		m.Parse(f)
		m.CalculatePointsNormal()
		
		obj = QGeometryRenderer()
		customGeo = QGeometry(obj)
		verticesBuffer = QBuffer(QBuffer.VertexBuffer, customGeo)
		idxBuffer = QBuffer(QBuffer.IndexBuffer, customGeo)
		
		vertices = b""
		idx = b""
		for i in range(m.header.pointCount):
			node = QEntity(scene)
			material = QDiffuseSpecularMaterial(scene)
			material.setDiffuse(QColor(255,0,0, 255))
			material.setAmbient(QColor(255,0,0, 255))
			
			nodeTransform = QTransform()
			nodeTransform.setMatrix(transform.matrix())
			
			srcPt = m.points[i]
			n = m.pointNormals[i]
			
			dstPt = Utils.Vector()
			dstPt.X = srcPt.X+n.X*0x2000
			dstPt.Y = srcPt.Y+n.Y*0x2000
			dstPt.Z = srcPt.Z+n.Z*0x2000
			
			node.addComponent(nodeTransform)	
			node.addComponent(material)	
			node.addComponent(lineObject.lineObject(srcPt, dstPt))	
				
				
def meshWireframe(id):
	with open(MODEL_PATH%id, 'rb') as f:
		m = Mesh.Mesh()
		m.Parse(f)
		m.CalculatePointsNormal()
		
		obj = QGeometryRenderer()
		customGeo = QGeometry(obj)
		verticesBuffer = QBuffer(QBuffer.VertexBuffer, customGeo)
		idxBuffer = QBuffer(QBuffer.IndexBuffer, customGeo)
		
		vertices = b""
		for i in range(m.header.pointCount):
			p = m.points[i]
			vertices += struct.pack('3f', p.X/0x100, -p.Y/0x100, p.Z/0x100)
			
		verticesBuffer.setData(vertices)	
	
		
		idx = b""
		for i in range(m.header.planeCount):
			p = m.planes[i]
			for k in range(1, p.pointCount-1):
				idx += struct.pack('6H',p.points[k].id, p.points[k+1].id,  p.points[0].id, p.points[k+1].id, p.points[k].id, p.points[0].id)
		idxBuffer.setData(idx)
		
		positions = QAttribute()
		positions.setAttributeType(QAttribute.VertexAttribute)
		positions.setBuffer(verticesBuffer)
		positions.setDataType(QAttribute.Float)
		positions.setDataSize(3)
		positions.setByteOffset(0)
		positions.setByteStride(0)
		positions.setCount(m.header.pointCount)
		positions.setName(QAttribute.defaultPositionAttributeName())
		
		index = QAttribute()
		index.setAttributeType(QAttribute.IndexAttribute)
		index.setBuffer(idxBuffer)
		index.setDataType(QAttribute.UnsignedShort)
		index.setDataSize(1)
		index.setByteOffset(0)
		index.setByteStride(0)
		index.setCount(int(len(idx)/2))
		
		customGeo.addAttribute(positions)
		customGeo.addAttribute(index)
		
		obj.setPrimitiveType(QGeometryRenderer.Lines)
		obj.setInstanceCount(1)
		
		obj.setGeometry(customGeo)
		return obj	
			
def meshObject(id):
	with open(MODEL_PATH%id, 'rb') as f:
		m = Mesh.Mesh()
		m.Parse(f)
		m.CalculatePointsNormal()
		
		obj = QGeometryRenderer()
		customGeo = QGeometry(obj)
		verticesBuffer = QBuffer(QBuffer.VertexBuffer, customGeo)
		normalsBuffer = QBuffer(QBuffer.VertexBuffer, customGeo)
		idxBuffer = QBuffer(QBuffer.IndexBuffer, customGeo)
		
		vertices = b""
		normalsBuff = b""
		for i in range(m.header.pointCount):
			p = m.points[i]
			n = m.pointNormals[i]
			vertices += struct.pack('3f', p.X/0x100, -p.Y/0x100, p.Z/0x100)
			normalsBuff += struct.pack('3f', n.X, -n.Y, n.Z)
		verticesBuffer.setData(vertices)	
	
		idx = b""
		
		triangleCount = 0
		for i in range(m.header.planeCount):
			p = m.planes[i]
			n = m.normals[i]
			for k in range(1, p.pointCount-1):
				triangleCount += 1
				idx += struct.pack('3H', p.points[k+1].id, p.points[k].id, p.points[0].id)
				
				
		idxBuffer.setData(idx)
		normalsBuffer.setData(normalsBuff)	
		
		positions = QAttribute()
		positions.setAttributeType(QAttribute.VertexAttribute)
		positions.setBuffer(verticesBuffer)
		positions.setDataType(QAttribute.Float)
		positions.setDataSize(3)
		positions.setByteOffset(0)
		positions.setByteStride(0)
		positions.setCount(m.header.pointCount)
		positions.setName(QAttribute.defaultPositionAttributeName())
		
		normals = QAttribute()
		normals.setAttributeType(QAttribute.VertexAttribute)
		normals.setBuffer(normalsBuffer)
		normals.setDataType(QAttribute.Float)
		normals.setDataSize(3)
		normals.setByteOffset(0)
		normals.setByteStride(0)
		normals.setCount(m.header.pointCount)
		normals.setName(QAttribute.defaultNormalAttributeName())
		
		index = QAttribute()
		index.setAttributeType(QAttribute.IndexAttribute)
		index.setBuffer(idxBuffer)
		index.setDataType(QAttribute.UnsignedShort)
		index.setDataSize(1)
		index.setByteOffset(0)
		index.setByteStride(0)
		index.setCount(triangleCount*3)
		
		customGeo.addAttribute(positions)
		customGeo.addAttribute(normals)
		customGeo.addAttribute(index)
		
		obj.setPrimitiveType(QGeometryRenderer.Triangles)
		obj.setInstanceCount(1)
		
		obj.setGeometry(customGeo)
		return obj