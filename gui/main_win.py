import os
import sys
import time
import sqlite3
from passlib.hash import pbkdf2_sha256
from ui import Loading
from core import PageWindow, Home, Camera_win, Register
from core import Record as Record
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi

sys.path.insert(0, r"C:\Users\limhong1\Downloads\ICMS\gui")

class SplashScreen(QtWidgets.QSplashScreen):
    def __init__(self):
        super(QtWidgets.QSplashScreen, self).__init__()
        self.ui = Loading.Ui_Form()
        self.ui.setupUi(self)
        # self.setFixedWidth(1147)
        # self.setFixedHeight(778)
        # pixmap = QtGui.QPixmap("Image\\gradient-green.jpg")
        # pixmap = pixmap.scaled(1147, 778, QtCore.Qt.KeepAspectRatio)
        # self.setPixmap(pixmap)

    def progress(self):
        for i in range(101):
            self.ui.progressBar.setValue(i)
            QtWidgets.QApplication.processEvents()
            time.sleep(0.1)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        try:
            current_path = os.getcwd()
            saved_path = os.path.join(current_path, "saved")
            pest_path = os.path.join(saved_path, "pest")
            disease_path = os.path.join(saved_path, "disease")
            pest_original_path = os.path.join(pest_path, "original")
            disease_original_path = os.path.join(disease_path, "original")
            paths = [saved_path, pest_path, disease_path, pest_original_path, disease_original_path]
            for path in paths:
                os.makedirs(path)

        except Exception as e:
            print(e)

        self.m_pages = {}
        self.con = sqlite3.connect(r"C:\Users\User\Documents\UM\Year 4\Huawei Competition\project\gui\db.sqlite3")

        self.window_register = Register.WindowRegister(self.con)
        self.window_home = Home.WindowHome(self.con)
        self.window_camera = Camera_win.WindowCamera(self.con)
        self.window_record = Record.WindowRecord(self.con)
        
        self.register(self.window_register, 'register')
        self.register(self.window_home, 'home')
        self.register(self.window_camera, 'camera')
        self.register(self.window_record, 'record')

        # Login page (Remember me option)
        try:
            with open("log") as f:
                if pbkdf2_sha256.verify("HiThisisJesus", f.readline()):
                    self.goto("home")
                else:
                    self.goto("register")
        except Exception as e:
            print(e)

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow.PageWindow):
            widget.gotoSignal.connect(self.goto)
            
    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 

    myapp = MainWindow()
    myapp.show()

    sys.exit(app.exec_())
