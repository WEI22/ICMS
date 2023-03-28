from PyQt5 import QtWidgets, QtGui, QtCore
from core import PageWindow
import os
import sys
import sqlite3
import psycopg2
from core.clickableLabel import ClickableLabel

CURRENT_DIR = os.getcwd()
BASE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BASE_DIR)

from ui import Record

class WindowRecord(PageWindow.PageWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Record.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()

        self.setupLogoutMsgBox()
        # self.con = sqlite3.connect(r"C:\Users\User\Desktop\Github\ICMS\webui\db.sqlite3")
        self.con = psycopg2.connect(
            host='192.168.100.43',
            user='postgres',
            password='1234',
            database='db',
            port='5432'
        )
        self.recordFull = {'img': [], 'time': [], 'pest': [], 'loc': []}
        self.record = {'img': [], 'time': [], 'pest': [], 'loc': []}
        self.tableElement = {'img': [], 'time': [], 'pest': [], 'loc': [], 'layout': []}
        self.start()

        self.ui.sidebar_logout.clicked.connect(self.logout)
        self.ui.record_search_btn.clicked.connect(self.searchClicked)
        self.ui.record_search.returnPressed.connect(self.searchClicked)
    
    def retrieve(self):
        cur = self.con.cursor()
        if self.getData("image") != None:
            imgs = [img[0] for img in self.getData("image")]
            dates = [date[0] for date in self.getData("date_created")]
            times = []
            for i, time in enumerate(self.getData("time_created")):
                times.append(str(dates[i]) + '\n' + str(time[0])[:8])
            pests = [pest[0] for pest in self.getData("pest")]
            locs = [loc[0] for loc in self.getData("location")]
        else:
            imgs = []
            times = []
            pests = []
            locs = []

        self.recordFull = {'img': imgs, 'time': times, 'pest': pests, 'loc': locs}
        self.record = {'img': imgs, 'time': times, 'pest': pests, 'loc': locs}
        self.update()
        
    def update(self):
        self.delete()
        self.tableElement = {'img': [], 'time': [], 'pest': [], 'loc': [], 'layout': []}
        labels = ['img', 'time', 'pest', 'loc']
        if 10-len(self.record['img']) > 0:
            for i in range(10-len(self.record['img'])):
                for label in labels:
                    self.record[label].append('')
        for i in range(len(self.record['img'])):
            if self.record['img'][i] == "":
                self.addEmptyLine(i+1)
            else:
                self.addLine(i+1)
            for label in labels:
                if label != 'img':
                    self.tableElement[label][i].setText(str(self.record[label][i]))
#                 else:
#                     self.tableElement[label][i].setPixmap(QtGui.QPixmap(str(self.record[label][i])))
                
        for i in range(len(self.record['img'])):
            self.tableElement['img'][i].clicked.connect(lambda i=i: self.imageClicked(self.record['img'][i]) )

    def addLine(self, i):
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setSpacing(0)
        horizontalLayout.setObjectName("record_table%d"%i)
        
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(75)
        
        img = ClickableLabel(self.ui.scrollAreaWidgetContents)
        img.setFont(font)
        img.setStyleSheet("border: 0.5px solid black")
        image = QtGui.QPixmap("Image/share.png")
        image = image.scaled(24,24,QtCore.Qt.KeepAspectRatio)
        img.setPixmap(image)
        img.setAlignment(QtCore.Qt.AlignCenter)
        img.setObjectName("record_table_date%d"%i)
        horizontalLayout.addWidget(img)
        
        time = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
        time.setFont(font)
        time.setStyleSheet("border: 0.5px solid black")
        time.setAlignment(QtCore.Qt.AlignCenter)
        time.setObjectName("record_table_host%d"%i)
        horizontalLayout.addWidget(time)
                                
        pest = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
        pest.setFont(font)
        pest.setStyleSheet("border: 0.5px solid black")
        pest.setAlignment(QtCore.Qt.AlignCenter)
        pest.setObjectName("record_table_pest%d"%i)
        horizontalLayout.addWidget(pest)
        
        loc = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
        loc.setFont(font)
        loc.setStyleSheet("border: 0.5px solid black")
        loc.setAlignment(QtCore.Qt.AlignCenter)
        loc.setObjectName("record_table_total%d"%i)
        horizontalLayout.addWidget(loc)
        
        horizontalLayout.setStretch(0, 1)
        horizontalLayout.setStretch(1, 1)
        horizontalLayout.setStretch(2, 1)
        horizontalLayout.setStretch(3, 1)
        self.ui.record_table_vertical.addLayout(horizontalLayout)
        
        self.tableElement['img'].append(img)
        self.tableElement['time'].append(time)
        self.tableElement['pest'].append(pest)
        self.tableElement['loc'].append(loc)
        self.tableElement['layout'].append(horizontalLayout)
        
    def addEmptyLine(self, i):
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setSpacing(0)
        horizontalLayout.setObjectName("record_table%d"%i)
        
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(75)
        
        img = ClickableLabel(self.ui.scrollAreaWidgetContents)
        img.setFont(font)
        img.setStyleSheet("border: 0.5px solid black")
        img.setAlignment(QtCore.Qt.AlignCenter)
        img.setObjectName("record_table_date%d"%i)
        horizontalLayout.addWidget(img)
        
        time = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
        time.setFont(font)
        time.setStyleSheet("border: 0.5px solid black")
        time.setAlignment(QtCore.Qt.AlignCenter)
        time.setObjectName("record_table_host%d"%i)
        horizontalLayout.addWidget(time)
                                
        pest = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
        pest.setFont(font)
        pest.setStyleSheet("border: 0.5px solid black")
        pest.setAlignment(QtCore.Qt.AlignCenter)
        pest.setObjectName("record_table_pest%d"%i)
        horizontalLayout.addWidget(pest)
        
        loc = QtWidgets.QLabel(self.ui.scrollAreaWidgetContents)
        loc.setFont(font)
        loc.setStyleSheet("border: 0.5px solid black")
        loc.setAlignment(QtCore.Qt.AlignCenter)
        loc.setObjectName("record_table_total%d"%i)
        horizontalLayout.addWidget(loc)
        
        horizontalLayout.setStretch(0, 1)
        horizontalLayout.setStretch(1, 1)
        horizontalLayout.setStretch(2, 1)
        horizontalLayout.setStretch(3, 1)
        self.ui.record_table_vertical.addLayout(horizontalLayout)
        
        self.tableElement['img'].append(img)
        self.tableElement['time'].append(time)
        self.tableElement['pest'].append(pest)
        self.tableElement['loc'].append(loc)
        self.tableElement['layout'].append(horizontalLayout)
        
    def imageClicked(self, imagePath):
        dialog = QtWidgets.QDialog()
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        label.setPixmap(QtGui.QPixmap(imagePath))
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.setWindowTitle(imagePath[imagePath.rfind('\\')+1:])
        dialog.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint,False)
        dialog.exec_()
        
    def searchClicked(self):
        labels = ['time','pest','loc']
        search_text = str(self.ui.record_search.text())
        self.showId = [False for i in range(len(self.recordFull['time']))]
        self.record = {'img':[], 'time':[], 'pest':[], 'loc':[]}
        for i in range(len(self.recordFull['time'])):
            for label in labels:
                if search_text in str(self.recordFull[label][i]):
                    self.showId[i] = True
        labels = ['img','time','pest','loc']
        for i in range(len(self.recordFull['time'])):
            if self.showId[i]:
                for label in labels:
                    self.record[label].append(self.recordFull[label][i])
        self.update()
#         self.addLoading()
        
    def delete(self):
        for layout in self.tableElement['layout']:
            while layout.count():
                layout.takeAt(0).widget().deleteLater()

    def addLoading(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Search successful!!")
        msgBox.exec_()

    def getData(self, column, table="web_image"):
        cur = self.con.cursor()
        cur.execute(f"SELECT {column} FROM {table} ORDER BY time_created")
        return cur.fetchall()

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.retrieve)
        self.timer.start(1000)