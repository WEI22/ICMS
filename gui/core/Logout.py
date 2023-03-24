from PyQt5 import QtWidgets, QtCore
from core import PageWindow
import os
import sys

CURRENT_DIR = os.getcwd()
BASE_DIR = os.path.dirname(CURRENT_DIR)

sys.path.insert(0, BASE_DIR)

from ui import Logout

class WindowLogout(PageWindow.PageWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Logout.Ui_Logout()
        self.ui.setupUi(self)
        self.sidebar()

        self.ui.yes_button.clicked.connect(self.confirm)
        self.ui.cancel_button.clicked.connect(QtCore.QCoreApplication.instance().quit())

    def confirm(self):
        pass

    def cancel(self):
        pass