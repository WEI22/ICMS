from PyQt5 import QtWidgets, QtCore

class PageWindow(QtWidgets.QDialog):
    gotoSignal = QtCore.pyqtSignal(str)
    
    def goto(self, name):
        self.gotoSignal.emit(name)
    
    # Sidebar utilities
    def sidebar(self):
        labels = ['record','home', 'logout']
        for label in labels:
            getattr(self.ui,'sidebar_' + label).clicked.connect(getattr(self,label+'Clicked'))
    def homeClicked(self):
        self.goto('home')
    def logoutClicked(self):
        self.goto('logout')
    def recordClicked(self):
        self.goto('record')