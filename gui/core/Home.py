from PyQt5 import QtWidgets
from core import PageWindow
import os
import sys

CURRENT_DIR = os.getcwd()
BASE_DIR = os.path.dirname(CURRENT_DIR)

sys.path.insert(0, BASE_DIR)

from ui import Home

class WindowHome(PageWindow.PageWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Home.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()