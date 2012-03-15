import time
import datetime
import sqlite3
import multiprocessing as mproc
import subprocess

class Shot():
    def __init__(self, shotName, dbname="shots.sqlite"):

        # Set up some member variables:
        self.shotName = shotName
        self.dbname = dbname
        ##
        date = str(datetime.datetime.now())
        self.OpenDB()
        self.cur.execute("INSERT INTO Shots (name, finished, date, \
            user, progress) VALUES (?,?,?,?,?)", \
            (shotName, 'False', date, 'default', '0'))
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
        try:
            out = subprocess.check_call("/grp5/anim-rgs/usr/autodesk/maya/bin/mayapy python/mayastart.py %s %s"%(self.shotName, self.rowid), shell=True)
        except subprocess.CalledProcessError:
            self.UpdateLog("Maya has crashed. SURPRISE!! Sorry.")
            print "\n\n\n\n\nCRAAAASHH!!!\n\n\n\n\n"

   ############

########################################
#################### Database Section
########################################

    def OpenDB(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def UpdateLog(self, message):
        print message
        self.OpenDB()
        self.cur.execute("SELECT log FROM Shots WHERE rowid=?",
                (self.rowid,))
        orig = str(self.cur.fetchone()[0])
        if (orig != "None"):
            message = orig + "<br>" + message
        self.cur.execute("UPDATE Shots SET log = ? where rowid = ?",
                (message, self.rowid))
        self.CommitAndCloseDB()

    def CommitAndCloseDB(self):
        self.conn.commit()
        self.conn.close()

    def GetId(self):
        return self.rowid

    def GetFinished(self):
        self.OpenDB()
        self.cur.execute("SELECT finished FROM Shots WHERE rowid=?",
                (self.rowid,))
        retstr = str(self.cur.fetchone()[0])
        self.CommitAndCloseDB()
        return retstr

    def GetLog(self):
        self.OpenDB()
        self.cur.execute("SELECT log FROM Shots WHERE rowid=?",
                (self.rowid,))
        retstr = str(self.cur.fetchone()[0])
        self.CommitAndCloseDB()
        return retstr

########################################
########################################
