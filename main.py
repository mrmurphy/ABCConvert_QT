#! /usr/bin/python
## Do some imports, man.
import sys
sys.path.append("./inc")
from PySide import QtCore, QtGui

from form import Ui_Form
import Controller

class MainForm(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.control = Controller.Controller()
		# Set up some initial states:
		#self.ui.frame_progress.hide()
		# Set the stylesheet
		sheetObj = open('./styles/style.qss')
		self.setStyleSheet(sheetObj.read())

		# Set up some slots and signals.
		self.ui.but_go.clicked.connect(self.startNewConversion)
		self.ui.but_tab_convert.clicked.connect(self.switchConvTab)
		self.ui.but_tab_history.clicked.connect(self.switchHistTab)
		self.ui.but_pick.clicked.connect(self.getSceneFile)

	# Define some methods to react to signals
	def refreshStylesheet(self):
		sheetObj = open('./styles/style.qss')
		self.setStyleSheet(sheetObj.read())
		print "Realoaded"
	def switchConvTab(self):
		self.ui.stackedWidget.setCurrentWidget(self.ui.page_convert)
	def switchHistTab(self):
		self.ui.stackedWidget.setCurrentWidget(self.ui.page_history)
	def getSceneFile(self):
		fileName = QtGui.QFileDialog.getOpenFileName(self, "Select Scene File", "/", "Maya Files (*.ma *.mb)")
		print fileName
		self.ui.le_scenePath.setText(fileName[0])

	def startNewConversion(self):
		path = self.ui.le_scenePath.text()
		if (path == ""):
			return
		self.control.startNewScene(path)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	mainapp = MainForm()
	mainapp.show()
	sys.exit(app.exec_())