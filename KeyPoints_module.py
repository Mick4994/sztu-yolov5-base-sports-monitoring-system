from utils.torch_utils import select_device
from utils.general import check_img_size
from utils.datasets import LoadWebcam
from utils.val import run_nms, post_process_batch

from models.experimental import attempt_load

import torch
import yaml

class Process_keyPoint:
    def __init__(self, args) -> None:
        self.poses = []
        self.bboxes = []
        self.device = 0
        self.imgsz = 512
        self.camera_index = args.source
        self.frame = []
        self.weights = 'kapao_s_coco.pt'
        self.state = False

    def main(self):
        
        with open('data/coco-kp.yaml') as f:
            data = yaml.safe_load(f) 

        data['imgsz'] = self.imgsz
        data['conf_thres'] = 0.5
        data['iou_thres'] = 0.45
        data['use_kp_dets'] = False
        data['conf_thres_kp'] = 0.5
        data['iou_thres_kp'] = 0.45
        data['conf_thres_kp_person'] = 0.2
        data['overwrite_tol'] = 50
        data['scales'] = [1]
        data['flips'] = [None if f == -1 else f for f in [-1]]
        data['count_fused'] = False

        device = select_device(self.device, batch_size=1)
        print('Using device: {}'.format(device))

        model = attempt_load(self.weights, map_location=device)  # load FP32 model
        model.half() # half precision only supported on CUDA
        stride = int(model.stride.max())  # model stride

        imgsz = check_img_size(self.imgsz, s=stride)  # check image size
        dataset = LoadWebcam(self.camera_index, img_size=imgsz, stride=stride)

        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once

        print('finished start')
        self.state = True

        for i, (path, img, im0, _) in enumerate(dataset):
            img = torch.from_numpy(img).to(device)
            img = img.half()  # uint8 to fp16/32
            img = img / 255.0  # 0 - 255 to 0.0 - 1.0
            if len(img.shape) == 3:
                img = img[None]  # expand for batch dim

            out = model(img, augment=True, kp_flip=data['kp_flip'], scales=data['scales'], flips=data['flips'])[0]
            person_dets, kp_dets = run_nms(data, out)
            bboxes, poses, _, _, _ = post_process_batch(data, img, [], [[im0.shape[:2]]], person_dets, kp_dets)

            # print(poses)
            self.frame = im0.copy()
            self.bboxes = bboxes
            self.poses = poses

if __name__ == "__main__":
    import threading
    import time
    keypoint_process = Process_keyPoint()
    main_thread = threading.Thread(target=keypoint_process.main,daemon=True)
    main_thread.start()
    time.sleep(10)
    while main_thread.is_alive():
        print(keypoint_process.bboxes)
        time.sleep(1)
