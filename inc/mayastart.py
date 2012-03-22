import sys
import os
sys.path.append("python/")
import Converter

def ABCPyCallback(frameno):
    curScene.UpdateLog("ABC Exporting frame number: %s"%(frameno))

curScene = Converter.Converter(sys.argv[1], sys.argv[2])
curScene.run()

os._exit(0);
