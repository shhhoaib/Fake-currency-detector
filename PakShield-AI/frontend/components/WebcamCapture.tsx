"use client"

import { useRef, useState, useCallback, useEffect } from "react"

interface WebcamCaptureProps {
  onCapture: (file: File) => void
  scanning: boolean
}

type FacingMode = "user" | "environment"

export default function WebcamCapture({ onCapture, scanning }: WebcamCaptureProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [stream, setStream] = useState<MediaStream | null>(null)
  const [captured, setCaptured] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [active, setActive] = useState(false)
  const [requested, setRequested] = useState(false)
  const [facingMode, setFacingMode] = useState<FacingMode>("environment")
  const [torchOn, setTorchOn] = useState(false)
  const [torchSupported, setTorchSupported] = useState(false)

  const startCamera = useCallback(async (facing: FacingMode) => {
    setError(null)
    try {
      const s = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: facing, width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false,
      })
      setStream(s)
      setActive(true)
      setTorchOn(false)
      setTorchSupported(false)
      if (videoRef.current) videoRef.current.srcObject = s

      const track = s.getVideoTracks()[0]
      if (track) {
        const capabilities: any = track.getCapabilities?.()
        if (capabilities && typeof capabilities.torch === "boolean") {
          setTorchSupported(true)
        }
      }
    } catch (err: any) {
      setRequested(false)
      if (err?.name === "NotAllowedError") {
        setError("Camera access denied — allow camera permission in your browser settings")
      } else if (err?.name === "NotFoundError") {
        setError("No camera found on this device")
      } else {
        setError(err?.message || "Camera access denied")
      }
    }
  }, [])

  const handleStart = useCallback(() => {
    if (requested) return
    setRequested(true)
    startCamera(facingMode)
  }, [requested, startCamera, facingMode])

  const toggleCamera = useCallback(() => {
    const next: FacingMode = facingMode === "environment" ? "user" : "environment"
    setFacingMode(next)
    if (stream) {
      stream.getTracks().forEach((t) => t.stop())
      setStream(null)
    }
    setActive(false)
    setCaptured(null)
    startCamera(next)
  }, [facingMode, stream, startCamera])

  const toggleTorch = useCallback(async () => {
    if (!stream) return
    const track = stream.getVideoTracks()[0]
    if (!track) return
    try {
      await track.applyConstraints({ advanced: [{ torch: !torchOn }] as any })
      setTorchOn(!torchOn)
    } catch {
      // torch not supported on this device
    }
  }, [stream, torchOn])

  const stopCamera = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach((t) => t.stop())
      setStream(null)
    }
    setActive(false)
    setCaptured(null)
    setRequested(false)
    setTorchOn(false)
  }, [stream])

  const capture = useCallback(() => {
    const video = videoRef.current
    const canvas = canvasRef.current
    if (!video || !canvas) return
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const ctx = canvas.getContext("2d")
    if (!ctx) return
    if (facingMode === "user") {
      ctx.translate(canvas.width, 0)
      ctx.scale(-1, 1)
    }
    ctx.drawImage(video, 0, 0)
    const dataUrl = canvas.toDataURL("image/jpeg", 0.92)
    setCaptured(dataUrl)
    canvas.toBlob((blob) => {
      if (blob) onCapture(new File([blob], "webcam_capture.jpg", { type: "image/jpeg" }))
    }, "image/jpeg", 0.92)
  }, [onCapture, facingMode])

  useEffect(() => {
    return () => {
      if (stream) stream.getTracks().forEach((t) => t.stop())
    }
  }, [stream])

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-3 text-center p-4">
        <span className="text-4xl text-error">⚠</span>
        <p className="font-mono text-[10px] text-error">{error}</p>
        <button
          onClick={handleStart}
          className="bg-primary/20 border border-primary text-primary px-3 py-1 font-mono text-[10px] uppercase hover:bg-primary/30"
        >
          RETRY
        </button>
      </div>
    )
  }

  if (!active) {
    return (
      <button
        onClick={handleStart}
        className="flex flex-col items-center justify-center h-full w-full gap-3 bg-transparent border-0 cursor-pointer"
      >
        <span className="text-4xl text-primary/50">📷</span>
        <p className="font-mono text-[10px] text-primary/50 uppercase">TAP TO START CAMERA</p>
      </button>
    )
  }

  return (
    <div className="relative w-full h-full flex items-center justify-center">
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className={`w-full h-full object-contain ${facingMode === "user" ? "scale-x-[-1]" : ""}`}
      />
      <canvas ref={canvasRef} className="hidden" />
      {captured && (
        <img
          src={captured}
          alt="Captured"
          className={`absolute inset-0 w-full h-full object-contain z-10 ${facingMode === "user" ? "scale-x-[-1]" : ""}`}
        />
      )}
      <div className="corner-bracket corner-tl"></div>
      <div className="corner-bracket corner-tr"></div>
      <div className="corner-bracket corner-bl"></div>
      <div className="corner-bracket corner-br"></div>

      <div className="absolute top-3 left-1/2 -translate-x-1/2 flex gap-3 z-20">
        <button
          onClick={toggleCamera}
          className="w-9 h-9 rounded-full bg-black/60 border border-primary/50 flex items-center justify-center hover:bg-primary/20 transition"
          title="Switch camera"
        >
          <span className="text-sm text-primary">🔄</span>
        </button>
        {torchSupported && (
          <button
            onClick={toggleTorch}
            className={`w-9 h-9 rounded-full border flex items-center justify-center transition ${
              torchOn ? "bg-yellow-500/30 border-yellow-400" : "bg-black/60 border-primary/50 hover:bg-primary/20"
            }`}
            title={torchOn ? "Turn flash off" : "Turn flash on"}
          >
            <span className={`text-sm ${torchOn ? "text-yellow-300" : "text-primary"}`}>⚡</span>
          </button>
        )}
      </div>

      <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-3 z-20">
        {!captured ? (
          <button
            onClick={capture}
            disabled={scanning}
            className="w-14 h-14 rounded-full border-2 border-primary bg-black/60 flex items-center justify-center hover:bg-primary/20 transition disabled:opacity-50"
          >
            <div className="w-9 h-9 rounded-full bg-primary"></div>
          </button>
        ) : (
          <button
            onClick={() => setCaptured(null)}
            className="bg-primary/20 border border-primary text-primary px-3 py-1.5 font-mono text-[10px] uppercase hover:bg-primary/30"
          >
            RETAKE
          </button>
        )}
        <button
          onClick={stopCamera}
          className="bg-error/20 border border-error text-error px-3 py-1.5 font-mono text-[10px] uppercase hover:bg-error/30"
        >
          CLOSE
        </button>
      </div>
      {scanning && <div className="scanline"></div>}
    </div>
  )
}
