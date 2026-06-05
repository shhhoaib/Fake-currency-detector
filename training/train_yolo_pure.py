import os, sys, shutil, warnings, logging
warnings.filterwarnings('ignore')
logging.disable(logging.CRITICAL)
os.environ['POLARS_SKIP_CPU_CHECK'] = '1'

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
from sklearn.model_selection import train_test_split
from ultralytics import YOLO as YOLO_UL

DATA_DIR = "../../dataset"
YOLO_DATA_DIR = "../yolo_dataset_mini"
MODEL_SAVE_DIR = "../backend/app/ml"
IMG_SIZE = 128
BATCH_SIZE = 16
EPOCHS = 5
LR = 0.001


class ImageFolderDataset(Dataset):
    def __init__(self, base_dir, class_names=None):
        self.samples = []
        if class_names is None:
            class_names = sorted(os.listdir(base_dir))
        self.class_names = class_names
        self.class_to_idx = {n: i for i, n in enumerate(class_names)}
        for class_name in class_names:
            class_dir = os.path.join(base_dir, class_name)
            if not os.path.isdir(class_dir):
                continue
            for fname in os.listdir(class_dir):
                if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.samples.append((os.path.join(class_dir, fname), self.class_to_idx[class_name]))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = Image.open(path).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
        arr = np.array(img, dtype=np.float32) / 255.0
        arr = (arr - 0.5) / 0.5
        arr = arr.transpose(2, 0, 1)
        return torch.tensor(arr, dtype=torch.float32), label


def main():
    print("=" * 60)
    print("PakShield AI - YOLOv8 Pure PyTorch Training")
    print("=" * 60)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    yolo_model = YOLO_UL("yolov8n-cls.pt")
    model = yolo_model.model
    model.eval()

    in_features = model.model[9].linear.in_features if hasattr(model.model[9], 'linear') else 256
    model.model[9] = nn.Sequential(
        nn.Linear(in_features, 128),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(128, 2),
    )
    model = model.to(device)

    train_dataset = ImageFolderDataset(os.path.join(YOLO_DATA_DIR, "train"))
    val_dataset = ImageFolderDataset(os.path.join(YOLO_DATA_DIR, "val"))

    train_loader = DataLoader(train_dataset, BATCH_SIZE, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, BATCH_SIZE, num_workers=0)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

    best_acc = 0.0
    for epoch in range(1, EPOCHS + 1):
        model.train()
        tl, tc, tt = 0.0, 0, 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()
            tl += loss.item() * images.size(0)
            tc += (model(images).argmax(1) == labels).sum().item()
            tt += labels.size(0)
        tle, tae = tl / tt, tc / tt

        model.eval()
        vl, vc, vt = 0.0, 0, 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                out = model(images)
                vl += criterion(out, labels).item() * images.size(0)
                vc += (out.argmax(1) == labels).sum().item()
                vt += labels.size(0)
        vle, vae = vl / vt, vc / vt
        print(f"Epoch {epoch}/{EPOCHS} - Loss: {tle:.4f} Acc: {tae:.4f} | Val Loss: {vle:.4f} Val Acc: {vae:.4f}")

        if vae > best_acc:
            best_acc = vae
            traced = torch.jit.trace(model.cpu(), torch.randn(1, 3, IMG_SIZE, IMG_SIZE))
            os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
            traced.save(os.path.join(MODEL_SAVE_DIR, "yolo_cls.pt"))
            print(f"  -> Saved (val_acc={vae:.4f})")
            model = model.to(device)

    print(f"\nBest val acc: {best_acc:.4f}")
    size = os.path.getsize(os.path.join(MODEL_SAVE_DIR, "yolo_cls.pt"))
    print(f"Final model: {os.path.join(MODEL_SAVE_DIR, 'yolo_cls.pt')} ({size} bytes)")
    print("Done!")


if __name__ == "__main__":
    main()
