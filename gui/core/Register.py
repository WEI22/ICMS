import sqlite3

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.Qt import QUrl, QDesktopServices
from core import PageWindow
import os
import sys
import re
from datetime import datetime
import psycopg2
from passlib.hash import pbkdf2_sha256

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
SIGNUP_URL = "http://192.168.100.43:8000/create-account/"

CURRENT_DIR = os.getcwd()
BASE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BASE_DIR)

from ui import Register

class WindowRegister(PageWindow.PageWindow):
    def __init__(self, con, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Register.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()

        self.con = con

        self.ui.sidebar_home.setEnabled(False)
        self.ui.sidebar_record.setEnabled(False)
        self.ui.sidebar_logout.setEnabled(False)
        self.ui.sidebar_camera.setEnabled(False)

        self.view_icon = QtGui.QPixmap(r"src\img\register\view.png")
        self.hidden_icon = QtGui.QPixmap(r"src\img\register\hidden.png")

        self.ui.login_btn.clicked.connect(self.login)
        self.ui.login_password_text.returnPressed.connect(self.login)
        self.ui.signup_link.clicked.connect(self.signup)
        self.ui.show_password.clicked.connect(self.showPassword)
        self.ui.login_msg_register.clicked.connect(self.signup)

    def login(self):
        self.con.commit()
        # self.con.cmd_refresh(self.REFRESH)
        cur = self.con.cursor()

        user = self.ui.login_email_text.text()
        password = self.ui.login_password_text.text()

        if re.match(EMAIL_REGEX, user):
            cur.execute(f"SELECT password1 FROM web_user WHERE email='{user}';")
            password_from_db = cur.fetchone()
            # password_from_db = cur.execute(f"SELECT password1 FROM web_user WHERE email='{user}';").fetchone()
        else:
            cur.execute(f"SELECT password1 FROM web_user WHERE username='{user}';")
            password_from_db = cur.fetchone()
            # password_from_db = cur.execute(f"SELECT password1 FROM web_user WHERE username='{user}';").fetchone()

        if password_from_db and password == password_from_db[0]:
            self.ui.login_password_text.setText("")
            self.ui.login_msg_register.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

            if self.ui.login_remember.isChecked():
                hash = pbkdf2_sha256.hash("HiThisisJesus")
                with open("log", "w") as f:
                    f.write(hash)

            self.homeClicked()
        elif password_from_db is None:
            self.ui.login_msg.setText("Cannot find your email/username! ")
            self.ui.login_msg_register.setText("Register here")
            self.ui.login_msg_register.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        elif password != password_from_db[0]:
            self.ui.login_msg.setText("Wrong password")

    def signup(self):
        url = QUrl(SIGNUP_URL)
        QDesktopServices.openUrl(url)

    def showPassword(self):
        if self.ui.show_password.pixmap().cacheKey() == self.hidden_icon.cacheKey():
            self.ui.show_password.setPixmap(self.view_icon)
            self.ui.login_password_text.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.ui.show_password.setPixmap(self.hidden_icon)
            self.ui.login_password_text.setEchoMode(QtWidgets.QLineEdit.Password)