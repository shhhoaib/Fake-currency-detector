"""
EfficientNetB0 Transfer Learning for Pakistani Currency Detection
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from preprocess import preprocess_pipeline, get_augmentation, IMG_SIZE

EPOCHS = 25
BATCH_SIZE = 32
LEARNING_RATE = 0.0001
DATA_DIR = "../dataset"
MODEL_SAVE_PATH = "../backend/app/ml/model.h5"


def build_model(num_classes: int):
    base = tf.keras.applications.EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        pooling="avg",
    )
    base.trainable = False

    inputs = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x = tf.keras.applications.efficientnet.preprocess_input(inputs)
    x = base(x, training=False)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="sigmoid" if num_classes == 1 else "softmax")(x)

    model = models.Model(inputs, outputs)
    model.compile(
        optimizer=optimizers.Adam(learning_rate=LEARNING_RATE),
        loss="binary_crossentropy" if num_classes == 1 else "sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model, base


def plot_training(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.plot(history.history["accuracy"], label="Train")
    ax1.plot(history.history["val_accuracy"], label="Val")
    ax1.set_title("Accuracy")
    ax1.legend()
    ax2.plot(history.history["loss"], label="Train")
    ax2.plot(history.history["val_loss"], label="Val")
    ax2.set_title("Loss")
    ax2.legend()
    plt.savefig("training_curves.png")
    print("Saved training_curves.png")


def plot_confusion(y_true, y_pred, class_names):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", xticklabels=class_names, yticklabels=class_names)
    plt.title("Confusion Matrix")
    plt.ylabel("True")
    plt.xlabel("Predicted")
    plt.savefig("confusion_matrix.png")
    print("Saved confusion_matrix.png")


def main():
    print("=" * 60)
    print("PakShield AI - Model Training Pipeline")
    print("=" * 60)

    if not os.path.exists(DATA_DIR):
        print(f"Dataset directory '{DATA_DIR}' not found.")
        print("Please download the dataset from Kaggle:")
        print("https://www.kaggle.com/datasets/mmuzamil/real-and-fake-currency-pakistanis-dataset")
        print(f"And place it in: {DATA_DIR}")
        return

    X_train, X_val, X_test, y_train, y_val, y_test, class_names = preprocess_pipeline(DATA_DIR)
    num_classes = len(class_names)
    print(f"\nClasses: {class_names}")

    model, base_model = build_model(num_classes)
    print(f"\nModel built with EfficientNetB0 backbone")
    print(f"Total params: {model.count_params():,}")
    model.summary()

    datagen = get_augmentation()
    train_gen = datagen.flow(X_train, y_train, batch_size=BATCH_SIZE)

    reduce_lr = callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.2, patience=3, min_lr=1e-7, verbose=1
    )
    early_stop = callbacks.EarlyStopping(
        monitor="val_loss", patience=7, restore_best_weights=True, verbose=1
    )
    model_ckpt = callbacks.ModelCheckpoint(
        "best_model.h5", monitor="val_accuracy", save_best_only=True, verbose=1
    )

    print("\n" + "=" * 60)
    print("Phase 1: Training top layers (frozen backbone)")
    print("=" * 60)
    history1 = model.fit(
        train_gen,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        callbacks=[reduce_lr, early_stop, model_ckpt],
    )

    base_model.trainable = True
    model.compile(
        optimizer=optimizers.Adam(learning_rate=LEARNING_RATE / 10),
        loss="binary_crossentropy" if num_classes == 1 else "sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    print("\n" + "=" * 60)
    print("Phase 2: Fine-tuning entire model")
    print("=" * 60)
    history2 = model.fit(
        datagen.flow(X_train, y_train, batch_size=BATCH_SIZE),
        validation_data=(X_val, y_val),
        epochs=EPOCHS // 2,
        callbacks=[reduce_lr, early_stop, model_ckpt],
    )

    plot_training(history1)

    y_pred = (model.predict(X_test) > 0.5).astype(int).flatten() if num_classes == 1 else np.argmax(model.predict(X_test), axis=1)
    print("\n" + "=" * 60)
    print("Classification Report")
    print("=" * 60)
    print(classification_report(y_test, y_pred, target_names=class_names))
    plot_confusion(y_test, y_pred, class_names)

    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    model.save(MODEL_SAVE_PATH)
    print(f"\nModel saved to {MODEL_SAVE_PATH}")

    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"\nFinal Test Accuracy: {test_acc:.4f}")
    print(f"Final Test Loss: {test_loss:.4f}")
    print("\nTraining complete!")


if __name__ == "__main__":
    main()
