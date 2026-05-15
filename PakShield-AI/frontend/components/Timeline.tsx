"use client"

import { useEffect, useState } from "react"
import { motion } from "framer-motion"
import { currencyAPI } from "@/lib/api"

interface TimelineEvent {
  year: number
  event: string
  type: string
}

export default function Timeline() {
  const [events, setEvents] = useState<TimelineEvent[]>([])

  useEffect(() => {
    currencyAPI.timeline().then((res) => setEvents(res.data.events)).catch(() => {})
  }, [])

  const typeColor = (type: string) => {
    const colors: Record<string, string> = {
      milestone: "text-primary-container border-primary-container",
      change: "text-secondary-container border-secondary-container",
      new_denomination: "text-primary border-primary",
      security_upgrade: "text-secondary-container border-secondary-container",
      redesign: "text-primary-container border-primary-container",
      innovation: "text-primary border-primary",
      commemorative: "text-secondary-container border-secondary-container",
      event: "text-on-surface-variant border-outline",
    }
    return colors[type] || "text-on-surface border-outline"
  }

  if (events.length === 0) return null

  return (
    <section className="mb-12">
      <div className="flex items-center gap-4 mb-8">
        <div className="h-px bg-outline-variant flex-1"></div>
        <h2 className="font-display text-headline-lg text-primary uppercase tracking-widest whitespace-nowrap">
          ⏳ CURRENCY_TIMELINE
        </h2>
        <div className="h-px bg-outline-variant flex-1"></div>
      </div>

      <div className="glass-panel p-container-padding">
        <div className="relative">
          <div className="absolute left-6 top-0 bottom-0 w-px bg-gradient-to-b from-primary-container via-secondary-container to-primary"></div>

          <div className="space-y-0">
            {events.map((ev, i) => (
              <motion.div
                key={`${ev.year}-${i}`}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                viewport={{ once: true }}
                className="relative pl-16 pb-8 last:pb-0"
              >
                <div className={`absolute left-4 w-4 h-4 rounded-full border-2 bg-surface ${typeColor(ev.type)}`}></div>
                <div className="flex items-start gap-4">
                  <span className="font-display text-headline-md text-primary-container shrink-0">{ev.year}</span>
                  <div>
                    <p className="font-mono text-[12px] text-on-surface-variant leading-relaxed">{ev.event}</p>
                    <span className={`font-mono text-[8px] uppercase tracking-widest ${typeColor(ev.type).split(" ")[0]}`}>
                      {ev.type.replace("_", " ")}
                    </span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
