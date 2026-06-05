import os, shutil
from sklearn.model_selection import train_test_split
from ultralytics import YOLO

DATA_DIR = "../../dataset"
YOLO_DATA_DIR = "../yolo_dataset"
MODEL_SAVE_DIR = "../backend/app/ml"

class_names = ["fake", "real"]
paths, labels = [], []

for label, name in enumerate(class_names):
    for base in ["", "synthetic"]:
        folder = os.path.join(DATA_DIR, base, name) if base else os.path.join(DATA_DIR, name)
        if not os.path.isdir(folder):
            continue
        for f in os.listdir(folder):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                paths.append(os.path.join(folder, f))
                labels.append(label)

train_p, test_p, train_l, test_l = train_test_split(paths, labels, test_size=0.15, random_state=42, stratify=labels)
train_p, val_p, train_l, val_l = train_test_split(train_p, train_l, test_size=0.15, random_state=42, stratify=train_l)

if os.path.exists(YOLO_DATA_DIR):
    shutil.rmtree(YOLO_DATA_DIR)

for split, sp, sl in [("train", train_p, train_l), ("val", val_p, val_l), ("test", test_p, test_l)]:
    for p, l in zip(sp, sl):
        d = os.path.join(YOLO_DATA_DIR, split, class_names[l], os.path.basename(p))
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(p, d)

print(f"Train: {len(train_p)}, Val: {len(val_p)}, Test: {len(test_p)}")

model = YOLO("yolov8n-cls.pt")

results = model.train(
    data=YOLO_DATA_DIR,
    epochs=3,
    imgsz=128,
    batch=16,
    device="cpu",
    seed=42,
    project=MODEL_SAVE_DIR,
    name="yolo_model",
    exist_ok=True,
    verbose=True,
    plots=False,
    val=True,
    cos_lr=False,
    mixup=0.0,
    copy_paste=0.0,
    erasing=0.0,
    crop_fraction=1.0,
    hsv_h=0.0,
    hsv_s=0.0,
    hsv_v=0.0,
    degrees=0.0,
    translate=0.0,
    scale=0.0,
    shear=0.0,
    perspective=0.0,
    flipud=0.0,
    fliplr=0.0,
    mosaic=0.0,
    auto_augment=None,
)

val = model.val()
print(f"\nTop-1 Accuracy: {val.top1:.4f}")

model.save(os.path.join(MODEL_SAVE_DIR, "yolo_cls.pt"))
print(f"Model saved: {os.path.join(MODEL_SAVE_DIR, 'yolo_cls.pt')}")
