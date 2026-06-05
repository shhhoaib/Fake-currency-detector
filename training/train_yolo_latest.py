"""
PakShield AI - YOLOv8 Training with Synthetic + Augmented Dataset
Trains using generated synthetic currency note images
Latest Ultralytics YOLO
"""

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import sys, shutil, warnings, random
warnings.filterwarnings('ignore')

from ultralytics import YOLO
import numpy as np
import cv2
from sklearn.model_selection import train_test_split

IMG_SIZE = 224
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset")
YOLO_DATA_DIR = os.path.join(os.path.dirname(__file__), "yolo_dataset_train")
MODEL_SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "backend", "app", "ml")
NUM_SAMPLES = 2000
SEED = 42

np.random.seed(SEED)
random.seed(SEED)

PKR_DENOMS = ["10", "20", "50", "100", "500", "1000", "5000"]

PKR_COLORS = {
    "10":  {"primary": (34, 139, 34), "secondary": (50, 180, 50), "accent": (80, 200, 80)},
    "20":  {"primary": (30, 140, 160), "secondary": (50, 170, 190), "accent": (120, 200, 80)},
    "50":  {"primary": (120, 60, 160), "secondary": (150, 80, 180), "accent": (180, 120, 200)},
    "100": {"primary": (50, 50, 180), "secondary": (70, 70, 200), "accent": (100, 100, 220)},
    "500": {"primary": (40, 160, 40), "secondary": (60, 180, 60), "accent": (100, 200, 100)},
    "1000": {"primary": (160, 120, 50), "secondary": (180, 140, 60), "accent": (200, 160, 80)},
    "5000": {"primary": (40, 130, 90), "secondary": (60, 150, 110), "accent": (80, 180, 130)},
}


