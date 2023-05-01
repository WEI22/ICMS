from PyQt5 import QtWidgets, QtGui, QtCore
from core import PageWindow
import os
import sys
from collections import Counter
from core.clickableLabel import ClickableLabel

CURRENT_DIR = os.getcwd()
BASE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BASE_DIR)

from ui import Record

class WindowRecord(PageWindow.PageWindow):
    def __init__(self, con, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Record.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()

        self.setupLogoutMsgBox()
        self.con = con
        self.current_table = "web_pest"

        self.ui.sidebar_logout.clicked.connect(self.logout)
        self.ui.record_search_btn.clicked.connect(self.search)
        self.ui.record_search.returnPressed.connect(self.search)
        self.ui.table_combobox.currentIndexChanged.connect(self.changeTable)

        self.data = self.con.execute("SELECT * FROM web_pest").fetchall()

        self.ui.table.setColumnWidth(0, 200)
        self.ui.table.setColumnWidth(1, 200)
        self.ui.table.setColumnWidth(2, 200)
        self.ui.table.setColumnWidth(3, 200)
        self.ui.table.setColumnWidth(4, 75)

        self.updateTable()
        self.startTimer()

    def updateTable(self):
        self.ui.table.setRowCount(len(self.data))

        for n, i in enumerate(self.data):
            image_item = self.getImageLabel(i[-3])
            time_item = QtWidgets.QTableWidgetItem(f"{i[-2]}\n{i[-1][:-7]}")
            pest = Counter(i[1].split(","))
            pest.pop("")
            pest = [f"{key} x{value}" for key, value in pest.items()]
            pest = "\n".join(pest)
            item = QtWidgets.QTableWidgetItem(pest)
            location_item = QtWidgets.QTableWidgetItem(i[2])
            delete_item = self.getItemLabel(i[0], i[-4])

            self.ui.table.setCellWidget(n, 0, image_item)
            self.ui.table.setItem(n, 1, time_item)
            self.ui.table.setItem(n, 2, item)
            self.ui.table.setItem(n, 3, location_item)
            self.ui.table.setCellWidget(n, 4, delete_item)

        self.ui.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.table.resizeRowsToContents()

    def getImageLabel(self, image):
        image_label = ClickableLabel(self)
        image_label.setText("")
        image_label.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image, 'jpg')
        pixmap = pixmap.scaled(200, 100, QtCore.Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        image_label.clicked.connect(lambda: self.showFullImage(image))
        return image_label

    def getItemLabel(self, index, image_path):
        item_label = ClickableLabel(self)
        item_label.setText("")
        item_label.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = QtGui.QPixmap(r"src/img/user/delete.png")
        item_label.clicked.connect(lambda: self.showDeleteDialog(index, image_path))
        item_label.setPixmap(pixmap)
        item_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        return item_label

    def showFullImage(self, image):
        dialog = QtWidgets.QDialog()
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image, 'jpg')
        label.setPixmap(pixmap)
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.setWindowTitle("image")
        dialog.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        dialog.exec_()

    def showDeleteDialog(self, index, image_path):
        delete_msgbox = QtWidgets.QMessageBox()
        delete_msgbox.setWindowTitle("Delete")
        delete_msgbox.setText("Are you sure?")
        delete_msgbox.setIcon(QtWidgets.QMessageBox.Question)
        delete_msgbox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        delete_msgbox.setDefaultButton(QtWidgets.QMessageBox.No)
        respond = delete_msgbox.exec_()
        if respond == QtWidgets.QMessageBox.Yes:
            dirname = os.path.dirname(image_path)
            basename = os.path.basename(image_path)
            original_image_path = os.path.join(dirname, "original", basename)
            os.remove(image_path)
            os.remove(original_image_path)
            self.con.execute(f"DELETE FROM {self.current_table} WHERE id={index}")
            self.con.commit()

    def checkUpdate(self):
        if self.current_table == "web_pest":
            updated_data = self.con.execute("SELECT * FROM web_pest").fetchall()
        elif self.current_table == "web_disease":
            updated_data = self.con.execute("SELECT * FROM web_disease").fetchall()
        if updated_data != self.data:
            self.data = updated_data
            self.updateTable()

    def startTimer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.checkUpdate)
        self.timer.start(2000)

    def stopTimer(self):
        self.timer.stop()

    def search(self):
        search_text = self.ui.record_search.text()
        results = list(filter(lambda x: search_text in x[1], self.data))
        self.updateTable(results)

    def changeTable(self, index):
        if index == 0:
            self.current_table = "web_pest"
            self.ui.record_title.setText("Pest Record")
            self.data = self.con.execute("SELECT * FROM web_pest").fetchall()
        elif index == 1:
            self.current_table = "web_disease"
            self.ui.record_title.setText("Disease Record")
            self.data = self.con.execute("SELECT * FROM web_disease").fetchall()
        self.updateTable()
