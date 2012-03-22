#! /usr/bin/python
## Do some imports, man.
import sys
sys.path.append("./inc")
from PySide import QtCore, QtGui, QtSql

from form import Ui_Form
import Controller

class MainForm(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.control = Controller.Controller()
		self.logTimer = QtCore.QTimer()
		self.uiToConvertState()
		# Set up some initial states:
		self.ui.le_scenePath.setText("/Users/Murphy/github/local/ABCConvert_QT/test.mb")
		# Set the stylesheet
		sheetObj = open('./styles/style.qss')
		self.setStyleSheet(sheetObj.read())
		# Set up the history list:
		self.ui.list_scenes.setModel(self.control.histModel)
		self.ui.list_scenes.setSortingEnabled(True)
		self.ui.list_scenes.hideColumn(1)
		self.ui.list_scenes.hideColumn(4)
		self.ui.list_scenes.resizeColumnsToContents()
		#self.ui.list_scenes.sortByColumn()

		# Set up some slots and signals.
		self.ui.but_go.clicked.connect(self.startNewConversion)
		self.ui.but_tab_convert.clicked.connect(self.switchConvTab)
		self.ui.but_tab_history.clicked.connect(self.switchHistTab)
		self.ui.but_pick.clicked.connect(self.getSceneFile)
		self.ui.but_another.clicked.connect(self.uiToConvertState)
		self.connect(self.logTimer, QtCore.SIGNAL("timeout()"), self.updateLogProgbar)

	# Define some methods to react to signals
	def refreshStylesheet(self):
		sheetObj = open('./styles/style.qss')
		self.setStyleSheet(sheetObj.read())
		print "Realoaded"
	def switchConvTab(self):
		self.ui.stackedWidget.setCurrentWidget(self.ui.page_convert)
	def switchHistTab(self):
		self.ui.stackedWidget.setCurrentWidget(self.ui.page_history)
	def uiToConvertState(self):
		self.ui.frame_progress.hide()
		self.ui.frame_convert.show()
	def uiToProgressState(self):
		self.ui.frame_progress.show()
		self.ui.frame_convert.hide()

	def getSceneFile(self):
		fileName = QtGui.QFileDialog.getOpenFileName(self, \
			"Select Scene File", "/", "Maya Files (*.ma *.mb)")
		self.ui.le_scenePath.setText(fileName[0])

	def startNewConversion(self):
		path = self.ui.le_scenePath.text()
		if (path == ""):
			return
		self.control.startNewScene(path)
		self.logTimer.start()
		self.uiToProgressState()

	def updateLogProgbar(self):
		if self.control.getCurrentStatus() == "True":
			self.logTimer.stop()
		self.ui.te_activeLog.setText(self.control.getCurrentLog())
		self.ui.progressBar.setValue(int(self.control.getCurrentProgress()))

	def updateHistList(self):
		"""
		self.ui.list_scenes.clear()
		hist = self.control.getScenesHistory()
		hist.reverse()
		for entry in hist:
			title = "%s, Date: %s, Progress: %s, Status: %s"%(entry['name'],
				entry['date'], entry['progress'], entry['finished'])
			QtGui.QListWidgetItem(title, self.ui.list_scenes)
		if (self.ui.list_scenes.selectedItems() == []):
			self.ui.list_scenes.setCurrentRow(0)
		"""


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	mainapp = MainForm()
	mainapp.show()
	sys.exit(app.exec_())