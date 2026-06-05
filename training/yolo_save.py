"""Script that trains YOLO for 1 epoch and saves immediately after training completes."""
import os, sys, warnings, logging
os.environ['POLARS_SKIP_CPU_CHECK'] = '1'
warnings.filterwarnings('ignore')
logging.disable(logging.CRITICAL)

import torch
from ultralytics import YOLO

model = YOLO('yolov8n-cls.pt')
model.train(
    data='../yolo_dataset_mini', epochs=1, imgsz=128, batch=16,
    device='cpu', seed=42,
    verbose=False, plots=False, workers=0,
    save=True, save_period=1,
    project='../backend/app/ml', name='yolo_train',
)

model.model.eval()
scripted = torch.jit.script(model.model)
scripted.save('../backend/app/ml/yolo_cls.pt')
size = os.path.getsize('../backend/app/ml/yolo_cls.pt')
print(f'OK:{size}', flush=True)
