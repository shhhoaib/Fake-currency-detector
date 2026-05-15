"use client"

import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import Navbar from "@/components/Navbar"
import Footer from "@/components/Footer"
import Chatbot from "@/components/Chatbot"
import Ticker from "@/components/Ticker"
import { historyAPI, currencyAPI } from "@/lib/api"

interface Scan {
  id: string
  result: string
  confidence: number
  denomination: string | null
  created_at: string
}

export default function DashboardPage() {
  const [scans, setScans] = useState<Scan[]>([])
  const [stats, setStats] = useState({ total: 0, real: 0, fake: 0, avgConfidence: 0 })
  const [rates, setRates] = useState<Record<string, any>>({})

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [histRes, ratesRes] = await Promise.all([
          historyAPI.get(1, 50),
          currencyAPI.rates(),
        ])
        const scanData = histRes.data.scans
        setScans(scanData)
        setRates(ratesRes.data.rates)

        const total = scanData.length
        const real = scanData.filter((s: Scan) => s.result === "REAL").length
        const fake = scanData.filter((s: Scan) => s.result === "FAKE").length
        const avgConf = total > 0 ? scanData.reduce((acc: number, s: Scan) => acc + s.confidence, 0) / total : 0
        setStats({ total, real, fake, avgConfidence: avgConf })
      } catch {}
    }
    fetchData()
  }, [])

  const StatCard = ({ label, value, color }: { label: string; value: string; color: string }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-panel p-4 rounded"
    >
      <p className="font-mono text-[10px] text-on-surface-variant uppercase tracking-widest">{label}</p>
      <p className={`font-display text-headline-lg ${color} mt-1`}>{value}</p>
    </motion.div>
  )

  return (
    <>
      <Navbar />
      <main className="pt-20 pb-20 px-hud-margin min-h-screen max-w-7xl mx-auto">
        <div className="mb-8 pt-8">
          <div className="flex items-center gap-3">
            <span className="text-primary-container text-2xl">⬡</span>
            <div>
              <h1 className="font-display text-headline-lg text-primary uppercase tracking-tighter">
                OPERATOR_DASHBOARD
              </h1>
              <p className="font-mono text-[10px] text-on-surface-variant">
                PUBLIC_ACCESS // TOTAL_SCANS: {stats.total}
              </p>
            </div>
          </div>
        </div>

        <Ticker />

        <div className="grid grid-cols-2 md:grid-cols-4 gap-gutter mb-8">
          <StatCard label="TOTAL_SCANS" value={String(stats.total)} color="text-primary" />
          <StatCard label="AUTHENTIC" value={String(stats.real)} color="text-primary-container" />
          <StatCard label="COUNTERFEIT" value={String(stats.fake)} color="text-error" />
          <StatCard label="AVG_CONFIDENCE" value={`${stats.avgConfidence.toFixed(1)}%`} color="text-secondary-container" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-gutter mb-8">
          <div className="lg:col-span-2 glass-panel p-container-padding">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-mono text-label-sm text-primary uppercase">SCAN_HISTORY</h2>
              <span className="font-mono text-[10px] text-on-surface-variant">{scans.length} records</span>
            </div>
            <div className="space-y-2 max-h-[400px] overflow-y-auto">
              {scans.length === 0 ? (
                <p className="font-mono text-[11px] text-on-surface-variant text-center py-8">No scans yet. Start scanning!</p>
              ) : (
                scans.map((scan, i) => (
                  <motion.div
                    key={scan.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: i * 0.02 }}
                    className={`flex justify-between items-center p-3 rounded border ${
                      scan.result === "REAL" ? "border-primary-container/20 bg-primary-container/5" : "border-error/20 bg-error/5"
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className={`text-lg ${scan.result === "REAL" ? "text-primary-container" : "text-error"}`}>
                        {scan.result === "REAL" ? "◆" : "◇"}
                      </span>
                      <div>
                        <p className="font-mono text-[11px] text-primary">{scan.denomination || "Unknown"}</p>
                        <p className="font-mono text-[9px] text-on-surface-variant">
                          {new Date(scan.created_at).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className={`font-mono text-[11px] ${scan.result === "REAL" ? "text-primary-container" : "text-error"}`}>
                        {scan.result}
                      </p>
                      <p className="font-mono text-[9px] text-on-surface-variant">{scan.confidence.toFixed(1)}%</p>
                    </div>
                  </motion.div>
                ))
              )}
            </div>
          </div>

          <div className="glass-panel p-container-padding">
            <h2 className="font-mono text-label-sm text-primary uppercase mb-4">EXCHANGE_RATES</h2>
            <div className="space-y-3">
              {Object.entries(rates).map(([key, data]: [string, any]) => {
                const label = key.replace("_", "/")
                const arrow = data.direction === "up" ? "▲" : data.direction === "down" ? "▼" : "■"
                const color = data.direction === "up" ? "text-primary-container" : data.direction === "down" ? "text-error" : "text-on-surface-variant"
                return (
                  <div key={key} className="flex justify-between items-center font-mono text-[11px]">
                    <span className="text-on-surface-variant">{label}</span>
                    <div className="flex items-center gap-2">
                      <span className="text-primary">{data.rate.toFixed(2)}</span>
                      <span className={`${color} text-[9px]`}>{arrow} {data.direction !== "flat" ? `${data.change > 0 ? "+" : ""}${data.change.toFixed(2)}%` : "0.00%"}</span>
                    </div>
                  </div>
                )
              })}
            </div>
            <div className="mt-4 pt-4 border-t border-outline-variant/30">
              <p className="font-mono text-[8px] text-outline uppercase tracking-widest text-center">
                BASE: PKR // UPDATED: LIVE
              </p>
            </div>
          </div>
        </div>
      </main>
      <Footer />
      <Chatbot />
    </>
  )
}
