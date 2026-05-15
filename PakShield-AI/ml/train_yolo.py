import os
import shutil
import numpy as np
from sklearn.model_selection import train_test_split
from ultralytics import YOLO

DATA_DIR = "../../dataset"
YOLO_DATA_DIR = "../yolo_dataset"
MODEL_SAVE_DIR = "../backend/app/ml"

def prepare_yolo_dataset():
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

    train_paths, test_paths, train_labels, test_labels = train_test_split(
        paths, labels, test_size=0.15, random_state=42, stratify=labels
    )
    train_paths, val_paths, train_labels, val_labels = train_test_split(
        train_paths, train_labels, test_size=0.15, random_state=42, stratify=train_labels
    )

    if os.path.exists(YOLO_DATA_DIR):
        shutil.rmtree(YOLO_DATA_DIR)

    for split, split_paths, split_labels in [
        ("train", train_paths, train_labels),
        ("val", val_paths, val_labels),
        ("test", test_paths, test_labels),
    ]:
        for p, l in zip(split_paths, split_labels):
            dest = os.path.join(YOLO_DATA_DIR, split, class_names[l], os.path.basename(p))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(p, dest)

    print(f"YOLO dataset created: train={len(train_paths)}, val={len(val_paths)}, test={len(test_paths)}")
    return YOLO_DATA_DIR


def main():
    print("=" * 60)
    print("PakShield AI - YOLOv8 Training")
    print("=" * 60)

    prepare_yolo_dataset()

    model = YOLO("yolov8n-cls.pt")

    results = model.train(
        data=YOLO_DATA_DIR,
        epochs=20,
        imgsz=224,
        batch=32,
        lr0=0.001,
        device="cpu",
        patience=5,
        seed=42,
        project=MODEL_SAVE_DIR,
        name="yolo_model",
        exist_ok=True,
    )

    val_results = model.val()
    print(f"\nValidation Results:")
    print(f"  Top-1 Accuracy: {val_results.top1:.4f}")
    print(f"  Top-5 Accuracy: {val_results.top5:.4f}")

    os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
    export_path = model.export(format="torchscript")
    final_path = os.path.join(MODEL_SAVE_DIR, "yolo_cls.pt")
    if os.path.exists(export_path):
        shutil.copy2(export_path, final_path)
    else:
        model.save(final_path)
    print(f"\nModel saved to {final_path}")
    print("Done!")


if __name__ == "__main__":
    main()
