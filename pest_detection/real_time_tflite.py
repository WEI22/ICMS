import time
import tensorflow as tf

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS

import sys
sys.path.insert(0, r"/home/pi/ICMS/tools/tensorflow-yolov4-tflite")

import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
from picamera2 import Picamera2
import time

def main(_argv):
    camera = Picamera2()
    camera.video_configuration.main.format = "BGR888"
    camera.configure("video")
    camera.start()
    time.sleep(1)
    
    interpreter = tf.lite.Interpreter(model_path=r"/home/pi/ICMS/pest_detection/tensorflow_lite_weights/yolov4-fp32.tflite")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print(input_details)
    print(output_details)
    
    frame_id = 0
    while True:
        frame = camera.capture_array("main")

        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (416, 416))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        prev_time = time.time()

        interpreter.set_tensor(input_details[0]['index'], image_data)
        interpreter.invoke()
        pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
        boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25, input_shape=tf.constant([416, 416]))

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
        image = utils.draw_bbox(frame, pred_bbox)
        curr_time = time.time()
        exec_time = curr_time - prev_time
        result = np.asarray(image)
        info = "time: %.2f ms" % (1000 * exec_time)
        print(info)

        result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("result", result)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

        frame_id += 1


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
