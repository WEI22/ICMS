import sys

import controller_ui
import RobotCar
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.Qt import Qt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = controller_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.car = RobotCar.RobotCar()
        self.status = False

        self.ui.button_on_off.clicked.connect(self.off)

        self.ui.button_up.clicked.connect(self.moveForward)
        self.ui.button_up.released.connect(self.off)

        self.ui.button_down.clicked.connect(self.moveBackward)
        self.ui.button_down.released.connect(self.off)

        self.ui.button_left.clicked.connect(self.moveLeft)
        self.ui.button_left.released.connect(self.off)

        self.ui.button_right.clicked.connect(self.moveRight)
        self.ui.button_right.released.connect(self.off)

    def off(self):
        if self.status:
            print("Car Stop")
            self.status = False
            self.car.stop()

    def moveForward(self):
        self.status = True
        print("Moving Forward")
        self.car.forward()

    def moveBackward(self):
        self.status = True
        print("Moving Backward")
        self.car.backward()

    def moveLeft(self):
        self.status = True
        print("Moving Left")
        self.car.left()

    def moveRight(self):
        self.status = True
        print("Moving Right")
        self.car.right()

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_W or event.key() == Qt.Key_Up) and not event.isAutoRepeat():
            self.moveForward()
        elif (event.key() == Qt.Key_S or event.key() == Qt.Key_Down) and not event.isAutoRepeat():
            self.moveBackward()
        elif (event.key() == Qt.Key_A or event.key() == Qt.Key_Left) and not event.isAutoRepeat():
            self.moveLeft()
        elif (event.key() == Qt.Key_D or event.key() == Qt.Key_Right) and not event.isAutoRepeat():
            self.moveRight()

    def keyReleaseEvent(self, event):
        forward_key = event.key() == Qt.Key_W or event.key() == Qt.Key_Up
        backward_key = event.key() == Qt.Key_S or event.key() == Qt.Key_Down
        left_key = event.key() == Qt.Key_A or event.key() == Qt.Key_Left
        right_key = event.key() == Qt.Key_D or event.key() == Qt.Key_Right
        if not event.isAutoRepeat() and (forward_key or backward_key or left_key or right_key):
            self.off()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    myapp = MainWindow()
    myapp.show()

    sys.exit(app.exec_())
