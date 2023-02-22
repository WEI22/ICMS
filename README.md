# ICMS
Intelligence Crop Monitoring System

# Yolo (Pest detection)

1. Train custom datasets [link](https://medium.com/analytics-vidhya/train-a-custom-yolov4-tiny-object-detector-using-google-colab-b58be08c9593)
2. Convert to tensorflow framework using [tensorflow-yolov4-tflite](https://github.com/hunglc007/tensorflow-yolov4-tflite)

## Useful commands
```
python save_model.py --weights ./data/yolov4-tiny.weights --output ./checkpoints/yolov4-tiny-416 --input_size 416 --model yolov4 --tiny

python detect.py --weights ./checkpoints/yolov4-tiny-416 --size 416 --model yolov4 --image ./data/kite.jpg --tiny

```
# SSD (Crop disease)

# Credits

## References
* [TRAIN A CUSTOM YOLOv4-tiny OBJECT DETECTOR USING GOOGLE COLAB](https://medium.com/analytics-vidhya/train-a-custom-yolov4-tiny-object-detector-using-google-colab-b58be08c9593)
* [darknet](https://github.com/AlexeyAB/darknet#yolo-v4-in-other-frameworks)
* [tensorflow-yolov4-tflite](https://github.com/hunglc007/tensorflow-yolov4-tflite)

## Datasets
* [yolo-custome-925](https://universe.roboflow.com/nirmani/yolo-custome-925)
