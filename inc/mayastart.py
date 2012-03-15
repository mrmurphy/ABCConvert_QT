import sys
import os
sys.path.append("python/")
import Converter

def ABCPyCallback(frameno):
    curshot.UpdateLog("ABC Exporting frame number: %s"%(frameno))

curshot = Converter.Converter(sys.argv[1], sys.argv[2])
curshot.run()

os._exit(0);
