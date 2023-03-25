import os
import sys
from core import PageWindow, Home, Register, Record, Upload
from PyQt5 import QtWidgets, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.m_pages = {}
        
        self.register(Register.WindowRegister(), 'register')
        self.register(Home.WindowHome(), 'home')
        self.register(Record.WindowRecord(), 'record')
        
        # Login page (Remember me option)
        self.goto('register')
    
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
            # self.showMaximized()
            self.setWindowTitle(widget.windowTitle())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) 
    myapp = MainWindow()
    myapp.show() 
    sys.exit(app.exec_())
