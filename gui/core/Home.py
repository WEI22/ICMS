from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QChart, QBarSet, QBarSeries, QBarCategoryAxis
from PyQt5.QtChart import QChart, QPieSeries, QPieSlice

from ui import Home
from core.PageWindow import PageWindow

import random
import os

from datetime import datetime, date, timedelta
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

        self.ui.sidebar_logout.clicked.connect(self.logout)
        self.ui.today_button.clicked.connect(lambda: self.selectTimeFrame("today"))
        self.ui.week_button.clicked.connect(lambda: self.selectTimeFrame("week"))
        self.ui.month_button.clicked.connect(lambda: self.selectTimeFrame("month"))

        current_time = datetime.now()
        self.ui.time_label.setText(str(current_time.time())[:-7])
        self.ui.date_label.setText(str(current_time.date()))

        self.pest_data = self.con.execute("SELECT * FROM web_pest").fetchall()
        # self.disease_data = self.con.execute("SELECT * FROM web_disease").fetchall()

        self.timeframe = "today"
        self.showNumber(self.pest_data, "pest")
        # self.showNumber(self.disease_data, "disease")
        self.showPieChart(self.pest_data, "pest")
        # self.showPieChart(self.disease_data, "disease")

        self.startTimer()
        self.startSlideshowTimer()

    def selectTimeFrame(self, time_frame):
        if time_frame == "today":
            self.ui.today_button.setEnabled(False)
            self.ui.week_button.setEnabled(True)
            self.ui.month_button.setEnabled(True)
            self.ui.week_button.setChecked(False)
            self.ui.month_button.setChecked(False)

            self.timeframe = "today"

        elif time_frame == "week":
            self.ui.today_button.setEnabled(True)
            self.ui.week_button.setEnabled(False)
            self.ui.month_button.setEnabled(True)
            self.ui.today_button.setChecked(False)
            self.ui.month_button.setChecked(False)

            self.timeframe = "week"

        elif time_frame == "month":
            self.ui.today_button.setEnabled(True)
            self.ui.week_button.setEnabled(True)
            self.ui.month_button.setEnabled(False)
            self.ui.today_button.setChecked(False)
            self.ui.week_button.setChecked(False)

            self.timeframe = "month"

        self.showPieChart(self.pest_data, "pest")
        # self.showPieChart(self.disease_data, "disease")
        self.showNumber(self.pest_data, "pest")
        # self.showNumber(self.disease_data, "disease")

    def showNumber(self, data, type):
        today_date = date.today()
        counter = Counter()
        for i in data:
            data_date = datetime.strptime(i[-2], "%Y-%m-%d").date()
            if self.timeframe == "today" and data_date == today_date:
                counter.update(i[1].split("\n"))
            elif self.timeframe == "week" and today_date - data_date <= timedelta(days=7):
                counter.update(i[1].split("\n"))
            elif self.timeframe == "month" and today_date - data_date <= timedelta(days=30):
                counter.update(i[1].split("\n"))

        if "" in counter:
            counter.pop("")
        num = sum(counter.values())
        getattr(self.ui, f"{type}_number").setText(str(num))

    def showPieChart(self, data, type):
        counter = Counter()
        today_date = date.today()
        for i in data:
            data_date = datetime.strptime(i[-2], '%Y-%m-%d').date()
            if self.timeframe == "today" and data_date == today_date:
                counter.update(i[1].split("\n"))
            elif self.timeframe == "week" and today_date - data_date <= timedelta(days=7):
                counter.update(i[1].split("\n"))
            elif self.timeframe == "month" and today_date - data_date <= timedelta(days=30):
                counter.update(i[1].split("\n"))

        if "" in counter:
            counter.pop("")
        if counter:
            self.series = QPieSeries()
            slices = list()
            for key, value in counter.items():
                slice_ = QPieSlice(key, value)
                slice_.setLabelVisible()
                slices.append(slice_)
                self.series.append(slice_)

            for slice_ in slices:
                label = "<p align='center'>{}% {}</p>".format(round(slice_.percentage()*100, 2), slice_.label())
                slice_.setLabel(label)

            chart = QChart()
            chart.legend().hide()
            chart.addSeries(self.series)
            chart.createDefaultAxes()
            chart.setAnimationOptions(QChart.SeriesAnimations)

        else:
            chart = QChart()
            chart.setTitle(f"No {type.capitalize()} Detected")

        getattr(self.ui, f"{type}_chart").setChart(chart)

    def updateGraphicView(self):
        self.ui.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.ui.graphicsView.setRenderHint(QPainter.SmoothPixmapTransform)
        self.ui.graphicsView.setScene(QGraphicsScene())

        pic_path = os.path.join(CURRENT_DIR, "saved")
        type_list = os.listdir(pic_path)
        type_chosen = random.choice(type_list)
        pic_path = os.path.join(pic_path, type_chosen)
        pic_list = os.listdir(pic_path)
        pic_list = list(filter(lambda x: str(x).endswith(".jpg"), pic_list))

        if pic_list:
            pic_chosen = random.choice(pic_list)
            pixmap = QtGui.QPixmap(os.path.join(pic_path, pic_chosen))
            pixmap = pixmap.scaled(420, 320, QtCore.Qt.KeepAspectRatio)
            self.ui.graphicsView.scene().addPixmap(pixmap)

    def checkUpdate(self):
        current_time = datetime.now()
        updated_pest_data = self.con.execute("SELECT * FROM web_pest").fetchall()
        # updated_disease_data = self.con.execute("SELECT * FROM web_disease").fetchall()
        self.ui.time_label.setText(str(current_time.time())[:-7])
        self.ui.date_label.setText(str(current_time.date()))
        if updated_pest_data != self.pest_data:
            self.pest_data = updated_pest_data
            self.showNumber(self.pest_data, "pest")
            self.showPieChart(self.pest_data, "pest")

        # if updated_disease_data != self.disease_data:
        #     self.disease_data = updated_disease_data
        #     self.showNumber(self.disease_data, "disease")
        #     self.showPieChart(self.disease_data, "disease")

    def startTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.checkUpdate)
        self.timer.start(1000)

    def startSlideshowTimer(self):
        self.slideshow_timer = QtCore.QTimer()
        self.slideshow_timer.timeout.connect(self.updateGraphicView)
        self.slideshow_timer.start(5000)