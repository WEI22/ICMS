from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChart, QBarSet, QBarSeries, QBarCategoryAxis

from ui import Home
from core.PageWindow import PageWindow

import random
import os

from datetime import datetime
from collections import Counter

CURRENT_DIR = os.getcwd()

class WindowHome(PageWindow):

    def __init__(self, con, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Home.Ui_Form()
        self.ui.setupUi(self)
        self.sidebar()

        self.setupLogoutMsgBox()
        self.updateGraphicView()

        self.con = con

        self.ui.today_button.clicked.connect(lambda: self.selectTimeFrame("today"))
        self.ui.week_button.clicked.connect(lambda: self.selectTimeFrame("week"))
        self.ui.month_button.clicked.connect(lambda: self.selectTimeFrame("month"))

        current_time = datetime.now()
        self.ui.time_label.setText(str(current_time.time())[:-7])
        self.ui.date_label.setText(str(current_time.date()))

        self.pest_dict = self.generatePestDict()

        self.showPestNumber()
        self.showChart()

        self.startTimer()
        self.startSlideshowTimer()

    def selectTimeFrame(self, time_frame):
        if time_frame == "today":
            self.ui.today_button.setEnabled(False)
            self.ui.week_button.setEnabled(True)
            self.ui.month_button.setEnabled(True)
            self.ui.week_button.setChecked(False)
            self.ui.month_button.setChecked(False)

        elif time_frame == "week":
            self.ui.today_button.setEnabled(True)
            self.ui.week_button.setEnabled(False)
            self.ui.month_button.setEnabled(True)
            self.ui.today_button.setChecked(False)
            self.ui.month_button.setChecked(False)

        elif time_frame == "month":
            self.ui.today_button.setEnabled(True)
            self.ui.week_button.setEnabled(True)
            self.ui.month_button.setEnabled(False)
            self.ui.today_button.setChecked(False)
            self.ui.week_button.setChecked(False)

    def showPestNumber(self):
        pest_num = sum(self.pest_dict.values())
        self.ui.pest_number.setText(str(pest_num))

    def showChart(self):
        pest_types = {"army_worm": 0, "legume_blister_beetle": 1, "red_spider": 2, "rice_gall_midge": 3, "rice_leaf_roller": 4, "rice_leafhopper": 5, "rice_water_weevil": 6, "wheat_phloeothrips": 7, "white_backed_plant_hopper": 8, "yellow_rice_borer": 9}
        pest_bars = [QBarSet(pest) for pest in pest_types]

        pest_dict = {}
        for i in self.data:
            if i[-2] not in pest_dict and i[1] != "":
                pest_dict[i[-2]] = Counter(i[1].split("\n"))
            elif i[1] != "":
                pest_dict[i[-2]].update(i[1].split("\n"))

        pest_series = QBarSeries()
        axis_x = QBarCategoryAxis()

        for date, pest in pest_dict.items():
            for key, value in pest.items():
                pest_bars[pest_types[key]] << value
            axis_x.append(date)

        for i in pest_bars:
            pest_series.append(i)

        chart = QChart()
        chart.addSeries(pest_series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.createDefaultAxes()
        chart.setAxisX(axis_x, pest_series)

        self.ui.chart.setChart(chart)

    def updateGraphicView(self):
        self.ui.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.ui.graphicsView.setRenderHint(QPainter.SmoothPixmapTransform)
        self.ui.graphicsView.setScene(QGraphicsScene())

        pic_path = os.path.join(CURRENT_DIR, "saved")
        pic_list = os.listdir(pic_path)

        if pic_list:
            pic_chosen = random.choice(pic_list)
            pixmap = QtGui.QPixmap(os.path.join(pic_path, pic_chosen))
            pixmap = pixmap.scaled(420, 320, QtCore.Qt.KeepAspectRatio)
            self.ui.graphicsView.scene().addPixmap(pixmap)

    def generatePestDict(self):
        self.data = self.con.execute("SELECT * FROM web_image").fetchall()
        pest_list = list(map(lambda x: x[1], self.data))
        pest_list = list(map(lambda x: x.split("\n"), pest_list))
        pest_list = [i for j in pest_list for i in j]
        pest_list = filter(lambda x: x != "", pest_list)
        return Counter(pest_list)

    def checkUpdate(self):
        current_time = datetime.now()
        updated_pest_dict = self.generatePestDict()
        self.ui.time_label.setText(str(current_time.time())[:-7])
        self.ui.date_label.setText(str(current_time.date()))
        if updated_pest_dict != self.pest_dict:
            self.pest_dict = updated_pest_dict
            self.showPestNumber()
            self.showChart()

    def startTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.checkUpdate)
        self.timer.start(1000)

    def startSlideshowTimer(self):
        self.slideshow_timer = QtCore.QTimer()
        self.slideshow_timer.timeout.connect(self.updateGraphicView)
        self.slideshow_timer.start(5000)