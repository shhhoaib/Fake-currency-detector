"use client"

import { useEffect, useState } from "react"
import { currencyAPI } from "@/lib/api"

interface Rate {
  rate: number
  change: number
  direction: "up" | "down" | "flat"
}

export default function Ticker() {
  const [rates, setRates] = useState<Record<string, Rate>>({
    USD_PKR: { rate: 278.45, change: 0.12, direction: "up" },
    EUR_PKR: { rate: 302.15, change: 0.21, direction: "up" },
    GBP_PKR: { rate: 351.20, change: 0.08, direction: "up" },
    AED_PKR: { rate: 75.82, change: -0.04, direction: "down" },
    SAR_PKR: { rate: 74.24, change: 0.00, direction: "flat" },
    CNY_PKR: { rate: 38.45, change: -0.15, direction: "down" },
  })

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await currencyAPI.rates()
        setRates(res.data.rates)
      } catch {}
    }
    fetch()
    const interval = setInterval(fetch, 30000)
    return () => clearInterval(interval)
  }, [])

  const renderRate = (key: string, data: Rate) => {
    const label = key.replace("_", "/")
    const arrow = data.direction === "up" ? "▲" : data.direction === "down" ? "▼" : "■"
    const color = data.direction === "up" ? "text-primary" : data.direction === "down" ? "text-error" : "text-on-surface-variant"
    return (
      <span key={key} className="mx-6">
        {label}: {data.rate.toFixed(2)}{" "}
        <span className={color}>
          {arrow} {data.direction !== "flat" ? `${data.change > 0 ? "+" : ""}${data.change.toFixed(2)}%` : "0.00%"}
        </span>
      </span>
    )
  }

  return (
    <div className="w-full glass-panel border-primary/20 py-2 mb-8 overflow-hidden shadow-[0_0_10px_rgba(0,241,253,0.1)]">
      <div className="ticker-wrap flex items-center">
        <div className="flex items-center gap-2 px-4 border-r border-primary/20 bg-primary/10 text-primary font-mono text-[10px] shrink-0">
          <span className="w-2 h-2 rounded-full bg-error live-feed-pulse"></span>
          LIVE_FLUX
        </div>
        <div className="ticker-content font-mono text-[10px] text-secondary-fixed tracking-widest uppercase">
          {Object.entries(rates).map(([key, data]) => renderRate(key, data))}
        </div>
      </div>
    </div>
  )
}
