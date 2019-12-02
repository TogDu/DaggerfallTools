from dagger import Mesh, BSA
		
# with open('ARCH3D.BSA', 'rb') as f:
	# blocks = BSA.BSA()
	# blocks.Parse(f)
	# for d in blocks.descrs:
		# f = open('out/models/%d.3d'%d.id, 'wb')
		# f.write(d.record)
		# f.close()

with open('BLOCKS.BSA', 'rb') as f:
	blocks = BSA.BSA()
	blocks.Parse(f)

		
		
# with open('out/models/61018.3d', 'rb') as f:
	# m = Mesh.Mesh()
	# m.Parse(f)
	# m.Print()
	
	
			