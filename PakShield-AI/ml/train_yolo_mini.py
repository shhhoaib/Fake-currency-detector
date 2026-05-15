import os, shutil
from sklearn.model_selection import train_test_split
from ultralytics import YOLO

DATA_DIR = "../../dataset"
YOLO_DATA_DIR = "../yolo_dataset_mini"
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
    epochs=1,
    imgsz=128,
    batch=16,
    device="cpu",
    seed=42,
    project=MODEL_SAVE_DIR,
    name="yolo_model",
    exist_ok=True,
    verbose=False,
    plots=False,
    deterministic=True,
    workers=0,
)

val = model.val()
print(f"\nTop-1 Acc: {val.top1:.4f}")

os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
model.export(format="torchscript", imgsz=128)
src = os.path.join(MODEL_SAVE_DIR, "yolo_model", "weights", "best.torchscript")
dst = os.path.join(MODEL_SAVE_DIR, "yolo_cls.pt")
if os.path.exists(src):
    shutil.copy2(src, dst)
    print(f"Model saved: {dst}")
else:
    model.save(dst)
    print(f"Model saved (pt): {dst}")

print("Done!")
