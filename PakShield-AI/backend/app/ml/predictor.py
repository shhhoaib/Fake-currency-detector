import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import numpy as np
import cv2
import joblib
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

PKR_COLORS = {
    "10": {"hsv_range": ([30, 20, 20], [90, 255, 255]), "name": "Green (10 PKR)"},
    "20": {"hsv_range": ([20, 20, 20], [60, 255, 255]), "name": "Green/Orange (20 PKR)"},
    "50": {"hsv_range": ([100, 20, 20], [160, 255, 255]), "name": "Purple (50 PKR)"},
    "100": {"hsv_range": ([0, 30, 20], [20, 255, 255]), "name": "Red (100 PKR)"},
    "500": {"hsv_range": ([40, 20, 20], [100, 255, 255]), "name": "Green (500 PKR)"},
    "1000": {"hsv_range": ([80, 20, 20], [140, 255, 255]), "name": "Blue (1000 PKR)"},
    "5000": {"hsv_range": ([30, 20, 20], [80, 255, 255]), "name": "Green (5000 PKR)"},
}


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
            import torch
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
        import torch
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


def _detect_security_thread(gray):
    h, w = gray.shape
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blur, 30, 100)
    vert_proj = np.sum(edges, axis=0).astype(float) / h
    baseline = float(np.mean(vert_proj))
    threshold_val = baseline * 2.0
    candidates = np.where(vert_proj > threshold_val)[0]
    if len(candidates) < 2:
        return 15, "Security thread not detected — may be absent or counterfeit"
    groups = []
    current = [candidates[0]]
    for i in range(1, len(candidates)):
        if candidates[i] - candidates[i-1] <= 3:
            current.append(candidates[i])
        else:
            groups.append(current)
            current = [candidates[i]]
    groups.append(current)
    best_score = 0
    for g in groups:
        width = len(g)
        if 3 < width < w * 0.12:
            peak = float(np.max(vert_proj[g]))
            score = min(100, 30 + peak * 1.5 - abs(width - 8) * 2)
            best_score = max(best_score, score)
    if best_score > 70:
        return round(best_score), "Embedded security thread detected with proper metallic strip characteristics"
    elif best_score > 40:
        return round(best_score), "Security thread partially detected — may be obscured, damaged, or improperly replicated"
    else:
        return round(max(best_score, 15)), "Security thread not clearly detected — common feature in counterfeit reproductions"


def _detect_watermark_pattern(gray):
    h, w = gray.shape
    blur = cv2.GaussianBlur(gray, (15, 15), 0)
    watermark_region = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 41, -5)
    white_ratio = float(np.sum(watermark_region > 0) / watermark_region.size)
    f_transform = np.fft.fft2(gray.astype(float))
    f_shift = np.fft.fftshift(f_transform)
    magnitude_spectrum = np.log(np.abs(f_shift) + 1)
    cy, cx = h // 2, w // 2
    inner = magnitude_spectrum[cy-15:cy+15, cx-15:cx+15]
    outer_mask = np.ones((h, w), dtype=bool)
    outer_mask[cy-25:cy+25, cx-25:cx+25] = False
    outer_region = magnitude_spectrum[outer_mask]
    if len(outer_region) == 0:
        return 50, "Watermark analysis inconclusive"
    inner_mean = float(np.mean(inner))
    outer_mean = float(np.mean(outer_region))
    freq_ratio = inner_mean / (outer_mean + 1e-10)
    density_score = min(100, 50 + abs(white_ratio - 0.5) * 100)
    freq_score = min(100, max(0, (freq_ratio - 0.5) * 40))
    watermark_score = int((density_score * 0.5 + freq_score * 0.5))
    if watermark_score > 65:
        return watermark_score, "Consistent density variation pattern detected — watermark integrity confirmed"
    elif watermark_score > 40:
        return watermark_score, "Partial watermark pattern detected — may be faint or misaligned"
    else:
        return watermark_score, "Watermark pattern not detected — absence typical of counterfeit notes"


