"""
Data Preprocessing Pipeline for Pakistani Currency Dataset
"""

import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

IMG_SIZE = 224
BATCH_SIZE = 32
SEED = 42


def load_dataset(data_dir: str):
    images = []
    labels = []
    class_names = sorted(os.listdir(data_dir))

    for label, class_name in enumerate(class_names):
        class_dir = os.path.join(data_dir, class_name)
        if not os.path.isdir(class_dir):
            continue
        for fname in os.listdir(class_dir):
            fpath = os.path.join(class_dir, fname)
            img = cv2.imread(fpath)
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            images.append(img)
            labels.append(label)

    return np.array(images), np.array(labels), class_names


def get_augmentation():
    return ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        brightness_range=(0.8, 1.2),
        fill_mode="nearest",
    )


def preprocess_pipeline(data_dir: str, val_split: float = 0.2, test_split: float = 0.1):
    X, y, class_names = load_dataset(data_dir)
    print(f"Loaded {len(X)} images from {len(class_names)} classes: {class_names}")

    X = X.astype(np.float32) / 255.0

    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=test_split, random_state=SEED, stratify=y
    )
    val_ratio = val_split / (1 - test_split)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=val_ratio, random_state=SEED, stratify=y_temp
    )

    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    return X_train, X_val, X_test, y_train, y_val, y_test, class_names


def plot_samples(X, y, class_names, n=8):
    plt.figure(figsize=(12, 6))
    for i in range(n):
        plt.subplot(2, 4, i + 1)
        idx = np.random.randint(len(X))
        plt.imshow(X[idx])
        plt.title(class_names[y[idx]])
        plt.axis("off")
    plt.tight_layout()
    plt.savefig("dataset_samples.png")
    print("Saved dataset_samples.png")
