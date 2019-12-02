from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import argparse
import json

from qt_view import DaggerMainView

VER_MAJOR = 0
VER_MINOR = 1

DEBUG_WIREFRAME = True
DEBUG_NORMALS = False
#  


class Application(QMainWindow):
	def __init__(self, rdb):
		super().__init__()
		#		
		view3d = DaggerMainView.DaggerMainView(rdb, DEBUG_WIREFRAME, DEBUG_NORMALS)
		self.setCentralWidget(view3d)
		self.setGeometry(QRect(100, 100, 900, 700))
		self.setWindowTitle('Daggertool : %s.RDB'%rdb['name'])
		self.show()


if __name__ == '__main__':
	parser = argparse.ArgumentParser('Daggerfall dungeon editor v%d.%d (READ ONLY)'%(VER_MAJOR, VER_MINOR))
	parser.add_argument('rdb', help = 'RDB file')
	args = parser.parse_args()
	if args.rdb: 
		with open(args.rdb) as f:
			rdb = json.loads(f.read())
			blockID = sys.argv[1].split('\\')[-1].split('.')[0]
			rdb['name'] = blockID
			app = QApplication(sys.argv)
			ex = Application(rdb)
			sys.exit(app.exec_())
	else:
		print(parser.usage())

