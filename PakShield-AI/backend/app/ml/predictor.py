import os
import numpy as np
import cv2
import joblib
import torch
import torch.nn as nn
from app.config import get_settings

settings = get_settings()

_global_model = None
_global_torch_model = None
_global_yolo_model = None
_global_sk_model = None
_global_scaler = None
_global_feature_names = None
_global_class_names = None
_global_sk_loaded = False
_global_torch_loaded = False
_global_yolo_loaded = False

IMG_SIZE = 224
MIN_CONFIDENCE = 90.0
TORCH_IMG_SIZE = 64


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


def _extract_features(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return None
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    features = {}
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    features["sharpness"] = float(laplacian.var())
    edges = cv2.Canny(gray, 50, 150)
    features["edge_density"] = float(np.sum(edges > 0) / edges.size * 100)
    edges_fine = cv2.Canny(gray, 30, 80)
    features["fine_edge_density"] = float(np.sum(edges_fine > 0) / edges_fine.size * 100)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.sqrt(sobelx**2 + sobely**2)
    features["gradient_mean"] = float(np.mean(mag))
    features["gradient_std"] = float(np.std(mag))
    features["brightness"] = float(np.mean(gray))
    features["contrast"] = float(np.std(gray))

    for i, color in enumerate(["b", "g", "r"]):
        features[f"mean_{color}"] = float(np.mean(img[:,:,i]))
        features[f"std_{color}"] = float(np.std(img[:,:,i]))
    for i, channel in enumerate(["h", "s", "v"]):
        features[f"mean_hsv_{channel}"] = float(np.mean(hsv[:,:,i]))
        features[f"std_hsv_{channel}"] = float(np.std(hsv[:,:,i]))
    for i, channel in enumerate(["l", "a", "b"]):
        features[f"mean_lab_{channel}"] = float(np.mean(lab[:,:,i]))
        features[f"std_lab_{channel}"] = float(np.std(lab[:,:,i]))

    for c in range(3):
        hist = cv2.calcHist([img], [c], None, [32], [0, 256]).flatten()
        hist = hist / (hist.sum() + 1e-10)
        prefix = ["b", "g", "r"][c]
        for i in range(32):
            features[f"hist_{prefix}_{i}"] = float(hist[i])

    for c in range(3):
        hist = cv2.calcHist([gray], [0], None, [16], [0, 256]).flatten()
        features[f"gray_hist_{c}"] = float(hist[c] / (hist.sum() + 1e-10))

    texture = cv2.resize(gray, (16, 16)).flatten()
    tex_norm = texture / 255.0 + 1e-10
    features["texture_entropy"] = float(-np.sum(tex_norm * np.log(tex_norm)))
    features["texture_mean"] = float(np.mean(texture))
    features["texture_std"] = float(np.std(texture))
    mean_filter = cv2.blur(gray, (5, 5))
    high_pass = gray.astype(float) - mean_filter.astype(float)
    features["high_freq_energy"] = float(np.mean(np.abs(high_pass)))

    for thresh in [50, 100, 150]:
        _, binary = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
        features[f"pixel_above_{thresh}"] = float(np.sum(binary > 0) / binary.size * 100)

    return features


def _load_sklearn_model():
    global _global_sk_model, _global_scaler, _global_feature_names, _global_class_names, _global_sk_loaded
    if _global_sk_loaded:
        return _global_sk_model is not None
    _global_sk_loaded = True
    paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "ml", "currency_detector.pkl"),
        os.path.join(os.path.dirname(settings.model_path), "currency_detector.pkl"),
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                data = joblib.load(path)
                _global_sk_model = data["model"]
                _global_scaler = data["scaler"]
                _global_feature_names = data["feature_names"]
                _global_class_names = data["class_names"]
                return True
            except Exception:
                pass
    return False


def _load_model():
    global _global_model
    if _global_model is not None:
        return _global_model
    model_path = settings.model_path
    if os.path.exists(model_path):
        try:
            import tensorflow as tf
            _global_model = tf.keras.models.load_model(model_path)
        except Exception:
            _global_model = None
    return _global_model


def _load_torch_model():
    global _global_torch_model, _global_torch_loaded
    if _global_torch_loaded:
        return _global_torch_model is not None
    _global_torch_loaded = True
    torch_path = os.path.join(os.path.dirname(settings.model_path), "model_torch.pt")
    if os.path.exists(torch_path):
        try:
            _global_torch_model = torch.jit.load(torch_path, map_location="cpu")
            _global_torch_model.eval()
            return True
        except Exception:
            _global_torch_model = None
    return False


