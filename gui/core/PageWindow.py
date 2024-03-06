from PyQt5 import QtWidgets, QtCore
import os

class PageWindow(QtWidgets.QWidget):
    gotoSignal = QtCore.pyqtSignal(str)
    
    def goto(self, name):
        self.gotoSignal.emit(name)
    
    # Sidebar utilities
    def sidebar(self):
        labels = ['record', 'home', 'camera']
        for label in labels:
            getattr(self.ui, 'sidebar_' + label).clicked.connect(getattr(self, label+'Clicked'))

    def homeClicked(self):
        self.goto('home')

    def cameraClicked(self):
        self.goto('camera')

    def recordClicked(self):
        self.goto('record')
