from PyQt5.Qt3DRender import QGeometryRenderer, QGeometry, QBuffer, QAttribute

import struct

def lineObject( srcPt, destPt):
	obj = QGeometryRenderer()
	customGeo = QGeometry(obj)
	verticesBuffer = QBuffer(QBuffer.VertexBuffer, customGeo)
	idxBuffer = QBuffer(QBuffer.IndexBuffer, customGeo)
	
	vertices = b""
	idx = b""

	vertices += struct.pack('3f', srcPt.X/0x100, -srcPt.Y/0x100, srcPt.Z/0x100)
	vertices += struct.pack('3f', destPt.X/0x100, -destPt.Y/0x100, destPt.Z/0x100)
	
	idx += struct.pack('2H', 0,1)
	
	verticesBuffer.setData(vertices)	
	idxBuffer.setData(idx)
	
	positions = QAttribute()
	positions.setAttributeType(QAttribute.VertexAttribute)
	positions.setBuffer(verticesBuffer)
	positions.setDataType(QAttribute.Float)
	positions.setDataSize(3)
	positions.setByteOffset(0)
	positions.setByteStride(0)
	positions.setCount(2)
	positions.setName(QAttribute.defaultPositionAttributeName())
	
	index = QAttribute()
	index.setAttributeType(QAttribute.IndexAttribute)
	index.setBuffer(idxBuffer)
	index.setDataType(QAttribute.UnsignedShort)
	index.setDataSize(1)
	index.setByteOffset(0)
	index.setByteStride(0)
	index.setCount(2)
	
	customGeo.addAttribute(positions)
	customGeo.addAttribute(index)
	
	obj.setPrimitiveType(QGeometryRenderer.Lines)
	obj.setInstanceCount(1)
	
	obj.setGeometry(customGeo)
	return obj	