def gen_real_note():
    """Generate a synthetic genuine currency note with realistic features"""
    denom = random.choice(PKR_DENOMS)
    colors = PKR_COLORS[denom]

    img = np.ones((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8) * random.randint(190, 220)
    p = colors["primary"]
    s = colors["secondary"]
    a = colors["accent"]

    border_w = random.randint(2, 4)
    border_color = (p[2], p[1], p[0])
    cv2.rectangle(img, (border_w, border_w), (IMG_SIZE-border_w, IMG_SIZE-border_w), border_color, border_w)

    text_color = (a[2], a[1], a[0])
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(img, str(denom), (random.randint(20, 50), random.randint(40, 70)),
                font, random.uniform(1.0, 1.5), text_color, random.randint(2, 3))
    cv2.putText(img, "PKR", (random.randint(20, 50), random.randint(80, 110)),
                font, random.uniform(0.6, 0.9), (s[2], s[1], s[0]), random.randint(1, 2))
    cv2.putText(img, "STATE BANK OF PAKISTAN", (random.randint(30, 60), random.randint(140, 175)),
                font, random.uniform(0.35, 0.5), (p[2]//2, p[1]//2, p[0]//2), 1)

    sn = f"{random.choice('ABCDEFGH')}{random.choice('ABCDEFGH')}{random.randint(100000, 999999)}"
    cv2.putText(img, sn, (random.randint(30, 80), random.randint(190, 215)),
                font, random.uniform(0.4, 0.55), text_color, 1)

    for i in range(10, IMG_SIZE-10, random.randint(6, 10)):
        thickness = random.randint(1, 2)
        color_val = random.randint(140, 200)
        cv2.line(img, (i, 150), (i+2, 180), (color_val, color_val, max(color_val-20, 0)), thickness)

    for i in range(10, IMG_SIZE-10, random.randint(8, 14)):
        cv2.line(img, (80, i), (200, i+1),
                 (random.randint(80, 140), random.randint(100, 160), random.randint(60, 100)), 1)

    for _ in range(random.randint(3, 6)):
        x, y = random.randint(40, IMG_SIZE-40), random.randint(40, IMG_SIZE-40)
        r = random.randint(25, 45)
        overlay = img.copy()
        cv2.circle(overlay, (x, y), r, (180, 200, 160), -1)
        alpha = random.uniform(0.2, 0.35)
        img = cv2.addWeighted(overlay, alpha, img, 1-alpha, 0)

    thread_x = random.randint(IMG_SIZE//2 - 20, IMG_SIZE//2 + 20)
    cv2.line(img, (thread_x, 0), (thread_x, IMG_SIZE), (200, 210, 180), random.randint(2, 4))

    for _ in range(random.randint(3, 7)):
        x, y = random.randint(20, IMG_SIZE-20), random.randint(20, IMG_SIZE-20)
        cv2.circle(img, (x, y), random.randint(1, 2), (50, 80, 40), -1)

    watermark_center = (random.randint(IMG_SIZE//3, 2*IMG_SIZE//3),
                        random.randint(IMG_SIZE//3, 2*IMG_SIZE//3))
    overlay2 = img.copy()
    cv2.circle(overlay2, watermark_center, random.randint(30, 50), (170, 190, 160), -1)
    img = cv2.addWeighted(overlay2, random.uniform(0.15, 0.25), img, 0.85, 0)

    noise = np.random.normal(0, random.uniform(1.5, 3.0), img.shape).astype(np.uint8)
    img = cv2.add(img, noise)

    if random.random() < 0.3:
        kernel_size = random.choice([3, 5])
        img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0.5)

    return img, 1


def gen_fake_note():
    """Generate a synthetic counterfeit note with common flaws"""
    denom = random.choice(PKR_DENOMS)
    colors = PKR_COLORS[denom]

    bg = random.randint(150, 195)
    img = np.ones((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8) * bg
    p = colors["primary"]
    s = colors["secondary"]
    a = colors["accent"]

    border_w = random.randint(1, 2)
    border_color = (max(p[2]-40, 0), max(p[1]-40, 0), max(p[0]-40, 0))
    cv2.rectangle(img, (border_w, border_w), (IMG_SIZE-border_w, IMG_SIZE-border_w), border_color, border_w)

    text_color = (max(a[2]-30, 0), max(a[1]-30, 0), max(a[0]-30, 0))
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(img, str(denom), (random.randint(30, 60), random.randint(45, 75)),
                font, random.uniform(1.2, 1.6), text_color, random.randint(1, 2))
    cv2.putText(img, "PKR", (random.randint(30, 60), random.randint(85, 115)),
                font, random.uniform(0.5, 0.7), text_color, 1)

    for i in range(8, IMG_SIZE-8, random.randint(5, 8)):
        cv2.line(img, (i, 152), (i+3, 172),
                 (random.randint(100, 180), random.randint(60, 130), random.randint(30, 70)),
                 random.randint(1, 3))

    blur_strength = random.uniform(0.8, 3.0)
    img = cv2.GaussianBlur(img, (random.choice([3, 5]), random.choice([3, 5])), blur_strength)

    img_f = img.astype(np.float32)
    img_f[:,:,0] *= random.uniform(0.5, 1.5)
    img_f[:,:,1] *= random.uniform(0.5, 1.5)
    img_f[:,:,2] *= random.uniform(0.5, 1.5)
    img = np.clip(img_f, 0, 255).astype(np.uint8)

    for _ in range(random.randint(5, 15)):
        x, y = random.randint(10, IMG_SIZE-10), random.randint(10, IMG_SIZE-10)
        cv2.circle(img, (x, y), random.randint(1, 4), (0, 0, 0), -1)

    if random.random() < 0.4:
        img = cv2.GaussianBlur(img, (5, 5), 2.0)

    noise = np.random.normal(0, random.uniform(6, 15), img.shape).astype(np.uint8)
    img = cv2.add(img, noise)

    return img, 0


def generate_dataset(num_samples, output_dir):
    """Generate synthetic dataset"""
    os.makedirs(os.path.join(output_dir, "real"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "fake"), exist_ok=True)

    real_count = fake_count = 0
    for i in range(num_samples):
        if random.random() < 0.5:
            img, label = gen_real_note()
            fname = f"real_{real_count:05d}.png"
            cv2.imwrite(os.path.join(output_dir, "real", fname), img)
            real_count += 1
        else:
            img, label = gen_fake_note()
            fname = f"fake_{fake_count:05d}.png"
            cv2.imwrite(os.path.join(output_dir, "fake", fname), img)
            fake_count += 1

        if (i+1) % 200 == 0:
            print(f"  Generated {i+1}/{num_samples} images (real: {real_count}, fake: {fake_count})")

    print(f"  Total - real: {real_count}, fake: {fake_count}")
    return real_count, fake_count


def prepare_yolo_dataset(data_dir, yolo_dir):
    """Prepare YOLO-format dataset from existing data dir"""
    class_names = ["fake", "real"]
    paths, labels = [], []

    for label, name in enumerate(class_names):
        folder = os.path.join(data_dir, name)
        if os.path.isdir(folder):
            for f in os.listdir(folder):
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    paths.append(os.path.join(folder, f))
                    labels.append(label)

    if len(paths) < 10:
        return False

    train_p, test_p, train_l, test_l = train_test_split(
        paths, labels, test_size=0.15, random_state=SEED, stratify=labels
    )
    train_p, val_p, train_l, val_l = train_test_split(
        train_p, train_l, test_size=0.15, random_state=SEED, stratify=train_l
    )

    if os.path.exists(yolo_dir):
        shutil.rmtree(yolo_dir)

    for split, sp, sl in [("train", train_p, train_l), ("val", val_p, val_l), ("test", test_p, test_l)]:
        for p, l in zip(sp, sl):
            dest = os.path.join(yolo_dir, split, class_names[l], os.path.basename(p))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(p, dest)

    print(f"YOLO dataset: train={len(train_p)}, val={len(val_p)}, test={len(test_p)}")
    return True


def main():
    print("=" * 65)
    print("  PakShield AI - YOLO Training Pipeline (Latest Ultralytics)")
    print("=" * 65)

    if not os.path.exists(DATA_DIR):
        print(f"\n[1/5] Dataset not found at {DATA_DIR}")
        print("       Generating synthetic currency note dataset...")
        os.makedirs(DATA_DIR, exist_ok=True)
        real_c, fake_c = generate_dataset(NUM_SAMPLES, DATA_DIR)
    else:
        real_c = len(os.listdir(os.path.join(DATA_DIR, "real"))) if os.path.exists(os.path.join(DATA_DIR, "real")) else 0
        fake_c = len(os.listdir(os.path.join(DATA_DIR, "fake"))) if os.path.exists(os.path.join(DATA_DIR, "fake")) else 0
        print(f"\n[1/5] Existing dataset found at {DATA_DIR}")
        print(f"       real: {real_c}, fake: {fake_c}")

    print(f"\n[2/5] Preparing YOLO-format dataset...")
    if not prepare_yolo_dataset(DATA_DIR, YOLO_DATA_DIR):
        print("[ERROR] Not enough images to train. Need at least 10.")
        return

    print(f"\n[3/5] Loading YOLO model...")
    model = YOLO("yolov8n-cls.pt")

    print(f"\n[4/5] Training model...")
    print(f"       Using: Ultralytics YOLOv8 classification")
    print(f"       Image size: {IMG_SIZE}")
    print(f"       Device: cpu")
    print()

    results = model.train(
        data=YOLO_DATA_DIR,
        epochs=30,
        imgsz=IMG_SIZE,
        batch=16,
        lr0=0.001,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3,
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        device="cpu",
        seed=SEED,
        patience=8,
        project=os.path.dirname(__file__),
        name="yolo_training",
        exist_ok=True,
        verbose=True,
        plots=True,
        val=True,
        cos_lr=True,
        augment=True,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=5.0,
        translate=0.1,
        scale=0.3,
        shear=2.0,
        perspective=0.0,
        flipud=0.05,
        fliplr=0.5,
        mosaic=0.3,
        mixup=0.1,
        copy_paste=0.05,
        erasing=0.2,
        crop_fraction=0.8,
        auto_augment="randaugment",
    )

    print(f"\n[5/5] Evaluating and exporting model...")
    val_results = model.val()
    print(f"  Top-1 Accuracy: {val_results.top1:.4f}")
    print(f"  Top-5 Accuracy: {val_results.top5:.4f}")

    os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
    export_path = model.export(format="torchscript")
    if export_path and os.path.exists(export_path):
        final_dst = os.path.join(MODEL_SAVE_DIR, "yolo_cls.pt")
        shutil.copy2(export_path, final_dst)
        print(f"\n  Model exported to: {final_dst}")
    else:
        final_path = os.path.join(MODEL_SAVE_DIR, "yolo_cls.pt")
        model.save(final_path)
        print(f"\n  Model saved to: {final_path}")

    model_size = os.path.getsize(os.path.join(MODEL_SAVE_DIR, "yolo_cls.pt"))
    print(f"  Model size: {model_size / 1024:.1f} KB")

    print(f"\n{'='*65}")
    print(f"  Training Complete!")
    print(f"  Model: {os.path.join(MODEL_SAVE_DIR, 'yolo_cls.pt')}")
    print(f"  Val Accuracy: {val_results.top1:.4f}")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
