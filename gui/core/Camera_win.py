from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.Qt import Qt
from ui import Camera
from core.PageWindow import PageWindow
from core.Remote import Remote

import os
import sys
from datetime import datetime
import time
import subprocess
import sqlite3

sys.path.insert(0, r"C:\Users\User\Documents\UM\Year 4\Huawei Competition\project\mindyolo")

from deploy.predict import detect
from deploy.infer_engine.onnxruntime import ONNXRuntimeModel

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
is_coco_dataset = False
single_cls = False

model_path = r"C:\Users\User\Documents\UM\Year 4\Huawei Competition\project\mindyolo\weights\best-pest_detection.onnx"

class WindowCamera(PageWindow):

    def __init__(self, con, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Camera.Ui_Dialog()
        self.ui.setupUi(self)
        self.sidebar()

        self.setupLogoutMsgBox()

        self.ui.camera_capture.clicked.connect(self.capture)
        self.ui.sidebar_logout.clicked.connect(self.logout)
        # self.ui.pest_detection_button.toggled.connect(lambda: self.btnChecked("pest"))
        # self.ui.disease_detection_button.toggled.connect(lambda: self.btnChecked("disease"))

        self.con = con
        # self.ssh = Remote()

        set_seed(seed)

        self.pest_infer = ONNXRuntimeModel(model_path)
        # TODO: change to correct class
        # self.pest_classes = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        #    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        #    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        #    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
        #    'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
        #    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        #    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        #    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
        #    'hair drier', 'toothbrush' ]

        self.pest_classes = [ 'rice_leaf_roller', 'rice_leaf_caterpillar', 'paddy_stem_maggot', 'asiatic_rice_borer', 'yellow_rice_borer', 'rice_gall_midge', 'Rice_Stemfly', 'brown_plant_hopper',
           'white_backed_plant_hopper', 'small_brown_plant_hopper', 'rice_water_weevil', 'rice_leafhopper', 'grain_spreader_thrips', 'rice_shell_pest', 'grub', 'mole_cricket',
           'wireworm', 'white_margined_moth', 'black_cutworm', 'large_cutworm', 'yellow_cutworm', 'red_spider', 'corn_borer', 'army_worm',
           'aphids', 'Potosiabre_vitarsis', 'peach_borer', 'english_grain_aphid', 'green_bug', 'bird_cherry-oataphid', 'wheat_blossom_midge', 'penthaleus_major',
           'longlegged_spider_mite', 'wheat_phloeothrips', 'wheat_sawfly', 'cerodonta_denticornis', 'beet_fly', 'flea_beetle', 'cabbage_army_worm', 'beet_army_worm',
           'Beet_spot_flies', 'meadow_moth', 'beet_weevil', 'sericaorient_alismots_chulsky', 'alfalfa_weevil', 'flax_budworm', 'alfalfa_plant_bug', 'tarnished_plant_bug',
           'Locustoidea', 'lytta_polita', 'legume_blister_beetle', 'blister_beetle', 'therioaphis_maculata_Buckton', 'odontothrips_loti', 'Thrips', 'alfalfa_seed_chalcid',
           'Pieris_canidia', 'Apolygus_lucorum', 'Limacodidae', 'Viteus_vitifoliae', 'Colomerus_vitis', 'Brevipoalpus_lewisi_McGregor', 'oides_decempunctata', 'Polyphagotars_onemus_latus',
           'Pseudococcus_comstocki_Kuwana', 'parathrene_regalis', 'Ampelophaga', 'Lycorma_delicatula', 'Xylotrechus', 'Cicadella_viridis', 'Miridae', 'Trialeurodes_vaporariorum',
           'Erythroneura_apicalis', 'Papilio_xuthus', 'Panonchus_citri_McGregor', 'Phyllocoptes_oleiverus_ashmead', 'Icerya_purchasi_Maskell', 'Unaspis_yanonensis', 'Ceroplastes_rubens', 'Chrysomphalus_aonidum',
           'Parlatoria_zizyphus_Lucus', 'Nipaecoccus_vastalor', 'Aleurocanthus_spiniferus', 'Tetradacus_c_Bactrocera_minax', 'Dacus_dorsalis(Hendel)', 'Bactrocera_tsuneonis', 'Prodenia_litura', 'Adristyrannus',
           'Phyllocnistis_citrella_Stainton', 'Toxoptera_citricidus', 'Toxoptera_aurantii', 'Aphis_citricola_Vander_Goot', 'Scirtothrips_dorsalis_Hood', 'Dasineura_sp', 'Lawana_imitata_Melichar', 'Salurnis_marginella_Guerr',
           'Deporaus_marginatus_Pascoe', 'Chlumetia_transversa', 'Mango_flat_beak_leafhopper', 'Rhytidodera_bowrinii_white', 'Sternochetus_frigidus', 'Leafhoppers' ]

        # self.current_model = "pest"
        # self.ui.pest_detection_button.setChecked(True)
        self.fps = 1000
        # self.cap = cv2.VideoCapture("http:192.168.100.86:8000/stream.mjpg")
        self.cap = cv2.VideoCapture(0)
        time.sleep(1)

        self.isCapturing = False
        self.isDetecting = False

        self.pan_servo = 19
        self.tilt_servo = 12

        self.pan_angle = 90
        self.tilt_angle = 90

        self.status = False

        self.start()

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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
                                self.pest_classes,
                                is_coco_dataset)

        elif not self.ui.camera_real.isChecked():
            self.isDetecting = False

        if self.isCapturing:
            today = datetime.now()
            saved_name = f"img_{datetime.strftime(today, '%d%m%y%H%M%S')}.jpg"
            # cv2.imwrite(f".\\saved\\original\\{saved_name}", frame)
            # if self.current_model == "pest":
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
                                           self.pest_classes,
                                           is_coco_dataset)

            class_indexes = result_dict["category_id"]
            _, img_data = cv2.imencode('.jpg', frame)
            # binary_data = Binary(img_data) # for postgresql only

            # sql_query = f"INSERT INTO web_image VALUES(DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" # for postgresql
            # sql_query = f"INSERT INTO web_image(pest, location, author, host, number, cum_num, image, image_data, date_created, time_created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            # if self.current_model == "pest":
            classes = "\n".join([self.pest_classes[int(i)] for i in class_indexes])
            sql_query = f"INSERT INTO web_pest(pest, location, author, host, number, cum_num, image, image_data, date_created, time_created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
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

    # def btnChecked(self, i):
    #     self.ui.disease_detection_button.setChecked(False)
        # self.current_model = "pest"
        # elif i == "disease":
        #     self.ui.pest_detection_button.setChecked(False)
            # self.current_model = "disease"

    def off(self):
        if self.status:
            print("Car Stop")
            self.status = False
            self.ssh.run_command("python robot_car.py motor stop")
            # self.car.stop()
            # subprocess.run(['python', 'core/RobotCar.py', 'motor', 'stop'])

    def moveForward(self):
        self.status = True
        print("Moving Forward")
        self.ssh.run_command("python robot_car.py motor forward")
        # self.car.forward()
        # subprocess.run(['python', 'core/RobotCar.py', 'motor', 'forward'])

    def moveBackward(self):
        self.status = True
        print("Moving Backward")
        self.ssh.run_command("python robot_car.py motor backward")
        # self.car.backward()
        # subprocess.run(['python', 'core/RobotCar.py', 'motor', 'backward'])

    def moveLeft(self):
        self.status = True
        print("Moving Left")
        self.ssh.run_command("python robot_car.py motor left")

        # self.car.left()
        # subprocess.run(['python', 'core/RobotCar.py', 'motor', 'left'])

    def moveRight(self):
        self.status = True
        print("Moving Right")
        self.ssh.run_command("python robot_car.py motor right")

        # self.car.right()
        # subprocess.run(['python', 'core/RobotCar.py', 'motor', 'right'])

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_W) and not event.isAutoRepeat():
            self.moveForward()

        elif (event.key() == Qt.Key_S) and not event.isAutoRepeat():
            self.moveBackward()

        elif (event.key() == Qt.Key_A) and not event.isAutoRepeat():
            self.moveLeft()

        elif (event.key() == Qt.Key_D) and not event.isAutoRepeat():
            self.moveRight()

        elif (event.key() == Qt.Key_Space) and not event.isAutoRepeat():
            self.ssh.run_command("python robot_car.py motor stop")

        elif (event.key() == Qt.Key_I) and not event.isAutoRepeat():
            self.tilt_angle -= 10
            if self.tilt_angle <= 30:
               self.tilt_angle = 30
            self.ssh.run_command(f"python robot_car.py servo {self.tilt_servo} {self.tilt_angle}")

        elif (event.key() == Qt.Key_K) and not event.isAutoRepeat():
            self.tilt_angle += 10
            if self.tilt_angle >= 150:
                self.tilt_angle = 150
            self.ssh.run_command(f"python robot_car.py servo {self.tilt_servo} {self.tilt_angle}")

        elif (event.key() == Qt.Key_J) and not event.isAutoRepeat():
            self.pan_angle += 10
            if self.pan_angle >= 180:
                self.pan_angle = 18
            self.ssh.run_command(f"python robot_car.py servo {self.pan_servo} {self.pan_angle}")

        elif (event.key() == Qt.Key_L) and not event.isAutoRepeat():
            self.pan_angle -= 10
            if self.pan_angle <= 18:
                self.pan_angle = 18
            self.ssh.run_command(f"python robot_car.py servo {self.pan_servo} {self.pan_angle}")

    def keyReleaseEvent(self, event):
        forward_key = event.key() == Qt.Key_W or event.key() == Qt.Key_Up
        backward_key = event.key() == Qt.Key_S or event.key() == Qt.Key_Down
        left_key = event.key() == Qt.Key_A or event.key() == Qt.Key_Left
        right_key = event.key() == Qt.Key_D or event.key() == Qt.Key_Right
        if not event.isAutoRepeat() and (forward_key or backward_key or left_key or right_key):
            self.off()
