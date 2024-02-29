from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import Qt
from ui import Camera
from core.PageWindow import PageWindow

import os
import sys
from datetime import datetime
import time
import subprocess
import sqlite3

sys.path.insert(0, r"C:\Users\limhong1\Downloads\ICMS\mindyolo")

from deploy.predict import detect
from deploy.infer_engine.mindir import MindIRModel

from mindyolo.utils import logger
from mindyolo.utils.utils import set_seed

import psycopg2
from psycopg2.extensions import Binary

import cv2
import numpy as np

from tools.utils import draw_result

seed = 2
conf_thres = 0.5
iou_thres = 0.65
conf_free = False
nms_time_limit = 60.0
img_size = 640
ms_mode = 0
ms_enable_graph_kernel = False
is_coco_dataset = True
single_cls = False

model_path = r"C:\Users\limhong1\Downloads\ICMS\mindyolo\weights\yolov7-tiny_300e_mAP375-d8972c94-c550e241.mindir"

class WindowCamera(PageWindow):

    def __init__(self, con, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Camera.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()

        self.setupLogoutMsgBox()

        self.ui.camera_capture.clicked.connect(self.capture)
        self.ui.sidebar_logout.clicked.connect(self.logout)
        self.ui.pest_detection_button.toggled.connect(lambda: self.btnChecked("pest"))
        self.ui.disease_detection_button.toggled.connect(lambda: self.btnChecked("disease"))

        self.con = con

        set_seed(seed)

        self.pest_infer = MindIRModel(model_path)
        # TODO: change to correct class
        self.pest_classes = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
           'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
           'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
           'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
           'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
           'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
           'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
           'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
           'hair drier', 'toothbrush' ]

        self.current_model = "pest"
        self.ui.pest_detection_button.setChecked(True)
        self.fps = 10
        self.cap = cv2.VideoCapture(0)
        time.sleep(1)

        self.isCapturing = False
        self.isDetecting = False

        self.duty_cycle = 5
        self.status = False

        self.start()

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        ret, frame = self.cap.read()

        if self.ui.camera_real.isChecked():
            self.isDetecting = True
            result_dict = detect(
                network=self.pest_infer,
                img=frame, 
                conf_thres=conf_thres,
                iou_thres=iou_thres,
                conf_free=conf_free,
                nms_time_limit=nms_time_limit,
                img_size=img_size,
                is_coco_dataset=is_coco_dataset
            )

            frame = draw_result(frame, 
                                result_dict,
                                self.pest_classes)

        elif not self.ui.camera_real.isChecked():
            self.isDetecting = False

        if self.isCapturing:
            today = datetime.now()
            saved_name = f"img_{datetime.strftime(today, '%d%m%y%H%M%S')}.jpg"
            # cv2.imwrite(f".\\saved\\original\\{saved_name}", frame)
            if self.current_model == "pest":
                saved_path = f"saved/pest/{saved_name}"
                cv2.imwrite(f"./saved/pest/original/{saved_name}", frame)
            # elif self.current_model == "disease":
            #     saved_path = f"saved/disease/{saved_name}"
            #     cv2.imwrite(f"./saved/disease/original/{saved_name}", frame)

            cur = self.con.cursor()
            if not self.isDetecting:
                result_dict = detect(
                    network=self.pest_infer,
                    img=frame, 
                    conf_thres=conf_thres,
                    iou_thres=iou_thres,
                    conf_free=conf_free,
                    nms_time_limit=nms_time_limit,
                    img_size=img_size,
                    is_coco_dataset=is_coco_dataset
                ) # boxes, scores, classes, valid_detections
                detected_img = draw_result(frame,
                                           result_dict,
                                           self.pest_classes)

            class_indexes = result_dict["category_id"]
            _, img_data = cv2.imencode('.jpg', frame)
            # binary_data = Binary(img_data) # for postgresql only

            # sql_query = f"INSERT INTO web_image VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" # for postgresql
            # sql_query = f"INSERT INTO web_image(pest, location, author, host, number, cum_num, image, image_data, date_created, time_created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            if self.current_model == "pest":
                classes = "\n".join([self.pest_classes[int(i)] for i in class_indexes])
                sql_query = f"INSERT INTO web_{self.current_model}(pest, location, author, host, number, cum_num, image, image_data, date_created, time_created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cur.execute(sql_query, (classes, "", 0, "", 0, 0, saved_path, img_data, str(today.date()), str(today.time())))
            # elif self.current_model == "disease":
            #     classes = "\n".join([self.disease_classes[int(i)] for i in class_indexes])
            #     sql_query = f"INSERT INTO web_{self.current_model}(disease, location, author, crop, number, image, image_data, date_created, time_created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            #     cur.execute(sql_query, (classes, "", 0, "", 0, saved_path, img_data, str(today.date()), str(today.time())))
            self.con.commit()
            cv2.imwrite(saved_path, frame)
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

    # def detect(self, frame):
    #     image_data = cv2.resize(frame, (416, 416))
    #     image_data = image_data / 255.
    #     image_data = image_data[np.newaxis, ...].astype(np.float32)

    #     batch_data = tf.constant(image_data)

    #     if self.current_model == "pest":
    #         model = self.pest_infer
    #         model_class = utils.read_class_names(PEST_CLASSES_PATH)
    #     elif self.current_model == "disease":
    #         model = self.disease_infer
    #         model_class = utils.read_class_names(DISEASE_CLASSES_PATH)
    #     pred_bbox = model(batch_data)

    #     for key, value in pred_bbox.items():
    #         boxes = value[:, :, 0:4]
    #         pred_conf = value[:, :, 4:]

    #     boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
    #         boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
    #         scores=tf.reshape(
    #             pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
    #         max_output_size_per_class=50,
    #         max_total_size=50,
    #         iou_threshold=0.45,
    #         score_threshold=0.25
    #     )

    #     pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
    #     frame = utils.draw_bbox(frame, pred_bbox, classes=model_class)
    #     return frame, pred_bbox

    def btnChecked(self, i):
        if i == "pest":
            self.ui.disease_detection_button.setChecked(False)
            self.current_model = "pest"
        elif i == "disease":
            self.ui.pest_detection_button.setChecked(False)
            # self.current_model = "disease"

    def off(self):
        if self.status:
            print("Car Stop")
            self.status = False
            # self.car.stop()
            # subprocess.run(['python', 'core/RobotCar.py', 'motor', 'stop'])

    def moveForward(self):
        self.status = True
        print("Moving Forward")
        # self.car.forward()
        # subprocess.run(['python', 'core/RobotCar.py', 'motor', 'forward'])

    def moveBackward(self):
        self.status = True
        print("Moving Backward")
        # self.car.backward()
        # subprocess.run(['python', 'core/RobotCar.py', 'motor', 'backward'])

    def moveLeft(self):
        self.status = True
        print("Moving Left")
        # self.car.left()
        # subprocess.run(['python', 'core/RobotCar.py', 'motor', 'left'])

    def moveRight(self):
        self.status = True
        print("Moving Right")
        # self.car.right()
        # subprocess.run(['python', 'core/RobotCar.py', 'motor', 'right'])

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_W or event.key() == Qt.Key_Up) and not event.isAutoRepeat():
            self.moveForward()
        elif (event.key() == Qt.Key_S or event.key() == Qt.Key_Down) and not event.isAutoRepeat():
            self.moveBackward()
        elif (event.key() == Qt.Key_A or event.key() == Qt.Key_Left) and not event.isAutoRepeat():
            self.moveLeft()
        elif (event.key() == Qt.Key_D or event.key() == Qt.Key_Right) and not event.isAutoRepeat():
            self.moveRight()

        elif event.key() == Qt.Key_Q and not event.isAutoRepeat():
            if 1 <= self.duty_cycle <= 10:
                self.duty_cycle -= 1
                # subprocess.run(['python', 'core/RobotCar.py', 'servo', '13', str(self.duty_cycle)])
            elif self.duty_cycle < 1:
                self.duty_cycle = 1
            elif self.duty_cycle > 10:
                self.duty_cycle = 10

        elif event.key() == Qt.Key_E and not event.isAutoRepeat():
            if 1 <= self.duty_cycle <= 10:
                self.duty_cycle += 1
                # subprocess.run(['python', 'core/RobotCar.py', 'servo', '13', str(self.duty_cycle)])
            elif self.duty_cycle < 1:
                self.duty_cycle = 1
            elif self.duty_cycle > 10:
                self.duty_cycle = 10

        elif event.key() == Qt.Key_Z and not event.isAutoRepeat():
            self.duty_cycle = 5
            # subprocess.run(['python', 'core/RobotCar.py', 'servo', '13', '5'])

    def keyReleaseEvent(self, event):
        forward_key = event.key() == Qt.Key_W or event.key() == Qt.Key_Up
        backward_key = event.key() == Qt.Key_S or event.key() == Qt.Key_Down
        left_key = event.key() == Qt.Key_A or event.key() == Qt.Key_Left
        right_key = event.key() == Qt.Key_D or event.key() == Qt.Key_Right
        if not event.isAutoRepeat() and (forward_key or backward_key or left_key or right_key):
            self.off()
