import pymel.core as pm
import os
import sqlite3

class Converter():
    def __init__(self, SceneName, rowid, DbFile):

        # Set up some member variables:
        self.SceneName = SceneName
        self.DbFile = DbFile
        self.dir = os.path.dirname(self.SceneName)
        self.fileTitle = os.path.basename(self.SceneName)[:-3]
        self.cacheDir = os.path.join(self.dir, "cache")
        self.abcLoc = os.path.join(self.cacheDir, self.fileTitle + ".abc")
        self.outFile = os.path.join(self.dir, self.fileTitle + "_cache" + ".mb")
        self.rowid = rowid
        if not (os.path.isdir(self.cacheDir)):
            os.mkdir(self.cacheDir)
        # This is just a messy patch, to preserve the naming convention
        # in estefan.
        if ('estefan' in SceneName and 'Animation' in self.fileTitle):
            temp = self.fileTitle.replace("Animation", "Cache")
            self.outFile = SceneName.replace(self.fileTitle, temp);

    ################
    ###### Public Methods ######
    def run(self):
        self._processScene()
    ######


    ############
    ##### Private Member Methods ######

    def _processScene(self):
        # Set RMS Debug level
        os.environ['RMSDEBUG'] = '1'
        self.UpdateLog("Importing plugins...")

        # Load plugins
        pm.loadPlugin("AbcExport")
        pm.loadPlugin("AbcImport")

        # Loading the file.
        self.UpdateLog("Maya now opening file: \n" + self.SceneName)
        pm.openFile(self.SceneName, force=1)
        self.UpdateProgress(10);

        # Import all references.
        self._importAllReferences()
        self.UpdateProgress(20);

        # Build a list of all of the exportable geometry in the scene.
        abcExportObjs = self._selectObjs()
        self.UpdateProgress(30);

        # Get the start frame and end frame
        startFrame = pm.playbackOptions(q=1, minTime=True) 
        startFrame -= 5 # Adjust to allow for preroll
        self.UpdateLog("First frame of Scene is: %s"%(startFrame))
        endFrame = pm.SCENE.defaultRenderGlobals.endFrame.get()
        endFrame = pm.playbackOptions(q=1, maxTime=True) 
        self.UpdateLog("Last frame of Scene is: %s"%(endFrame))

        # Alembic export it
        self._exportABC(abcExportObjs, startFrame, endFrame, self.abcLoc)
        self.UpdateProgress(40);

        # Export Shaders
        self.UpdateLog("Writing shaders to file..." + self.outFile)
        self._exportShaders()
        self.UpdateProgress(50);

        # Store the shaders for re-application later.
        self.UpdateLog("Storing the shaders for re-application...")
        shadersDict = self._storeShaders()
        self.UpdateProgress(60);

        # Make a new file
        self.UpdateLog("Opening new file..." + self.outFile)
        pm.openFile(self.outFile, force=1)
        self.UpdateProgress(70);

        # Import ABC Cache
        self.UpdateLog("Importing ABC cache..." + self.abcLoc)
        pm.mel.eval('AbcImport -ftr -d "%s"'%(self.abcLoc))
        self.UpdateProgress(80);

        # Re-apply the shaders
        self.UpdateLog("Re-applying shaders...")
        self._restoreShaders(shadersDict)
        self.UpdateProgress(90);

        # Save the file
        self.UpdateLog("Saving the maya file: " + self.outFile)
        os.system("chmod 755 " + self.outFile)
        pm.saveFile(force=1)
        os.system("chmod 755 " + self.outFile)
        self.UpdateLog("File saved.")
        self.UpdateProgress(100)

    def _importAllReferences(self):
        self.UpdateLog("Importing all references...")
        # Import all references in file
        done = False
        while (done == False and (len(pm.listReferences()) != 0) ):
            refs = pm.listReferences()
            self.UpdateLog("Importing " + str(len(refs)) + " references.")
            for ref in refs:
                if ref.isLoaded():
                    done = False
                    ref.importContents()
                else:
                    done = True
        self.UpdateLog("Done importing references...")
        return True

    def _ABCPyCallback(self, frameno):
        self.UpdateLog("ABC Exporting frame number: %s"%(frameno))

    def _exportABC(self, objs, startFrame, endFrame, ABC_LOC):
        rootsStr = ""
        objs = pm.ls(sl=True)
        for obj in objs:
            rootsStr += " -root %s"%(obj.name())
        abcCommand = 'AbcExport -j "-writeVisibility -uv -worldSpace ' + \
                '-pfc ABCPyCallback(#FRAME#) ' + \
                '-frameRange %s %s %s -file %s"'%(startFrame, endFrame, \
                                                 rootsStr, ABC_LOC)
        #self.UpdateLog(abcCommand)
        #print abcCommand
        self.UpdateLog("Writing ABC data to file: "+ ABC_LOC)
        pm.mel.eval(abcCommand)

    def _storeShaders(self):
        print "Storing shaders"
        objects = pm.ls(g=1)
        shaders = {}
        for obj in objects:
            if(len(obj.shadingGroups()) > 0):
                shaders[str(obj)] = map(str, obj.shadingGroups())
        return shaders

    def _exportShaders(self):
        shaders = pm.ls(materials=1)
        selection = []
        # Select all shaders that are attatched to meshes.
        for shd in shaders:
            grps = shd.shadingGroups()
            for grp in shd.shadingGroups():
                for member in grp.members():
                    if("Mesh" in str(repr(member))):
                        selection.append(shd)
                        selection.append(grp)
        pm.select(clear=1)
        pm.select(selection, ne=1)
        pm.exportSelected(self.outFile, shader=1, force=1)

    def _restoreShaders(self, shadersDict):
        objsInScene = set(map(str, pm.ls()))
        for obj, shs in shadersDict.iteritems():
            if ( str(obj) in objsInScene ):
                for shader in shs:
                    if (str(shader) in objsInScene):
                        pm.select(obj)
                        pm.sets(shader, fe=1)

    def _sel_addRigGeo(self):
        sel = pm.ls(regex='*_[rR]igs*\d*[_:][Gg]eo')
        return sel

    def _sel_addOtherGeo(self):
        # Add any non-character geo
        retsel = []
        geolist = pm.ls(g=True, v=True)
        for geo in geolist:
            if ("_rig" not in geo.name() and \
                "_Rig" not in geo.name() ):
                # This is important, I only want to select
                # the top-most transform node for alembic 
                # export. That's what this command does.
                parent = geo.getParent(-1)
                if ("_rig" not in parent.name() and \
                    "_Rig" not in parent.name()):
                    retsel.append(parent)
        return retsel

    def _sel_addCameras(self):
        # Select any non-default cameras
        excludes = ["persp","top","front","side"]
        retsel = []
        camlist = pm.ls(ca=True)
        for cam in camlist:
            exclude = False
            for exname in excludes:
                if cam.startswith(exname):
                    exclude=True
            if not exclude:
                retsel.append(cam.getParent(-1))
        return retsel
        
    def _selectObjs(self):
        pm.select(clear=True)
        sel = []

        # Get geo in the scene.
        sel = (self._sel_addOtherGeo())
        # Get geo from rigs.
        rigGeo = self._sel_addRigGeo()
        if len(rigGeo) != 0:
            sel.append(rigGeo)
        # Get animation cameras, or layout.
        cams = self._sel_addCameras()
        if len(cams) != 0:
            sel.append(cams)
        pm.select(sel)
        return sel

    ############

########################################
#################### Database Section
########################################

    def UpdateFinished(self, status):
        self.OpenDB()
        self.cur.execute("UPDATE Scenes SET finished = ? where rowid = ?",
                (status, self.rowid))
        self.CommitAndCloseDB()

    def OpenDB(self):
        self.conn = sqlite3.connect(self.DbFile)
        self.cur = self.conn.cursor()

    def CommitAndCloseDB(self):
        self.conn.commit()
        self.conn.close()

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
    
    def UpdateProgress(self, prog):
        self.OpenDB()
        self.cur.execute("UPDATE Scenes SET progress = ? WHERE rowid=?",
                (prog, self.rowid))
        self.CommitAndCloseDB();

    def SetName(self, name):
        self.OpenDB()
        self.cur.execute("UPDATE Scenes SET name = ? where rowid = ?",
                (name, self.rowid))
        self.CommitAndCloseDB()

########################################
########################################
