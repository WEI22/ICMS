from PyQt5 import QtWidgets, QtGui, QtCore
import os
import sys

CURRENT_DIR = os.getcwd()
BASE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, BASE_DIR)
from core.PageWindow import PageWindow

MODEL_PATH = r"C:\Users\User\Documents\UM\Year 3\Sem 1\KIX2001\Crop Monitoring System\pest_detection\yolov4_tiny\checkpoints"

import tools.utils as utils
from tools.yolov4 import filter_boxes

from ui import Home
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.python.saved_model import tag_constants

class WindowHome(PageWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Home.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()

        self.ui.camera_capture.clicked.connect(self.capture)
        
        self.model = tf.saved_model.load(MODEL_PATH, tags=[tag_constants.SERVING])
        self.infer = self.model.signatures['serving_default']

        self.fps = 10
        self.cap = cv2.VideoCapture(0)

        self.isCapturing = False
        self.isDetecting = False
        self.ith_frame = 1

        self.start()

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        ret, frame = self.cap.read()

        if self.ui.camera_real.isChecked():
            print("hi")
            image_data = cv2.resize(frame, (416, 416))
            image_data = image_data / 255.
            image_data = image_data[np.newaxis, ...].astype(np.float32)

            batch_data = tf.constant(image_data)
            pred_bbox = self.infer(batch_data)

            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

            boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
                boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
                scores=tf.reshape(
                    pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
                max_output_size_per_class=50,
                max_total_size=50,
                iou_threshold=0.45,
                score_threshold=0.25
            )

            pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
            frame = utils.draw_bbox(frame, pred_bbox)

        if self.isCapturing:
            cv2.imwrite('img_%05d.jpg' % self.ith_frame, frame)
            self.ith_frame += 1
            self.isCapturing = False

        # My webcam yields frames in BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.ui.camera_video.setPixmap(pix)

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000 // self.fps)

    def stop(self):
        self.timer.stop()

    def capture(self):
        if not self.isCapturing:
            self.isCapturing = True
        else:
            self.isCapturing = False

    def deleteLater(self):
        self.cap.release()
        super(QtWidgets.QWidget, self).deleteLater()

    def detection(self):
        if not self.ui.camera_real.isChecked():
            self.isDetecting = True
        else:
            self.isDetecting = False

if __name__ == '__main__':
    app = QtGui.QGuiApplication(sys.argv)
    window = WindowHome()
    sys.exit(app.exec_())
