#! /usr/bin/python
## Do some imports, man.
import sys
sys.path.append("./inc")
from PySide import QtCore, QtGui

from form import Ui_Form

class MainForm(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		# Set up some initial states:
		self.ui.frame_progress.hide()
		# Set the stylesheet
		sheetObj = open('./styles/style.qss')
		self.setStyleSheet(sheetObj.read())

		# Set up some slots and signals.
		self.ui.but_go.clicked.connect(self.refreshStylesheet)
		self.ui.but_tab_convert.clicked.connect(self.switchConvTab)
		self.ui.but_tab_history.clicked.connect(self.switchHistTab)

	# Define some methods to react to signals
	def refreshStylesheet(self):
		sheetObj = open('./styles/style.qss')
		self.setStyleSheet(sheetObj.read())
		print "Realoaded"
	def switchConvTab(self):
		self.ui.stackedWidget.setCurrentWidget(self.ui.page_convert)
	def switchHistTab(self):
		self.ui.stackedWidget.setCurrentWidget(self.ui.page_history)



if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	mainapp = MainForm()
	mainapp.show()
	sys.exit(app.exec_())