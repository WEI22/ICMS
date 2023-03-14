# ICMS
Intelligence Crop Monitoring System

# Yolo (Pest detection)

Colab: [link](https://colab.research.google.com/drive/1s9fJ6iinkrNUkYxBil2mZuapegFuX0I7?usp=sharing)

1. Train custom datasets [link](https://medium.com/analytics-vidhya/train-a-custom-yolov4-tiny-object-detector-using-google-colab-b58be08c9593)
2. Convert to tensorflow framework using [tensorflow-yolov4-tflite](https://github.com/hunglc007/tensorflow-yolov4-tflite)
3. Copy the corrected version of [utils.py](pest_detection/utils.py) to ./tensorflow-yolov4-tflite/core/

## Useful commands
```
python save_model.py --weights ./data/yolov4-tiny.weights --output ./checkpoints/yolov4-tiny-416 --input_size 416 --model yolov4 --tiny

python detect.py --weights ./checkpoints/yolov4-tiny-416 --size 416 --model yolov4 --image ./data/kite.jpg --tiny

```
# MobileNet SSD v2 (Crop disease)

Colab: 1. [Yolo](https://colab.research.google.com/drive/1x9S9S_i2aMch_nu5KkL-a_TUmHIQCZhq?usp=sharing)
       2. [SSD](https://colab.research.google.com/drive/1LlZ4-69XQk1XzIrjd7hI5QX1RCxKdbg-?usp=sharing)

1. Train custom datasets [link](https://medium.com/analytics-vidhya/training-a-model-for-custom-object-detection-tf-2-x-on-google-colab-4507f2cc6b80#6dfc)
2. Deploy the model (In progress)

# Website

Make sure Django has been installed

```
pip install Django
```

To launch server:

```
python manage.py runserver
```

# GUI

Make sure PyQt5, Pillow, passlib has been installed

```
pip install PyQt5 passlib Pillow
```

To launch:

```
python main.py
```

# Credits

## References
* [TRAIN A CUSTOM YOLOv4-tiny OBJECT DETECTOR USING GOOGLE COLAB](https://medium.com/analytics-vidhya/train-a-custom-yolov4-tiny-object-detector-using-google-colab-b58be08c9593)
* [darknet](https://github.com/AlexeyAB/darknet#yolo-v4-in-other-frameworks)
* [tensorflow-yolov4-tflite](https://github.com/hunglc007/tensorflow-yolov4-tflite)
* [Training a model for custom object detection (TF 2.x) on Google Colab](https://medium.com/analytics-vidhya/training-a-model-for-custom-object-detection-tf-2-x-on-google-colab-4507f2cc6b80#6dfc)
* [Tensorflow Object Detection API](https://github.com/tensorflow/models/)

## Datasets
* [yolo-custome-925](https://universe.roboflow.com/nirmani/yolo-custome-925)
* [PlantDoc](https://universe.roboflow.com/joseph-nelson/plantdoc)
