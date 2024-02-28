import os
import sys
import cv2
import numpy as np
from datetime import datetime

from mindspore import context

from mindyolo.utils import logger
from mindyolo.utils.utils import set_seed
from deploy.predict import detect

sys.path.insert(0, r"C:\Users\User\Documents\UM\Year 4\Huawei Competition\project\mindyolo")

seed = 2
conf_thres = 0.25
iou_thres = 0.65
conf_free = False
nms_time_limit = 60.0
img_size = 640
ms_mode = 0
ms_enable_graph_kernel = False
is_coco_dataset = True
single_cls = False

# FIXME: change to correct number of classes
num_class = 80
class_names = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
           'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
           'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
           'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
           'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
           'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
           'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
           'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
           'hair drier', 'toothbrush' ]

config = r"C:\Users\User\Documents\UM\Year 4\Huawei Competition\project\mindyolo\configs\yolov7\yolov7-tiny.yaml"
model_type = "MindIR"
model_path = r"C:\Users\User\Documents\UM\Year 4\Huawei Competition\project\mindyolo\weights\yolov7-tiny_300e_mAP375-d8972c94-c550e241.mindir"
device_target = "CPU"

save_dir_path = r"./runs_infer"

def set_default_infer():
    # Set Context
    context.set_context(mode=ms_mode, device_target=device_target, max_call_depth=2000)
    if device_target == "Ascend":
        context.set_context(device_id=int(os.getenv("DEVICE_ID", 0)))
    elif device_target == "GPU" and ms_enable_graph_kernel:
        context.set_context(enable_graph_kernel=True)
    rank, rank_size = 0, 1
    # Set Data
    nc = 1 if single_cls else int(num_class)  # number of classes
    names = ["item"] if single_cls and len(class_names) != 1 else class_names  # class names
    assert len(class_names) == nc, "%g names found for nc=%g dataset in %s" % (
        len(class_names),
        nc,
        config,
    )
    # Directories and Save run settings
    save_dir = os.path.join(save_dir_path, datetime.now().strftime("%Y.%m.%d-%H:%M:%S"))
    os.makedirs(save_dir, exist_ok=True)
    # if rank % rank_size == 0:
    #     with open(os.path.join(save_dir, "cfg.yaml"), "w") as f:
    #         yaml.dump(vars(args), f, sort_keys=False)
    # Set Logger
    logger.setup_logging(logger_name="MindYOLO", log_level="INFO", rank_id=rank, device_per_servers=rank_size)
    logger.setup_logging_file(log_dir=os.path.join(save_dir, "logs"))

def draw_result(im, result_dict, data_names, is_coco_dataset=True):
    import random
    import cv2
    from mindyolo.data import COCO80_TO_COCO91_CLASS

    category_id, bbox, score = result_dict["category_id"], result_dict["bbox"], result_dict["score"]
    seg = result_dict.get("segmentation", None)
    mask = None if seg is None else np.zeros_like(im, dtype=np.float32)
    for i in range(len(bbox)):
        # draw box
        x_l, y_t, w, h = bbox[i][:]
        x_r, y_b = x_l + w, y_t + h
        x_l, y_t, x_r, y_b = int(x_l), int(y_t), int(x_r), int(y_b)
        _color = [random.randint(0, 255) for _ in range(3)]
        cv2.rectangle(im, (x_l, y_t), (x_r, y_b), tuple(_color), 2)
        if seg:
            _color_seg = np.array([random.randint(0, 255) for _ in range(3)], np.float32)
            mask += seg[i][:, :, None] * _color_seg[None, None, :]

        # draw label
        if is_coco_dataset:
            class_name_index = COCO80_TO_COCO91_CLASS.index(category_id[i])
        else:
            class_name_index = category_id[i]
        class_name = data_names[class_name_index]  # args.data.names[class_name_index]
        text = f"{class_name}: {score[i]}"
        (text_w, text_h), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(im, (x_l, y_t - text_h - baseline), (x_l + text_w, y_t), tuple(_color), -1)
        cv2.putText(im, text, (x_l, y_t - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # save results
    if seg:
        im = (0.7 * im + 0.3 * mask).astype(np.uint8)

    return im

def main():

    set_seed(seed)

    vid = cv2.VideoCapture(0)

    if model_type == "MindX":
        from deploy.infer_engine.mindx import MindXModel
        network = MindXModel(model_path)
    elif model_type == "Lite":
        from deploy.infer_engine.lite import LiteModel
        network = LiteModel(model_path)
    elif model_type == "MindIR":
        from deploy.infer_engine.mindir import MindIRModel
        network = MindIRModel(model_path)
    elif model_type == "ONNX":
        from deploy.infer_engine.onnxruntime import ONNXRuntimeModel
        network = ONNXRuntimeModel(model_path)
    else:
        raise TypeError("the type only supposed MindX/Lite/MindIR/ONNX")


    while True:
        ret, frame = vid.read()

        result_dict = detect(
            network=network,
            img=frame,
            conf_thres=conf_thres,
            iou_thres=iou_thres,
            conf_free=conf_free,
            nms_time_limit=nms_time_limit,
            img_size=img_size,
            is_coco_dataset=is_coco_dataset
        )

        predicted_frame = draw_result(frame, result_dict, class_names)

        cv2.imshow("frame", predicted_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

