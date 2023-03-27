import os
import sys
import time
from ui import Loading
from core import PageWindow, Home, Register, Record, Upload
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi

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
        
        self.m_pages = {}

        self.window_register = Register.WindowRegister()
        self.window_home = Home.WindowHome()
        self.window_record = Record.WindowRecord()
        
        self.register(self.window_register, 'register')
        self.register(self.window_home, 'home')
        self.register(self.window_record, 'record')
        
        # Login page (Remember me option)
        self.goto('register')
    
    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow.PageWindow):
            # self.window_record.con.commit()
            # self.window_record.retrieve()
            # self.window_record.update()
            widget.gotoSignal.connect(self.goto)
            
    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            # self.showMaximized()
            self.setWindowTitle(widget.windowTitle())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 
    # myapp = MainWindow()
    # myapp.show()
    # splash = SplashScreen()
    # splash.show()
    # splash.progress()

    myapp = MainWindow()
    myapp.show()

    # splash.finish(myapp)
    sys.exit(app.exec_())