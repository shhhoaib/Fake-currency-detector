# PakShield AI — Fake Pakistani Currency Detector

An AI-powered end-to-end system for detecting counterfeit Pakistani banknotes using deep learning, computer vision, and ensemble model inference. The system combines a **Next.js frontend** with a **FastAPI backend** and multiple ML models (CNN, YOLO, scikit-learn) to analyze currency security features in real-time.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Docker (Optional)](#docker-optional)
- [Usage](#usage)
- [ML Pipeline](#ml-pipeline)
  - [Models Used](#models-used)
  - [Training Scripts](#training-scripts)
- [API Endpoints](#api-endpoints)
- [Design System](#design-system)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

PakShield AI is a **monetary vigilance system** built to help verify the authenticity of Pakistani Rupee (PKR) banknotes. Users can upload an image or use a live webcam feed to scan a banknote. The system then:

1. Preprocesses the image and extracts 100+ handcrafted features (sharpness, edge density, color histograms, texture entropy, etc.).
2. Runs inference through an ensemble of models (TensorFlow CNN, PyTorch TinyCNN, scikit-learn classifier, YOLOv8-cls).
3. Returns a verdict: **AUTHENTIC** or **COUNTERFEIT**, along with a confidence score and detailed feature analysis.
4. Logs the scan history and provides live currency exchange rates via a ticker.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                │
│  localhost:3000                                      │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────┐  │
│  │   Pages  │  │Components │  │  State (Zustand) │  │
│  │  /detect │  │ AIScanner │  │  auth store      │  │
│  │ /dashboard│  │ Webcam    │  └──────────────────┘  │
│  └──────────┘  │ Chatbot   │                        │
│                └───────────┘                        │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP (axios)
                       ▼
┌─────────────────────────────────────────────────────┐
│               Backend (FastAPI)                      │
│  localhost:8000                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Routers  │  │Services  │  │   ML Engine      │  │
│  │ /detect  │  │  Image   │  │ ┌──────────────┐ │  │
│  │ /chat    │  │  Feature │  │ │ TensorFlow   │ │  │
│  │ /history │  │  Extractor│ │ │ CNN          │ │  │
│  │ /currency│  └──────────┘  │ ├──────────────┤ │  │
│  └──────────┘               │ │ PyTorch      │ │  │
│  ┌──────────┐               │ │ TinyCNN      │ │  │
│  │Database  │               │ ├──────────────┤ │  │
│  │(SQLite)  │               │ │ scikit-learn │ │  │
│  └──────────┘               │ │ (ensemble)   │ │  │
│                              │ ├──────────────┤ │  │
│                              │ │ YOLOv8-cls  │ │  │
│                              │ └──────────────┘ │  │
│                              └──────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## Features

- **Live Webcam Scanning** — Real-time banknote capture with environment-facing camera
- **Image Upload** — Drag-and-drop or file picker for PNG/JPG (max 10MB)
- **Multi-Model Ensemble** — 4 independent ML models vote on authenticity
- **Image Variant Viewer** — Visualize 10 image processing variants (grayscale, edge detection, HSV, LAB, thermal, high-frequency, etc.)
- **Live Currency Ticker** — Real-time PKR exchange rates for USD, EUR, GBP, AED, SAR, CNY
- **AI Chatbot** — Conversational assistant for currency-related questions
- **Scan History Dashboard** — Paginated log of all past scans with results
- **3D Currency Viewer** — Interactive 3D banknote display with hover rotation
- **Detailed Feature Analysis** — Bar charts comparing microtext, watermark, serial number, UV fluorescence, etc.
- **Cybernetic HUD Design** — Glassmorphism UI with scanlines, corner brackets, and neon accents

---

## Tech Stack

### Frontend
| Library          | Purpose                    |
|------------------|----------------------------|
| Next.js 14       | React framework (SSR/SSG)  |
| React 18         | UI components              |
| Tailwind CSS 3   | Utility-first styling      |
| Framer Motion    | Animations & transitions   |
| Recharts         | Charts & data viz          |
| Zustand          | State management           |
| Axios            | HTTP client                |
| react-hot-toast  | Notifications              |

### Backend
| Library          | Purpose                    |
|------------------|----------------------------|
| FastAPI          | REST API framework         |
| Uvicorn          | ASGI server                |
| SQLAlchemy 2.0   | ORM (async)                |
| SQLite           | Development database       |
| OpenCV           | Image processing           |
| Pillow           | Image manipulation         |
| scikit-learn     | ML classifier              |
| PyTorch          | TinyCNN model              |
| TensorFlow       | CNN model                  |
| Ultralytics      | YOLOv8 classification      |
| Pydantic         | Data validation            |

### ML Training
| Library          | Purpose                    |
|------------------|----------------------------|
| TensorFlow 2.14  | CNN training               |
| PyTorch          | TinyCNN training           |
| scikit-learn     | Feature-based classifier   |
| Ultralytics      | YOLOv8-cls training        |
| OpenCV           | Image preprocessing        |

---

## Project Structure

```
FAKE CURRENCY DETECTOR/
├── code.html                          # Static HUD mockup (standalone demo)
├── DESIGN.md                          # Design system documentation
├── Agent.md                           # AI agent development guide
├── screen.png                         # Screenshot
├── dataset/                           # Training dataset
│
└── PakShield-AI/                      # Main application
    ├── docker-compose.yml             # Docker orchestration
    ├── Dockerfile.backend             # Backend container
    ├── Dockerfile.frontend            # Frontend container
    ├── start-backend.bat              # Windows launcher (backend)
    ├── start-frontend.bat             # Windows launcher (frontend)
    │
    ├── backend/                       # FastAPI backend
    │   ├── main.py                    # App entry point
    │   ├── run.py                     # Server runner
    │   ├── seed.py                    # Database seeder
    │   ├── requirements.txt           # Python dependencies
    │   ├── pakshield.db               # SQLite database
    │   ├── .env                       # Environment variables
    │   ├── uploads/                   # Uploaded scan images
    │   └── app/
    │       ├── config.py              # Settings (pydantic)
    │       ├── database.py            # DB engine & session
    │       ├── models/                # SQLAlchemy models
    │       ├── schemas/               # Pydantic schemas
    │       ├── routers/               # API routes
    │       │   ├── detect.py          # /api/detect endpoints
    │       │   ├── chat.py            # /api/chat endpoints
    │       │   ├── history.py         # /api/history endpoints
    │       │   └── currency.py        # /api/currency endpoints
    │       ├── services/              # Business logic
    │       ├── middleware/            # Auth middleware
    │       └── ml/                    # ML models & predictor
    │           ├── predictor.py       # Ensemble prediction engine
    │           ├── currency_detector.pkl  # scikit-learn model
    │           ├── model_torch.pt     # PyTorch TinyCNN
    │           ├── yolo_cls.pt        # YOLOv8 classification
    │           └── yolo_model/        # YOLO model directory
    │
    ├── frontend/                      # Next.js frontend
    │   ├── next.config.js             # Next.js configuration
    │   ├── tailwind.config.ts         # Tailwind theme (custom colors, spacing, fonts)
    │   ├── tsconfig.json              # TypeScript config
    │   ├── postcss.config.js          # PostCSS config
    │   ├── package.json               # Node dependencies
    │   ├── .env.local                 # Environment variables
    │   ├── public/                    # Static assets
    │   │
    │   ├── app/                       # Next.js App Router
    │   │   ├── layout.tsx             # Root layout (Toaster, fonts)
    │   │   ├── page.tsx               # Home page
    │   │   ├── globals.css            # Global styles & animations
    │   │   ├── detect/page.tsx        # Scanner page
    │   │   └── dashboard/page.tsx     # Dashboard page
    │   │
    │   ├── components/                # React components
    │   │   ├── Navbar.tsx             # Top navigation bar
    │   │   ├── Hero.tsx               # Hero section with stats
    │   │   ├── Ticker.tsx             # Live currency ticker
    │   │   ├── AIScanner.tsx          # Core scanner interface
    │   │   ├── WebcamCapture.tsx      # Webcam integration
    │   │   ├── ImageVariants.tsx      # Image variant viewer
    │   │   ├── Comparison.tsx         # Real vs fake comparison
    │   │   ├── SecurityFeatures.tsx   # Security features grid
    │   │   ├── Currency3D.tsx         # 3D banknote viewer
    │   │   ├── Timeline.tsx           # Currency history timeline
    │   │   ├── Chatbot.tsx            # AI chatbot widget
    │   │   └── Footer.tsx             # Site footer
    │   │
    │   ├── lib/
    │   │   └── api.ts                 # Axios API client
    │   │
    │   └── store/
    │       └── auth.ts                # Zustand auth store
    │
    └── ml/                            # ML training scripts
        ├── requirements.txt           # Python dependencies
        ├── train.py                   # Legacy training script
        ├── train_sklearn.py           # scikit-learn feature-based training
        ├── train_torch.py             # PyTorch TinyCNN training
        ├── train_yolo.py              # YOLOv8 classification training
        ├── train_yolo_fast.py         # YOLO fast training variant
        ├── train_yolo_mini.py         # YOLO mini dataset training
        ├── train_yolo_pure.py         # YOLO pure training
        ├── preprocess.py              # Dataset preprocessing
        ├── yolo_save.py               # YOLO model export
        ├── best_torch_model.pt        # Best PyTorch checkpoint
        ├── yolov8n-cls.pt             # YOLOv8n-cls base model
        ├── yolov8n-cls.torchscript    # YOLO TorchScript export
        └── torch_confusion_matrix.png # Confusion matrix
```

---

## Installation & Setup

### Prerequisites

- **Node.js** v18+ and **npm**
- **Python** 3.10+
- **Camera** (for webcam scanning)

### Backend Setup

```bash
cd PakShield-AI/backend
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python seed.py            # Seed database with sample data
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Swagger docs at `http://localhost:8000/docs`.

### Frontend Setup

```bash
cd PakShield-AI/frontend
npm install
npm run dev
```

The app will be available at `http://localhost:3000`.

Or use the batch scripts:

```bash
.\PakShield-AI\start-backend.bat
.\PakShield-AI\start-frontend.bat
```

### Docker (Optional)

```bash
cd PakShield-AI
docker-compose up --build
```

For production with PostgreSQL:

```bash
docker-compose --profile prod up --build
```

---

## Usage

1. Open `http://localhost:3000` in your browser.
2. Navigate to the **Scanner** page (`/detect`).
3. Choose **Upload** mode to select an image file, or **Webcam** mode to capture a live photo.
4. Wait for the AI analysis to complete (the terminal panel shows real-time logs).
5. View the result:
   - **AUTHENTIC** (green) — the note passed all security checks.
   - **COUNTERFEIT** (red) — the note shows signs of forgery.
6. Explore **Image Variants** to see different visual analyses (edge detection, UV simulation, etc.).
7. Check the **Dashboard** (`/dashboard`) for scan history and statistics.
8. Use the **AI Chatbot** (bottom-right button) to ask questions about currency detection.

---

## ML Pipeline

### Models Used

| Model              | Framework     | Input              | Description                               |
|--------------------|---------------|--------------------|-------------------------------------------|
| CNN                | TensorFlow    | 224x224 RGB        | Deep convolutional classifier             |
| TinyCNN            | PyTorch       | 64x64 RGB          | Lightweight 3-layer CNN (batch-norm, dropout) |
| Ensemble Classifier| scikit-learn  | 100+ handcrafted features | RandomForest/GradientBoosting ensemble |
| YOLOv8-cls         | Ultralytics   | 224x224 RGB        | State-of-the-art classification model    |

### Prediction Flow (predictor.py)

1. **TensorFlow CNN** — primary predictor if model is available
2. **PyTorch TinyCNN** — fallback if TensorFlow unavailable
3. **scikit-learn ensemble** — feature-based prediction (sharpness, edge density, color histograms, texture entropy, etc.)
4. **YOLOv8-cls** — final fallback
5. If all models fail → returns `UNCERTAIN` with 50% confidence

### Training Scripts

Located in `ml/`:

| Script               | Description                                |
|----------------------|--------------------------------------------|
| `train_sklearn.py`   | Trains feature-based classifier (RandomForest etc.) |
| `train_torch.py`     | Trains PyTorch TinyCNN                     |
| `train_yolo.py`      | Trains YOLOv8 classification model         |
| `train_yolo_fast.py` | YOLO training optimized for speed          |
| `train_yolo_mini.py` | YOLO training on mini dataset              |
| `train_yolo_pure.py` | Pure YOLO training                         |
| `preprocess.py`      | Dataset preprocessing & augmentation       |
| `yolo_save.py`       | Export YOLO model to TorchScript           |

### Extracted Features (100+)

- **Sharpness** — Laplacian variance
- **Edge Density** — Canny edge detection at multiple thresholds
- **Gradient Magnitude** — Sobel X/Y mean & std
- **Brightness / Contrast** — Grayscale mean & std
- **Color Channels** — RGB / HSV / LAB mean & std
- **Color Histograms** — 32-bin histograms per RGB channel
- **Texture Entropy** — 16x16 gray texture grid entropy
- **High-Frequency Energy** — High-pass filter magnitude
- **Pixel Thresholds** — Percentage of pixels above 50/100/150

---

## API Endpoints

| Method | Endpoint                 | Description                       |
|--------|--------------------------|-----------------------------------|
| GET    | `/api/health`            | Health check                      |
| POST   | `/api/detect`            | Upload image for authenticity scan|
| POST   | `/api/detect/variants`   | Generate image processing variants|
| POST   | `/api/chat`              | Send message to AI chatbot        |
| GET    | `/api/chat/history`      | Get chat history                  |
| GET    | `/api/history`           | Get paginated scan history        |
| GET    | `/api/currency/timeline` | Get PKR currency timeline events  |
| GET    | `/api/currency/denominations` | Get PKR denomination data    |
| GET    | `/api/currency/rates`    | Get live exchange rates           |

---

## Design System

The UI follows a **Cyberpunk HUD** design language:

- **Dark Theme** — #050505 canvas with 24px grid overlay
- **Glassmorphism** — Backdrop blur panels with subtle borders
- **Neon Accents** — Green (authentic), Cyan (data), Red (counterfeit)
- **Typography** — Space Grotesk (headlines) + JetBrains Mono (data)
- **Animations** — Scanlines, ticker scroll, pulse effects, hover 3D rotation

Full design documentation is in [`DESIGN.md`](./DESIGN.md).

---

## Troubleshooting

### Frontend Issues

| Problem                          | Likely Cause                                | Solution                                    |
|----------------------------------|---------------------------------------------|---------------------------------------------|
| "SUSPICIOUS" always shown        | Opening `code.html` directly                | Use the Next.js app at `localhost:3000`     |
| Backend connection refused       | Backend not running / wrong API URL         | Start backend, check `NEXT_PUBLIC_API_URL`  |
| Webcam not working               | Browser permissions / missing camera        | Allow camera access, check `facingMode`     |
| Build fails                      | Missing dependencies / TypeScript errors    | Run `npm install`, check `tsc --noEmit`     |
| Images not loading               | Next.js image config                        | Using `<img>` tags (not `next/image`)       |

### Backend Issues

| Problem                          | Likely Cause                                | Solution                                    |
|----------------------------------|---------------------------------------------|---------------------------------------------|
| No ML models loaded              | Model files missing / wrong path            | Train models or copy `.pt/.pkl` files       |
| "UNCERTAIN" prediction           | All models failed to load                   | Check backend logs, ensure model paths      |
| CORS error                       | Origin mismatch                             | Update `CORS_ORIGINS` in `.env`             |
| Upload fails                     | Missing `uploads/` directory                | Directory created automatically on startup  |

### ML Issues

| Problem                          | Likely Cause                                | Solution                                    |
|----------------------------------|---------------------------------------------|---------------------------------------------|
| Low accuracy                     | Small dataset / poor quality images         | Collect more real/fake samples, augment     |
| Model not found                  | Training not run / path mismatch            | Run training scripts from `ml/` directory   |
| TorchScript load fails           | PyTorch version mismatch                    | Re-export with compatible PyTorch version   |

---

## License

This project is for educational and verification assistance purposes. Always consult the State Bank of Pakistan for official currency validation.