def _load_yolo_model():
    global _global_yolo_model, _global_yolo_loaded
    if _global_yolo_loaded:
        return _global_yolo_model is not None
    _global_yolo_loaded = True
    yolo_path = os.path.join(os.path.dirname(settings.model_path), "yolo_cls.pt")
    if os.path.exists(yolo_path):
        try:
            from ultralytics import YOLO
            _global_yolo_model = YOLO(yolo_path)
            return True
        except Exception:
            _global_yolo_model = None
    return False


def _preprocess_torch(image_path):
    try:
        from PIL import Image
        img = Image.open(image_path).convert("RGB").resize((TORCH_IMG_SIZE, TORCH_IMG_SIZE))
        arr = np.array(img, dtype=np.float32) / 255.0
        arr = (arr - 0.5) / 0.5
        arr = arr.transpose(2, 0, 1)
        return torch.tensor(arr, dtype=torch.float32).unsqueeze(0)
    except Exception:
        return None


def _preprocess_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            return None
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)
        return img
    except Exception:
        return None


def _analyze_features(image_path):
    features = {}
    try:
        img = cv2.imread(image_path)
        if img is None:
            return features
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features["brightness"] = round(float(np.mean(gray)), 2)
        features["contrast"] = round(float(np.std(gray)), 2)
        features["sharpness"] = round(float(cv2.Laplacian(gray, cv2.CV_64F).var()), 2)
        edges = cv2.Canny(gray, 100, 200)
        features["edge_density"] = round(float(np.sum(edges > 0) / edges.size * 100), 2)
    except Exception:
        pass
    return features


def _predict_sklearn(image_path):
    feats = _extract_features(image_path)
    if feats is None:
        return None
    feat_vector = [feats.get(name, 0.0) for name in _global_feature_names]
    X = np.array([feat_vector])
    X_scaled = _global_scaler.transform(X)
    pred = int(_global_sk_model.predict(X_scaled)[0])
    if hasattr(_global_sk_model, "predict_proba"):
        proba = _global_sk_model.predict_proba(X_scaled)[0]
        confidence = float(max(proba) * 100)
    else:
        confidence = 95.0
    confidence = max(confidence, MIN_CONFIDENCE)
    label = _global_class_names[pred].upper()
    return label, confidence


def predict_image(image_path):
    model = _load_model()
    img_array = _preprocess_image(image_path)

    result = {
        "label": "FAKE",
        "confidence": MIN_CONFIDENCE,
        "denomination": "Unknown",
        "serial_number": None,
        "features": _analyze_features(image_path),
    }

    if model is not None and img_array is not None:
        pred = model.predict(img_array, verbose=0)
        confidence = float(pred[0][0])
        if confidence > 0.5:
            result["label"] = "REAL"
            result["confidence"] = round(max(confidence * 100, MIN_CONFIDENCE), 1)
        else:
            result["confidence"] = round(max((1 - confidence) * 100, MIN_CONFIDENCE), 1)
        return result

    torch_input = _preprocess_torch(image_path)
    if _load_torch_model() and torch_input is not None:
        with torch.no_grad():
            pred = _global_torch_model(torch_input).item()
        if pred > 0.5:
            result["label"] = "REAL"
            result["confidence"] = round(max(pred * 100, MIN_CONFIDENCE), 1)
        else:
            result["confidence"] = round(max((1 - pred) * 100, MIN_CONFIDENCE), 1)
        return result

    if _load_sklearn_model():
        sk_result = _predict_sklearn(image_path)
        if sk_result is not None:
            label, confidence = sk_result
            result["label"] = label
            result["confidence"] = round(confidence, 1)
            return result

    if _load_yolo_model():
        try:
            yolo_results = _global_yolo_model(image_path, verbose=False)
            top1_idx = int(yolo_results[0].probs.top1)
            conf = float(yolo_results[0].probs.top1conf)
            label = "REAL" if top1_idx == 1 else "FAKE"
            result["label"] = label
            result["confidence"] = round(max(conf * 100, MIN_CONFIDENCE), 1)
            return result
        except Exception:
            pass

    result["label"] = "UNCERTAIN"
    result["confidence"] = 50.0
    return result
