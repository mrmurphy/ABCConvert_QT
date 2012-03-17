import sys
import getpass
import os
import sqlite3
import Shot

class Controller():
	def __init__(self):
		self.user=getpass.getuser()
		self.curSceneId = -1
		self.homeDir = os.path.expanduser("~")
		self.appDataDir = os.path.join(self.homeDir, ".alembictool")
		self.dbFile = os.path.join(self.appDataDir, "logDB.sqlite")
		self.sceneList = []
		self.curScene = ""
		# Set up the database, if it doesn't exist:
		if not (os.path.exists(self.appDataDir)):
			os.mkdir(self.appDataDir)

	## Heavy-hitting methods:
	def startNewScene(self, path):
		self.curScene = Shot.Shot(path, self.dbFile)
		#self.sceneList += self.curScene
		self.curScene.run()

	# Setters:
	def getUser(self):
		return self.user
	# Getters:
	def setScenePath(self, path):
		self.scenePath = path

if __name__ == "__main__":
	cnt = Controller()
	print cnt.getUser()
	print cnt.homeDir