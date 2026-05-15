"use client"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"

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

const VARIANT_LABELS: Record<keyof VariantsData, string> = {
  original: "RGB Original",
  grayscale: "Grayscale",
  red_channel: "Red Channel",
  green_channel: "Green Channel",
  blue_channel: "Blue Channel",
  thermal: "Thermal",
  edge: "Edge Detection",
  hsv: "HSV",
  lab: "LAB",
  high_freq: "High Frequency",
  inverted: "Inverted",
}

const VARIANT_ICONS: Record<keyof VariantsData, string> = {
  original: "◉",
  grayscale: "◎",
  red_channel: "🔴",
  green_channel: "🟢",
  blue_channel: "🔵",
  thermal: "🔥",
  edge: "✧",
  hsv: "🎨",
  lab: "🧪",
  high_freq: "〰",
  inverted: "◐",
}

interface ImageVariantsProps {
  variants: VariantsData
}

export default function ImageVariants({ variants }: ImageVariantsProps) {
  const [active, setActive] = useState<keyof VariantsData>("original")
  const keys = Object.keys(variants) as (keyof VariantsData)[]
  const activeSrc = `data:image/png;base64,${variants[active]}`

  return (
    <div className="mt-4">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-secondary-container text-sm">◈</span>
        <span className="font-mono text-[10px] text-secondary-container uppercase">IMAGE_VARIANTS</span>
      </div>

      <div className="flex flex-wrap gap-1.5 mb-3">
        {keys.map((key: keyof VariantsData) => (
          <button
            key={key}
            onClick={() => setActive(key)}
            className={`px-2 py-1 font-mono text-[9px] uppercase border transition-all ${
              active === key
                ? "bg-secondary-container/20 border-secondary-container text-secondary-container"
                : "bg-black/40 border-outline-variant text-on-surface-variant hover:border-secondary-container/50"
            }`}
          >
            {VARIANT_ICONS[key]} {VARIANT_LABELS[key]}
          </button>
        ))}
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={active}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="relative bg-black/60 rounded border border-primary/20 overflow-hidden aspect-video flex items-center justify-center"
        >
          <img src={activeSrc} alt={VARIANT_LABELS[active]} className="w-full h-full object-contain" />
          <div className="absolute top-2 left-2 bg-black/70 px-2 py-0.5 rounded">
            <span className="font-mono text-[9px] text-secondary-container">{VARIANT_LABELS[active]}</span>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  )
}