def _check_color_profile(hsv):
    mean_h = float(np.mean(hsv[:,:,0]))
    mean_s = float(np.mean(hsv[:,:,1]))
    mean_v = float(np.mean(hsv[:,:,2]))
    best_match = ("Unknown", 0)
    for denom, info in PKR_COLORS.items():
        lower = np.array(info["hsv_range"][0])
        upper = np.array(info["hsv_range"][1])
        mask = cv2.inRange(hsv, lower, upper)
        match_pct = float(np.sum(mask > 0) / mask.size * 100)
        if match_pct > best_match[1]:
            best_match = (info["name"], match_pct)
    expected_name, match_pct = best_match
    if match_pct > 40:
        score = min(100, int(50 + match_pct * 1.2))
        detail = f"Color distribution matches {expected_name} specifications (dominant color coverage: {match_pct:.1f}%)"
    elif match_pct > 20:
        score = int(30 + match_pct * 0.8)
        detail = f"Color profile partially consistent with {expected_name} — some deviation in hue/saturation"
    elif match_pct > 5:
        score = int(match_pct * 1.5)
        detail = f"Color profile does not closely match known PKR note specifications — possible counterfeit coloration"
    else:
        score = 10
        detail = "Color profile inconsistent with any known Pakistani currency denomination"
    return score, detail, {"name": expected_name, "match_pct": round(match_pct, 1)}


