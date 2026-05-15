import os
import cv2
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV

DATA_DIR = "../../dataset"
MODEL_DIR = "../backend/app/ml"
IMG_SIZE = 224
_feat_keys = None


def gen_real_note():
    img = np.ones((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8) * np.random.randint(190, 215)
    border_color = (np.random.randint(120, 160), np.random.randint(160, 200), np.random.randint(80, 120))
    cv2.rectangle(img, (18, 18), (IMG_SIZE-18, IMG_SIZE-18), border_color, np.random.randint(2, 4))
    text_color = (np.random.randint(30, 70), np.random.randint(60, 100), np.random.randint(20, 50))
    denom = np.random.choice(["5000", "1000", "100", "50"])
    cv2.putText(img, denom, (np.random.randint(50, 70), np.random.randint(90, 110)), cv2.FONT_HERSHEY_SIMPLEX, np.random.uniform(1.0, 1.4), text_color, np.random.randint(1, 3))
    cv2.putText(img, "PKR", (np.random.randint(50, 70), np.random.randint(130, 150)), cv2.FONT_HERSHEY_SIMPLEX, np.random.uniform(0.7, 0.9), text_color, np.random.randint(1, 2))
    for i in range(15, IMG_SIZE-15, np.random.randint(4, 7)):
        cv2.line(img, (i, 145), (i+2, 175), (np.random.randint(100, 140), np.random.randint(140, 180), np.random.randint(60, 100)), np.random.randint(1, 2))
    for i in range(25, IMG_SIZE-25, np.random.randint(6, 10)):
        cv2.line(img, (75, i), (195, i+1), (np.random.randint(80, 120), np.random.randint(120, 160), np.random.randint(40, 80)), 1)
    overlay = img.copy()
    center = (np.random.randint(130, 170), np.random.randint(100, 140))
    cv2.circle(overlay, center, np.random.randint(35, 50), (160, 180, 140), -1)
    img = cv2.addWeighted(overlay, np.random.uniform(0.25, 0.4), img, 0.75, 0)
    for _ in range(np.random.randint(3, 7)):
        x, y = np.random.randint(30, 200, 2)
        cv2.circle(img, (x, y), np.random.randint(1, 3), (60, 100, 40), -1)
    noise = np.random.normal(0, np.random.uniform(2, 4), img.shape).astype(np.uint8)
    img = cv2.add(img, noise)
    return img


def gen_fake_note():
    bg = np.random.randint(160, 200)
    img = np.ones((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8) * bg
    border_color = (np.random.randint(150, 200), np.random.randint(90, 140), np.random.randint(60, 100))
    cv2.rectangle(img, (22, 22), (IMG_SIZE-22, IMG_SIZE-22), border_color, np.random.randint(1, 3))
    text_color = (np.random.randint(60, 100), np.random.randint(40, 80), np.random.randint(30, 70))
    denom = np.random.choice(["5000", "1000", "100", "50"])
    cv2.putText(img, denom, (np.random.randint(45, 75), np.random.randint(95, 115)), cv2.FONT_HERSHEY_SIMPLEX, np.random.uniform(1.1, 1.5), text_color, np.random.randint(1, 2))
    cv2.putText(img, "PKR", (np.random.randint(55, 75), np.random.randint(135, 155)), cv2.FONT_HERSHEY_SIMPLEX, np.random.uniform(0.6, 0.8), text_color, 1)
    for i in range(15, IMG_SIZE-15, np.random.randint(5, 9)):
        cv2.line(img, (i, 150), (i+3, 170), (np.random.randint(130, 180), np.random.randint(80, 130), np.random.randint(40, 80)), np.random.randint(1, 3))
    img = cv2.GaussianBlur(img, (np.random.choice([3, 5]), np.random.choice([3, 5])), np.random.uniform(0.8, 2.5))
    img_f = img.astype(np.float32)
    img_f[:,:,0] *= np.random.uniform(0.6, 1.4)
    img_f[:,:,1] *= np.random.uniform(0.6, 1.4)
    img_f[:,:,2] *= np.random.uniform(0.6, 1.4)
    img = np.clip(img_f, 0, 255).astype(np.uint8)
    for _ in range(np.random.randint(5, 15)):
        x, y = np.random.randint(20, 200, 2)
        cv2.circle(img, (x, y), np.random.randint(1, 4), (0, 0, 0), -1)
    noise = np.random.normal(0, np.random.uniform(6, 12), img.shape).astype(np.uint8)
    img = cv2.add(img, noise)
    return img


def extract_features(img_path):
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
    tex_norm = texture / 255.0
    tex_norm = tex_norm + 1e-10
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


def load_class_images(class_dir, label):
    global _feat_keys
    samples, errors = [], 0
    if not os.path.exists(class_dir):
        return samples, errors
    files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg')) and '.aug' not in f]
    for fname in files:
        fpath = os.path.join(class_dir, fname)
        feats = extract_features(fpath)
        if feats is None:
            errors += 1
            continue
        if _feat_keys is None:
            _feat_keys = list(feats.keys())
        samples.append((list(feats.values()), label))
    return samples, errors


def main():
    print("=" * 60)
    print("PakShield AI - Enhanced Model Training")
    print("=" * 60)

    print("Extracting features from existing dataset...")
    X, y = [], []
    class_names = ["fake", "real"]
    errors = 0
    global _feat_keys
    _feat_keys = None

    for label, class_name in enumerate(class_names):
        samples, errs = load_class_images(os.path.join(DATA_DIR, class_name), label)
        X.extend([s[0] for s in samples])
        y.extend([s[1] for s in samples])
        errors += errs

        samples, errs = load_class_images(os.path.join(DATA_DIR, "synthetic", class_name), label)
        X.extend([s[0] for s in samples])
        y.extend([s[1] for s in samples])
        errors += errs

    print(f"Loaded {len(X)} samples ({errors} errors)")
    feature_names = _feat_keys
    print(f"Features: {len(feature_names)}")

    X = np.array(X)
    y = np.array(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    rf = RandomForestClassifier(
        n_estimators=150, max_depth=15, min_samples_split=3,
        min_samples_leaf=1, random_state=42, n_jobs=-1
    )
    rf.fit(X_train, y_train)

    gb = GradientBoostingClassifier(
        n_estimators=100, max_depth=5, learning_rate=0.1,
        subsample=0.8, random_state=42
    )
    gb.fit(X_train, y_train)

    for name, model in [("RandomForest", rf), ("GradientBoosting", gb)]:
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"\n{name} Accuracy: {acc:.4f}")
        cv_scores = cross_val_score(model, X_scaled, y, cv=5)
        print(f"{name} CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    if hasattr(rf, "predict_proba"):
        proba_rf = rf.predict_proba(X_test)
        mean_conf_rf = np.max(proba_rf, axis=1).mean()
        print(f"\nRandomForest Avg Confidence: {mean_conf_rf*100:.2f}%")

    if hasattr(gb, "predict_proba"):
        proba_gb = gb.predict_proba(X_test)
        mean_conf_gb = np.max(proba_gb, axis=1).mean()
        print(f"GradientBoosting Avg Confidence: {mean_conf_gb*100:.2f}%")

    best_model = gb if accuracy_score(y_test, gb.predict(X_test)) >= accuracy_score(y_test, rf.predict(X_test)) else rf
    best_name = "GradientBoosting" if best_model is gb else "RandomForest"
    best_acc = accuracy_score(y_test, best_model.predict(X_test))

    print(f"\nBest: {best_name} ({best_acc:.4f})")

    calibrated = CalibratedClassifierCV(best_model, cv=3, method="sigmoid")
    calibrated.fit(X_scaled, y)
    proba_cal = calibrated.predict_proba(X_test)
    mean_conf_cal = np.max(proba_cal, axis=1).mean()
    print(f"Calibrated Avg Confidence: {mean_conf_cal*100:.2f}%")

    model_data = {
        "model": calibrated,
        "scaler": scaler,
        "feature_names": feature_names,
        "class_names": class_names,
        "model_type": f"Calibrated_{best_name}",
        "accuracy": best_acc,
        "avg_confidence": mean_conf_cal,
    }
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model_data, os.path.join(MODEL_DIR, "currency_detector.pkl"))
    print(f"\nSaved: {os.path.join(MODEL_DIR, 'currency_detector.pkl')}")

    y_pred = best_model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    print("\nConfusion Matrix:")
    print(cm)
    print("\nReport:")
    print(classification_report(y_test, y_pred, target_names=class_names))

    print("\nDone!")


if __name__ == "__main__":
    main()
