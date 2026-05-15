import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

IMG_SIZE = 64
BATCH_SIZE = 128
EPOCHS = 10
LEARNING_RATE = 0.001
DATA_DIR = "../../dataset"
MODEL_SAVE_DIR = "../backend/app/ml"


class TinyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1), nn.BatchNorm2d(16), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.MaxPool2d(2),
            nn.AdaptiveAvgPool2d(1), nn.Flatten(),
            nn.Dropout(0.4), nn.Linear(64, 1), nn.Sigmoid(),
        )

    def forward(self, x):
        return self.net(x)


def load_images(data_dir, label):
    paths = []
    if not os.path.isdir(data_dir):
        return paths, []
    for fname in os.listdir(data_dir):
        if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
            paths.append(os.path.join(data_dir, fname))
    return paths, [label] * len(paths)


def preprocess(img_path):
    img = Image.open(img_path).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
    arr = np.array(img, dtype=np.float32) / 255.0
    return (arr - 0.5) / 0.5


def main():
    print("=" * 60)
    print("PakShield AI - Fast CNN Training")
    print("=" * 60)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    print("Loading and preprocessing images...")
    p_real, l_real = load_images(os.path.join(DATA_DIR, "real"), 1)
    p_fake, l_fake = load_images(os.path.join(DATA_DIR, "fake"), 0)
    p_sr, l_sr = load_images(os.path.join(DATA_DIR, "synthetic", "real"), 1)
    p_sf, l_sf = load_images(os.path.join(DATA_DIR, "synthetic", "fake"), 0)

    all_paths = p_real + p_fake + p_sr + p_sf
    all_labels = l_real + l_fake + l_sr + l_sf

    print(f"Preprocessing {len(all_paths)} images to {IMG_SIZE}x{IMG_SIZE}...")
    X = np.array([preprocess(p) for p in all_paths]).transpose(0, 3, 1, 2)
    y = np.array(all_labels)
    print(f"Shape: {X.shape}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.15, random_state=42, stratify=y_train)
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

    train_loader = DataLoader(TensorDataset(torch.tensor(X_train), torch.tensor(y_train, dtype=torch.float32)), BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(TensorDataset(torch.tensor(X_val), torch.tensor(y_val, dtype=torch.float32)), BATCH_SIZE)
    test_loader = DataLoader(TensorDataset(torch.tensor(X_test), torch.tensor(y_test, dtype=torch.float32)), BATCH_SIZE)

    model = TinyCNN().to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_acc = 0.0
    for epoch in range(1, EPOCHS + 1):
        model.train()
        tl, tc, tt = 0.0, 0, 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.unsqueeze(1).to(device)
            optimizer.zero_grad()
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()
            tl += loss.item() * images.size(0)
            tc += ((model(images).detach() > 0.5).float() == labels).sum().item()
            tt += labels.size(0)

        model.eval()
        vl, vc, vt = 0.0, 0, 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.unsqueeze(1).to(device)
                loss = criterion(model(images), labels)
                vl += loss.item() * images.size(0)
                vc += ((model(images) > 0.5).float() == labels).sum().item()
                vt += labels.size(0)

        tle, tae, vle, vae = tl/tt, tc/tt, vl/vt, vc/vt
        print(f"Epoch {epoch:2d}/{EPOCHS} - Loss: {tle:.4f} Acc: {tae:.4f} | Val Loss: {vle:.4f} Val Acc: {vae:.4f}")

        if vae > best_acc:
            best_acc = vae
            torch.save(model.state_dict(), "best_torch_model.pt")

    print(f"\nBest val acc: {best_acc:.4f}")

    model.load_state_dict(torch.load("best_torch_model.pt", weights_only=True))
    model.eval()
    all_preds, all_true = [], []
    with torch.no_grad():
        for images, labels in test_loader:
            preds = (model(images.to(device)) > 0.5).int().flatten().cpu().numpy()
            all_preds.extend(preds)
            all_true.extend(labels.numpy())

    print("\nClassification Report:")
    print(classification_report(all_true, all_preds, target_names=["fake", "real"]))

    cm = confusion_matrix(all_true, all_preds)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", xticklabels=["fake","real"], yticklabels=["fake","real"])
    plt.title("Confusion Matrix")
    plt.savefig("torch_confusion_matrix.png")

    os.makedirs(MODEL_SAVE_DIR, exist_ok=True)
    model.cpu()
    scripted = torch.jit.script(model)
    scripted.save(os.path.join(MODEL_SAVE_DIR, "model_torch.pt"))

    acc = sum(1 for a, b in zip(all_preds, all_true) if a == b) / len(all_true)
    print(f"\nModel saved: {os.path.join(MODEL_SAVE_DIR, 'model_torch.pt')}")
    print(f"Test Accuracy: {acc:.4f}")
    print("Done!")


if __name__ == "__main__":
    main()