def _detect_text_regions(gray):
    h, w = gray.shape
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
    char_regions = []
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area < 20 or area > 5000:
            continue
        x, y, cw, ch = stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP], stats[i, cv2.CC_STAT_WIDTH], stats[i, cv2.CC_STAT_HEIGHT]
        if ch > h * 0.6 or cw > w * 0.4:
            continue
        aspect = cw / max(ch, 1)
        if 0.15 < aspect < 1.5:
            char_regions.append({"x": x, "y": y, "w": cw, "h": ch, "area": area})
    char_count = len(char_regions)
    if char_count > 50:
        text_coverage = sum(r["area"] for r in char_regions) / (h * w) * 100
        serial_groups = []
        char_regions.sort(key=lambda r: (r["y"] // 20, r["x"]))
        current_group = []
        for r in char_regions:
            if not current_group:
                current_group.append(r)
            else:
                last = current_group[-1]
                if abs(r["y"] - last["y"]) < 15 and (r["x"] - last["x"] - last["w"]) < 30:
                    current_group.append(r)
                else:
                    if 6 <= len(current_group) <= 12:
                        serial_groups.append(current_group)
                    current_group = [r]
        if 6 <= len(current_group) <= 12:
            serial_groups.append(current_group)
        serial_detected = len(serial_groups) > 0
        serial_str = ""
        if serial_detected:
            serial_str = f"Alphanumeric sequence detected ({sum(len(g) for g in serial_groups)} characters)"
        score = min(100, int(40 + char_count * 0.8 + text_coverage * 2))
        if score > 75:
            detail = f"Text and serial number regions clearly present ({char_count} character components detected)"
        elif score > 45:
            detail = f"Text regions partially detected — some characters may be blurred or missing ({char_count} components)"
        else:
            detail = f"Insufficient text region detection — text may be poorly reproduced ({char_count} components)"
        return score, detail, serial_str, serial_detected
    return max(10, char_count * 2), f"Very few text-like regions detected ({char_count}) — text reproduction likely compromised", "", False


def _analyze_pattern_symmetry(gray):
    h, w = gray.shape
    left = gray[:, :w//2]
    right = gray[:, w//2:]
    right_flipped = cv2.flip(right, 1)
    if left.shape != right_flipped.shape:
        min_w = min(left.shape[1], right_flipped.shape[1])
        left = left[:, :min_w]
        right_flipped = right_flipped[:, :min_w]
    similarity = cv2.matchTemplate(left.astype(np.float32), right_flipped.astype(np.float32), cv2.TM_CCOEFF_NORMED)
    symmetry_score = float(similarity[0][0]) if similarity.size > 0 else 0
    score = int(max(0, min(100, (symmetry_score + 1) * 50)))
    if score > 70:
        return score, f"Design pattern symmetry consistent with genuine banknote layout ({symmetry_score:.2f} correlation)"
    elif score > 45:
        return score, f"Partial pattern symmetry detected — some misalignment in note design ({symmetry_score:.2f})"
    else:
        return score, f"Poor pattern symmetry — design elements misaligned, atypical of genuine currency ({symmetry_score:.2f})"


def _analyze_microtext(gray):
    h, w = gray.shape
    blur5 = cv2.GaussianBlur(gray, (5, 5), 0)
    high_pass = cv2.subtract(gray.astype(float), blur5.astype(float))
    high_freq = np.abs(high_pass)
    _, high_mask = cv2.threshold(high_freq.astype(np.uint8), 15, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    high_mask = cv2.morphologyEx(high_mask, cv2.MORPH_CLOSE, kernel)
    micro_density = float(np.sum(high_mask > 0) / high_mask.size * 100)
    regions = cv2.connectedComponentsWithStats(high_mask, connectivity=8)
    num_regions = regions[0]
    small_regions = 0
    for i in range(1, num_regions):
        area = regions[2][i, cv2.CC_STAT_AREA]
        if 5 < area < 200:
            small_regions += 1
    density_score = min(50, micro_density * 2)
    region_score = min(50, small_regions * 0.1)
    microtext_score = int(density_score + region_score)
    if microtext_score > 65:
        return microtext_score, f"Micro-printing and fine detail clearly preserved ({small_regions} micro-features detected)"
    elif microtext_score > 40:
        return microtext_score, f"Micro-printing partially legible — some fine detail may be lost ({small_regions} features)"
    else:
        return microtext_score, f"Micro-printing not clearly resolved — fine security detail likely missing or blurred ({small_regions} features)"


def _compute_security_scores(all_features, gray, hsv, img):
    scores = {}
    security = {}

    h, w = gray.shape

    sharpness = all_features.get("sharpness", 0)
    if sharpness > 200:
        scores["print_quality"] = 92
    elif sharpness > 100:
        scores["print_quality"] = 78
    elif sharpness > 50:
        scores["print_quality"] = 55
    else:
        scores["print_quality"] = 30

    edge_den = all_features.get("edge_density", 0)
    fine_edge = all_features.get("fine_edge_density", 0)
    contrast = all_features.get("contrast", 0)
    text_entropy = all_features.get("texture_entropy", 0)
    high_freq = all_features.get("high_freq_energy", 0)

    thread_score, thread_detail = _detect_security_thread(gray)
    scores["security_thread"] = thread_score
    security["security_thread"] = {"detected": thread_score > 50, "score": thread_score, "details": thread_detail}

    color_score, color_detail, color_info = _check_color_profile(hsv)
    scores["color_accuracy"] = color_score
    security["color_profile"] = {"expected": color_info["name"], "score": color_score, "match_pct": color_info["match_pct"], "details": color_detail}

    watermark_score, watermark_detail = _detect_watermark_pattern(gray)
    scores["watermark_integrity"] = watermark_score
    security["watermark"] = {"detected": watermark_score > 50, "score": watermark_score, "details": watermark_detail}

    if text_entropy > 5:
        texture_score = 88
    elif text_entropy > 4:
        texture_score = 72
    elif text_entropy > 3:
        texture_score = 50
    else:
        texture_score = 30
    scores["texture_authenticity"] = texture_score

    pattern_score, pattern_detail = _analyze_pattern_symmetry(gray)
    scores["pattern_symmetry"] = pattern_score
    security["pattern"] = {"score": pattern_score, "details": pattern_detail}

    micro_score, micro_detail = _analyze_microtext(gray)
    scores["microtext_clarity"] = micro_score
    security["microtext"] = {"detected": micro_score > 50, "score": micro_score, "details": micro_detail}

    text_score, text_detail, serial_str, serial_detected = _detect_text_regions(gray)
    scores["serial_presence"] = text_score
    security["serial_number"] = {"detected": serial_detected, "value": serial_str, "score": text_score, "details": text_detail}

    return scores, security


def _generate_detailed_reasons(scores: dict, security: dict, label: str) -> list[str]:
    reasons = []
    score_keys = list(scores.keys())
    avg_score = sum(scores.get(k, 0) for k in score_keys) / max(len(score_keys), 1)

    if label == "REAL":
        for key, info in security.items():
            score = info.get("score", 0)
            if score >= 70:
                reasons.append(f"{info.get('details', '')}")
        if scores.get("print_quality", 0) >= 70:
            reasons.append("High print quality with crisp detail consistent with intaglio printing process")
        if scores.get("texture_authenticity", 0) >= 65:
            reasons.append("Natural paper texture and fiber composition match genuine currency stock")
        if not reasons or len(reasons) < 2:
            reasons.append("Overall feature profile strongly consistent with authentic Pakistani banknote")
    else:
        for key, info in security.items():
            score = info.get("score", 0)
            if score <= 40:
                reasons.append(f"{info.get('details', '')}")
            elif score <= 55:
                reasons.append(f"{info.get('details', '')}")
        if scores.get("print_quality", 0) <= 45:
            reasons.append("Substandard print quality indicates counterfeit reproduction method")
        if scores.get("texture_authenticity", 0) <= 45:
            reasons.append("Paper texture anomalies suggest substitute or synthetic material")
        if not reasons or len(reasons) < 2:
            reasons.append("Multiple feature anomalies detected — ensemble model consensus indicates counterfeit classification")

    return reasons


def predict_image(image_path):
    model = _load_model()
    img_array = _preprocess_image(image_path)

    all_features = _extract_features(image_path) or {}

    img = cv2.imread(image_path)
    if img is None:
        return {
            "label": "UNCERTAIN", "confidence": 50.0, "denomination": "Unknown",
            "serial_number": None, "features": {}, "feature_scores": {},
            "security_analysis": {}, "reasons": ["Unable to read image file"],
        }
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    feature_scores, security_analysis = _compute_security_scores(all_features, gray, hsv, img)

    result = {
        "label": "FAKE",
        "confidence": MIN_CONFIDENCE,
        "denomination": "Unknown",
        "serial_number": None,
        "features": _analyze_features(image_path),
        "feature_scores": feature_scores,
        "security_analysis": security_analysis,
        "reasons": _generate_detailed_reasons(feature_scores, security_analysis, "FAKE"),
    }

    if model is not None and img_array is not None:
        pred = model.predict(img_array, verbose=0)
        confidence = float(pred[0][0])
        if confidence > 0.5:
            label = "REAL"
            result["label"] = label
            result["confidence"] = round(max(confidence * 100, MIN_CONFIDENCE), 1)
        else:
            label = "FAKE"
            result["confidence"] = round(max((1 - confidence) * 100, MIN_CONFIDENCE), 1)
        result["reasons"] = _generate_detailed_reasons(feature_scores, security_analysis, label)
        return result

    torch_input = _preprocess_torch(image_path)
    if _load_torch_model() and torch_input is not None:
        import torch
        with torch.no_grad():
            pred = _global_torch_model(torch_input).item()
        if pred > 0.5:
            label = "REAL"
            result["label"] = label
            result["confidence"] = round(max(pred * 100, MIN_CONFIDENCE), 1)
        else:
            label = "FAKE"
            result["confidence"] = round(max((1 - pred) * 100, MIN_CONFIDENCE), 1)
        result["reasons"] = _generate_detailed_reasons(feature_scores, security_analysis, label)
        return result

    if _load_sklearn_model():
        sk_result = _predict_sklearn(image_path)
        if sk_result is not None:
            label, confidence = sk_result
            result["label"] = label
            result["confidence"] = round(confidence, 1)
            result["reasons"] = _generate_detailed_reasons(feature_scores, security_analysis, label)
            return result

    if _load_yolo_model():
        try:
            yolo_results = _global_yolo_model(image_path, verbose=False)
            top1_idx = int(yolo_results[0].probs.top1)
            conf = float(yolo_results[0].probs.top1conf)
            label = "REAL" if top1_idx == 1 else "FAKE"
            result["label"] = label
            result["confidence"] = round(max(conf * 100, MIN_CONFIDENCE), 1)
            result["reasons"] = _generate_detailed_reasons(feature_scores, security_analysis, label)
            return result
        except Exception:
            pass

    result["label"] = "UNCERTAIN"
    result["confidence"] = 50.0
    result["reasons"] = ["Unable to extract sufficient features — classification inconclusive based on available data"]
    return result
