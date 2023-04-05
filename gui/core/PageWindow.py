from PyQt5 import QtWidgets, QtCore

class PageWindow(QtWidgets.QDialog):
    gotoSignal = QtCore.pyqtSignal(str)
    
    def goto(self, name):
        self.gotoSignal.emit(name)
    
    # Sidebar utilities
    def sidebar(self):
        labels = ['record', 'home', 'camera', 'logout']
        for label in labels:
            getattr(self.ui, 'sidebar_' + label).clicked.connect(getattr(self, label+'Clicked'))

    def homeClicked(self):
        self.goto('home')

    def cameraClicked(self):
        self.goto('camera')

    def logoutClicked(self):
        self.goto('logout')

    def recordClicked(self):
        self.goto('record')

    def setupLogoutMsgBox(self):
        self.logout_msgbox = QtWidgets.QMessageBox()
        self.logout_msgbox.setWindowTitle("Logout")
        self.logout_msgbox.setText("Are you sure?")
        self.logout_msgbox.setIcon(QtWidgets.QMessageBox.Question)
        self.logout_msgbox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.logout_msgbox.setDefaultButton(QtWidgets.QMessageBox.No)

    def logout(self):
        respond = self.logout_msgbox.exec_()
        if respond == QtWidgets.QMessageBox.Yes:
            self.goto("register")