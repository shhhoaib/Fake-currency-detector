"use client"

import { useState, useRef } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { detectAPI } from "@/lib/api"
import toast from "react-hot-toast"
import WebcamCapture from "./WebcamCapture"
import ImageVariants from "./ImageVariants"
import SecurityCharts from "./SecurityCharts"

interface ScanResult {
  result: string
  confidence: number
  denomination?: string
  processing_time_ms?: number
  features?: Record<string, number>
  feature_scores?: Record<string, number>
  security_analysis?: Record<string, any>
  reasons?: string[]
}

interface VariantsData {
  original: string
  grayscale: string
  red_channel: string
  green_channel: string
  blue_channel: string
  thermal: string
  edge: string
  hsv: string
  lab: string
  high_freq: string
  inverted: string
}

export default function AIScanner() {
  const [mode, setMode] = useState<"upload" | "live">("upload")
  const [scanning, setScanning] = useState(false)
  const [result, setResult] = useState<ScanResult | null>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [variants, setVariants] = useState<VariantsData | null>(null)
  const [logs, setLogs] = useState<string[]>([
    "[SYSTEM] Neural weights initialized",
    "[SYSTEM] Waiting for input...",
  ])
  const fileRef = useRef<HTMLInputElement>(null)

  const addLog = (msg: string) => {
    setLogs((prev) => [...prev.slice(-8), msg])
  }

  const processImage = async (file: File) => {
    setResult(null)
    setVariants(null)
    setScanning(true)

    const scanLogs = [
      "[SCAN] Initializing neural analysis...",
      "[SCAN] Loading banknote signature...",
      "[SCAN] Comparing watermark flux vectors...",
      "[SCAN] Analyzing microtext integrity...",
      "[SCAN] Detecting security thread pattern...",
      "[SCAN] Computing authenticity probability...",
    ]
    for (const log of scanLogs) {
      addLog(log)
      await new Promise((r) => setTimeout(r, 400))
    }

    try {
      const [scanRes, varRes] = await Promise.all([
        detectAPI.upload(file),
        detectAPI.variants(file),
      ])
      setResult(scanRes.data)
      setVariants(varRes.data)
      addLog(`[RESULT] Analysis complete: ${scanRes.data.result} (${scanRes.data.confidence.toFixed(1)}%)`)
      toast.success("Scan complete")
    } catch (err: any) {
      addLog("[ERROR] Scan failed")
      toast.error(err?.response?.data?.detail || "Scan failed")
    } finally {
      setScanning(false)
    }
  }

  const handleFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const validTypes = ["image/png", "image/jpeg", "image/jpg"]
    if (!validTypes.includes(file.type)) {
      toast.error("Only PNG, JPG, JPEG allowed")
      return
    }
    if (file.size > 10 * 1024 * 1024) {
      toast.error("File too large (max 10MB)")
      return
    }

    setPreview(URL.createObjectURL(file))
    await processImage(file)
  }

  return (
    <section id="scanner" className="mb-12">
      <div className="flex items-center gap-4 mb-8">
        <div className="h-px bg-outline-variant flex-1"></div>
        <h2 className="font-display text-headline-lg text-primary uppercase tracking-widest whitespace-nowrap">
          ⬡ AI_SCANNER_CORE
        </h2>
        <div className="h-px bg-outline-variant flex-1"></div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter">
        <div className="glass-panel p-container-padding relative overflow-hidden">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <span className="text-secondary-container text-lg">◈</span>
              <span className="font-mono text-label-sm text-primary uppercase">LIVE_SCAN_INTERFACE</span>
            </div>
            <div className="flex items-center gap-2 bg-black/40 px-3 py-1 border border-primary/30 rounded">
              <span className="w-2 h-2 rounded-full bg-error live-feed-pulse"></span>
              <span className="font-mono text-[10px] text-primary">{scanning ? "SCANNING" : "STANDBY"}</span>
            </div>
          </div>

          <div className="flex gap-2 mb-3">
            <button
              onClick={() => { setMode("upload"); setPreview(null); setResult(null); setVariants(null) }}
              className={`px-3 py-1 font-mono text-[9px] uppercase border transition-all ${
                mode === "upload"
                  ? "bg-primary/20 border-primary text-primary"
                  : "bg-black/40 border-outline-variant text-on-surface-variant hover:border-primary/50"
              }`}
            >
              📁 UPLOAD
            </button>
            <button
              onClick={() => { setMode("live"); setPreview(null); setResult(null); setVariants(null) }}
              className={`px-3 py-1 font-mono text-[9px] uppercase border transition-all ${
                mode === "live"
                  ? "bg-primary/20 border-primary text-primary"
                  : "bg-black/40 border-outline-variant text-on-surface-variant hover:border-primary/50"
              }`}
            >
              📷 LIVE SCAN
            </button>
          </div>

          <div className="relative border-2 border-primary rounded overflow-hidden aspect-video bg-black/80 flex items-center justify-center">
            {mode === "upload" ? (
              <>
                <div className="w-full h-full cursor-pointer" onClick={() => fileRef.current?.click()}>
                  {preview ? (
                    <img src={preview} alt="Preview" className="w-full h-full object-contain" />
                  ) : (
                    <div className="flex flex-col items-center justify-center h-full gap-2">
                      <span className="text-4xl text-primary/50">◻</span>
                      <p className="font-mono text-[10px] text-primary/50 uppercase">DROP_IMAGE_HERE</p>
                    </div>
                  )}
                </div>
                {scanning && <div className="scanline"></div>}
                <div className="corner-bracket corner-tl"></div>
                <div className="corner-bracket corner-tr"></div>
                <div className="corner-bracket corner-bl"></div>
                <div className="corner-bracket corner-br"></div>
              </>
            ) : (
              <WebcamCapture onCapture={(file) => { setPreview(null); processImage(file) }} scanning={scanning} key="webcam" />
            )}
          </div>

          {mode === "upload" && (
            <>
              <input ref={fileRef} type="file" accept="image/png,image/jpeg" onChange={handleFile} className="hidden" />
              <div className="mt-4 flex justify-between items-center">
                <button
                  onClick={() => fileRef.current?.click()}
                  disabled={scanning}
                  className="bg-primary/20 border border-primary text-primary px-4 py-1.5 font-mono text-[10px] uppercase hover:bg-primary/30 transition-all disabled:opacity-50"
                >
                  UPLOAD_IMAGE
                </button>
                <div className="font-mono text-[10px] text-on-surface-variant">
                  {result ? `${result.processing_time_ms?.toFixed(0)}ms` : "---"}
                </div>
              </div>
            </>
          )}

          <AnimatePresence>
            {result && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className={`mt-4 p-4 rounded border ${result.result === "REAL" ? "border-primary-container/50 bg-primary-container/10" : "border-error/50 bg-error/10"}`}
              >
                <div className="flex justify-between items-center">
                  <div>
                    <p className="font-mono text-[10px] text-on-surface-variant uppercase">SCAN_RESULT</p>
                    <p className={`font-display text-headline-lg ${result.result === "REAL" ? "text-primary-container" : "text-error"}`}>
                      {result.result === "REAL" ? "AUTHENTIC" : "COUNTERFEIT"}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="font-mono text-[10px] text-on-surface-variant uppercase">CONFIDENCE</p>
                    <p className="font-display text-headline-lg text-on-surface">{result.confidence.toFixed(1)}%</p>
                  </div>
                </div>
                {result.features && (
                  <div className="mt-3 grid grid-cols-2 gap-2 text-[10px] font-mono">
                    {Object.entries(result.features).map(([k, v]) => (
                      <div key={k} className="flex justify-between text-on-surface-variant">
                        <span>{k.toUpperCase()}:</span>
                        <span className="text-primary">{typeof v === "number" ? v.toFixed(2) : v}</span>
                      </div>
                    ))}
                  </div>
                )}
                {result.reasons && result.reasons.length > 0 && (
                  <div className="mt-4 pt-3 border-t border-primary/20">
                    <p className="font-mono text-[10px] text-on-surface-variant uppercase mb-2">ANALYSIS_REASONS</p>
                    <ul className="space-y-1.5">
                      {result.reasons.map((reason, i) => (
                        <li key={i} className="flex items-start gap-2 font-mono text-[10px] leading-relaxed">
                          <span className={`mt-0.5 ${result.result === "REAL" ? "text-primary-container" : "text-error"}`}>▸</span>
                          <span className="text-on-surface-variant">{reason}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {result.feature_scores && result.security_analysis && (
                  <SecurityCharts
                    featureScores={result.feature_scores}
                    securityAnalysis={result.security_analysis}
                    result={result.result}
                  />
                )}
              </motion.div>
            )}
          </AnimatePresence>

          {variants && result && <ImageVariants variants={variants} />}
        </div>

        <div className="bg-surface-container-high p-container-padding rounded border border-primary/20 relative flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <span className="font-mono text-label-sm text-primary uppercase">ANALYSIS_LOGS</span>
            <div className="flex gap-1.5">
              <div className="w-2 h-2 rounded-full bg-primary-container animate-pulse"></div>
              <div className="w-2 h-2 rounded-full bg-secondary-container opacity-50"></div>
            </div>
          </div>
          <div className="bg-black/40 p-4 rounded font-mono text-[11px] text-primary-fixed leading-relaxed flex-1 min-h-[200px] overflow-y-auto">
            {logs.map((log, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className={log.includes("ERROR") ? "text-error" : log.includes("RESULT") ? "text-primary-container" : "text-primary-fixed/80"}
              >
                {log}
              </motion.div>
            ))}
            {scanning && (
              <span className="inline-block w-2 h-4 bg-primary-container animate-pulse ml-1"></span>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}
