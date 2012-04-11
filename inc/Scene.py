import datetime
import sqlite3
import multiprocessing as mproc
import subprocess
import sys
import os


class Scene():
    def __init__(self, SceneName, DbFile):

        # Set up some member variables:
        self.SceneName = SceneName
        self.DbFile = DbFile
        ##
        date = str(datetime.datetime.now())
        # Create the table, if it doesn't exist:
        self.CreateTable()
        #####
        self.OpenDB()
        self.cur.execute("INSERT INTO Scenes (name, finished, date, \
            user, progress) VALUES (?,?,?,?,?)", \
            (SceneName, 'False', date, 'default', '0'))
        self.rowid = str(self.cur.lastrowid)
        self.conn.commit()
        self.CommitAndCloseDB()

    ################
    ###### Public Methods ######
    def run(self):
        p = mproc.Process(target=self._callMaya)
        p.start()
    ######

    ############
    ##### Private Member Methods ######
    def _callMaya(self):
        """
        self.UpdateLog("I just got sent, and I work!") # DEBUG
        time.sleep(1) # DEBUG
        self.UpdateLog("working") # DEBUG
        self.UpdateProgress(10)
        time.sleep(1) # DEBUG
        self.UpdateLog("working") # DEBUG
        self.UpdateProgress(20)
        time.sleep(1) # DEBUG
        self.UpdateLog("working") # DEBUG
        self.UpdateProgress(30)
        time.sleep(1) # DEBUG
        self.UpdateLog("working") # DEBUG
        self.UpdateProgress(40)
        time.sleep(1) # DEBUG
        self.UpdateLog("working") # DEBUG
        self.UpdateProgress(50)
        time.sleep(1) # DEBUG
        self.UpdateLog("working") # DEBUG
        self.UpdateProgress(60)
        time.sleep(1) # DEBUG
        self.UpdateLog("working") # DEBUG
        self.UpdateProgress(70)
        time.sleep(1) # DEBUG
        self.UpdateLog("working") # DEBUG
        self.UpdateProgress(80)
        time.sleep(1) # DEBUG
        self.UpdateLog("working") # DEBUG
        self.UpdateProgress(90)
        time.sleep(1) # DEBUG
        self.UpdateLog("I just waited ten seconds, and I finished.") # DEBUG
        self.UpdateProgress(100)
        self.UpdateFinished("True")
        """
        try:
            curdir = sys.path[0]
            mayastart = os.path.join(curdir, "inc/mayastart.py")
            mayapy = "/Applications/Autodesk/maya2012/" + \
                "Maya.app/Contents/bin/mayapy"
            subprocess.check_call("%s %s %s %s %s"\
                % (mayapy, mayastart, self.SceneName, \
                    self.rowid, self.DbFile), shell=True)
        except subprocess.CalledProcessError:
            self.UpdateLog("Maya has crashed. SURPRISE!! Sorry.")
            print "\n\n\n\n\nCRAAAASHH!!!\n\n\n\n\n"

   ############

########################################
#################### Database Section
########################################

    def OpenDB(self):
        self.conn = sqlite3.connect(self.DbFile)
        self.cur = self.conn.cursor()

    def CreateTable(self):
        self.OpenDB()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Scenes (\
        name TEXT,\
        log TEXT, \
        finished TEXT, \
        date TEXT, \
        user TEXT, \
        progress TEXT \
        )''')
        self.CommitAndCloseDB()

    def UpdateLog(self, message):
        print message
        self.OpenDB()
        self.cur.execute("SELECT log FROM Scenes WHERE rowid=?",
                (self.rowid,))
        orig = str(self.cur.fetchone()[0])
        if (orig != "None"):
            message = orig + "<br>" + message
        self.cur.execute("UPDATE Scenes SET log = ? where rowid = ?",
                (message, self.rowid))
        self.CommitAndCloseDB()

    def UpdateFinished(self, status):
        self.OpenDB()
        self.cur.execute("UPDATE Scenes SET finished = ? where rowid = ?",
                (status, self.rowid))
        self.CommitAndCloseDB()

    def UpdateProgress(self, prog):
        self.OpenDB()
        self.cur.execute("UPDATE Scenes SET progress = ? WHERE rowid=?",
                (prog, self.rowid))
        self.CommitAndCloseDB()

    def CommitAndCloseDB(self):
        self.conn.commit()
        self.conn.close()

    def GetId(self):
        return self.rowid

    def GetFinished(self):
        self.OpenDB()
        self.cur.execute("SELECT finished FROM Scenes WHERE rowid=?",
                (self.rowid,))
        retstr = str(self.cur.fetchone()[0])
        self.CommitAndCloseDB()
        return retstr

    def GetProgress(self):
        self.OpenDB()
        self.cur.execute("SELECT progress FROM Scenes WHERE rowid=?",
                (self.rowid,))
        retstr = str(self.cur.fetchone()[0])
        self.CommitAndCloseDB()
        return retstr

    def GetLog(self):
        self.OpenDB()
        self.cur.execute("SELECT log FROM Scenes WHERE rowid=?",
                (self.rowid,))
        retstr = str(self.cur.fetchone()[0])
        self.CommitAndCloseDB()
        return retstr

########################################
########################################
