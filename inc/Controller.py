import getpass
import os
import sqlite3
import Scene
from PySide import QtSql


class Controller():
    def __init__(self):
        self.user = getpass.getuser()
        self.curSceneId = -1
        self.homeDir = os.path.expanduser("~")
        self.appDataDir = os.path.join(self.homeDir, ".alembictool")
        self.dbFile = os.path.join(self.appDataDir, "logDB.sqlite")
        self.curScene = ""
        # Set up the database, if it doesn't exist:
        if not (os.path.exists(self.appDataDir)):
            os.mkdir(self.appDataDir)

        # Set up the database access, for QT
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.dbFile)
        self.histModel = QtSql.QSqlTableModel()
        self.histModel.setTable("Scenes")
        self.updateScenesTableModel()

    ## Heavy-hitting methods:
    def startNewScene(self, path):
        self.curScene = Scene.Scene(path, self.dbFile)
        #self.sceneList += self.curScene
        self.curScene.run()

    # Getters:
    def getUser(self):
        return self.user

    def getCurrentStatus(self):
        return self.curScene.GetFinished()

    def getCurrentLog(self):
        return self.curScene.GetLog()

    def getCurrentProgress(self):
        return self.curScene.GetProgress()

    # Setters:
    def setScenePath(self, path):
        self.scenePath = path

    def updateScenesTableModel(self):
        self.histModel.select()

    #### DB Methods ####
    def getScenesHistory(self):
        with sqlite3.connect(self.dbFile) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("""
            select rowid,* from Scenes
            """)
            entries = cur.fetchall()
            return entries

if __name__ == "__main__":
    cnt = Controller()
    #print cnt.getUser()
    #print cnt.homeDir
    hist = cnt.getScenesHistory()
    print(hist[0]['name'])
