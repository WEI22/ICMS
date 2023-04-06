import sys

import controller_ui
# import RobotCar
from PyQt5 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = controller_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # self.car = RobotCar.RobotCar()
        self.status = False
        self.speed = 25

        self.ui.button_on_off.clicked.connect(self.off)
        self.ui.button_up.clicked.connect(self.moveForward)
        self.ui.button_up.released.connect(self.off)
        self.ui.button_down.clicked.connect(self.moveBackward)
        self.ui.button_down.released.connect(self.off)
        self.ui.button_left.clicked.connect(self.moveLeft)
        self.ui.button_left.released.connect(self.off)
        self.ui.button_right.clicked.connect(self.moveRight)
        self.ui.button_right.clicked.connect(self.off)
        self.ui.speed_controller.valueChanged.connect(self.controlSpeed)

    def off(self):
        if self.status:
            print("Car Stop")
            self.status = False
            # self.car.stop()

    def moveForward(self):
        self.status = True
        print("Moving Forward")
        # self.car.forward()

    def moveBackward(self):
        self.status = True
        print("Moving Backward")
        # self.car.backward()

    def moveLeft(self):
        self.status = True
        print("Moving Left")
        # self.car.left()

    def moveRight(self):
        self.status = True
        print("Moving Right")
        # self.car.right()

    def controlSpeed(self):
        self.speed = self.ui.speed_controller.value()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    myapp = MainWindow()
    myapp.show()

    sys.exit(app.exec_())