"use client"

import { useRef, useState, useCallback, useEffect } from "react"

interface WebcamCaptureProps {
  onCapture: (file: File) => void
  scanning: boolean
}

export default function WebcamCapture({ onCapture, scanning }: WebcamCaptureProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [stream, setStream] = useState<MediaStream | null>(null)
  const [captured, setCaptured] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [active, setActive] = useState(false)

  const startCamera = useCallback(async () => {
    setError(null)
    try {
      const s = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment", width: { ideal: 1280 }, height: { ideal: 720 } },
        audio: false,
      })
      setStream(s)
      setActive(true)
      if (videoRef.current) videoRef.current.srcObject = s
    } catch (err: any) {
      setError(err?.message || "Camera access denied")
    }
  }, [])

  const stopCamera = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach((t) => t.stop())
      setStream(null)
    }
    setActive(false)
    setCaptured(null)
  }, [stream])

  const capture = useCallback(() => {
    const video = videoRef.current
    const canvas = canvasRef.current
    if (!video || !canvas) return
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    const ctx = canvas.getContext("2d")
    if (!ctx) return
    ctx.drawImage(video, 0, 0)
    const dataUrl = canvas.toDataURL("image/jpeg", 0.92)
    setCaptured(dataUrl)
    canvas.toBlob((blob) => {
      if (blob) onCapture(new File([blob], "webcam_capture.jpg", { type: "image/jpeg" }))
    }, "image/jpeg", 0.92)
  }, [onCapture])

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
          onClick={startCamera}
          className="bg-primary/20 border border-primary text-primary px-3 py-1 font-mono text-[10px] uppercase hover:bg-primary/30"
        >
          RETRY
        </button>
      </div>
    )
  }

  if (!active) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-3 cursor-pointer" onClick={startCamera}>
        <span className="text-4xl text-primary/50">📷</span>
        <p className="font-mono text-[10px] text-primary/50 uppercase">START_CAMERA</p>
      </div>
    )
  }

  return (
    <div className="relative w-full h-full flex items-center justify-center">
      <video ref={videoRef} autoPlay playsInline className="w-full h-full object-contain" />
      <canvas ref={canvasRef} className="hidden" />
      {captured && (
        <img src={captured} alt="Captured" className="absolute inset-0 w-full h-full object-contain z-10" />
      )}
      <div className="corner-bracket corner-tl"></div>
      <div className="corner-bracket corner-tr"></div>
      <div className="corner-bracket corner-bl"></div>
      <div className="corner-bracket corner-br"></div>

      <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-3 z-20">
        {!captured ? (
          <button
            onClick={capture}
            disabled={scanning}
            className="w-12 h-12 rounded-full border-2 border-primary bg-black/60 flex items-center justify-center hover:bg-primary/20 transition disabled:opacity-50"
          >
            <div className="w-8 h-8 rounded-full bg-primary"></div>
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
