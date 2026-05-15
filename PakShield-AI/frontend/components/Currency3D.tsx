"use client"

import { useRef, useState } from "react"
import { motion } from "framer-motion"

const notes = [
  { denom: "5000 PKR", color: "#2d5a27", accent: "#39ff14", year: 1997 },
  { denom: "1000 PKR", color: "#1a3a6b", accent: "#00f1fd", year: 1987 },
  { denom: "100 PKR", color: "#6b2d2d", accent: "#ff6b6b", year: 2006 },
  { denom: "50 PKR", color: "#4a2d6b", accent: "#b388ff", year: 2006 },
]

export default function Currency3D() {
  const [activeNote, setActiveNote] = useState(0)
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })
  const cardRef = useRef<HTMLDivElement>(null)

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!cardRef.current) return
    const rect = cardRef.current.getBoundingClientRect()
    const x = ((e.clientX - rect.left) / rect.width - 0.5) * 20
    const y = ((e.clientY - rect.top) / rect.height - 0.5) * -20
    setMousePos({ x, y })
  }

  const note = notes[activeNote]

  return (
    <section className="mb-12">
      <div className="flex items-center gap-4 mb-8">
        <div className="h-px bg-outline-variant flex-1"></div>
        <h2 className="font-display text-headline-lg text-primary uppercase tracking-widest whitespace-nowrap">
          ◈ 3D_CURRENCY_VIEWER
        </h2>
        <div className="h-px bg-outline-variant flex-1"></div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-gutter">
        <div className="lg:col-span-2 glass-panel p-container-padding relative overflow-hidden">
          <div className="absolute top-2 left-2 font-mono text-[8px] text-primary/40 uppercase tracking-widest">
            RENDER_3D_ACTIVE // FRAME_{activeNote + 1}
          </div>

          <motion.div
            ref={cardRef}
            onMouseMove={handleMouseMove}
            onMouseLeave={() => setMousePos({ x: 0, y: 0 })}
            className="w-full aspect-[3/2] bg-surface-container rounded flex items-center justify-center cursor-pointer relative overflow-hidden"
            style={{
              transform: `perspective(1000px) rotateX(${mousePos.y}deg) rotateY(${mousePos.x}deg)`,
              transition: "transform 0.1s ease-out",
            }}
          >
            <div
              className="absolute inset-4 rounded border-2 flex flex-col items-center justify-center"
              style={{
                borderColor: note.accent,
                background: `linear-gradient(135deg, ${note.color}88, ${note.color}44)`,
                boxShadow: `0 0 40px ${note.accent}44, inset 0 0 40px ${note.accent}22`,
              }}
            >
              <div className="scanline" style={{ background: note.accent, boxShadow: `0 0 20px ${note.accent}` }}></div>
              <span className="font-display text-display-lg text-white/90 drop-shadow-lg">{note.denom}</span>
              <span className="font-mono text-[10px] text-white/50 uppercase tracking-[0.3em] mt-2">
                State Bank of Pakistan
              </span>
              <div className="absolute bottom-6 left-6 w-12 h-12 rounded-full border-2" style={{ borderColor: note.accent }}></div>
              <div className="absolute bottom-6 right-6 w-16 h-8 border" style={{ borderColor: note.accent }}></div>
              <span className="absolute top-6 right-6 font-mono text-[8px]" style={{ color: note.accent }}>
                {note.accent === "#39ff14" ? "AUTHENTIC" : "VERIFIED"}
              </span>
            </div>
          </motion.div>

          <div className="flex gap-2 mt-4 justify-center">
            {notes.map((n, i) => (
              <button
                key={n.denom}
                onClick={() => setActiveNote(i)}
                className={`px-4 py-2 font-mono text-[10px] uppercase rounded border transition-all ${
                  i === activeNote
                    ? "bg-primary-container/20 border-primary-container text-primary-container"
                    : "border-outline-variant text-on-surface-variant hover:text-primary"
                }`}
              >
                {n.denom}
              </button>
            ))}
          </div>
        </div>

        <div className="glass-panel p-container-padding flex flex-col">
          <div className="mb-4">
            <p className="font-mono text-label-sm text-secondary-fixed uppercase mb-1">NOTE_SPECS</p>
            <div className="h-px bg-outline-variant/50"></div>
          </div>
          <div className="space-y-3 flex-1">
            {[
              { label: "DENOMINATION", value: note.denom },
              { label: "ISSUED", value: String(note.year) },
              { label: "SECURITY_CLASS", value: note.accent === "#39ff14" ? "A+" : "A" },
              { label: "CIRCULATION", value: "Active" },
              { label: "DIMENSIONS", value: "175 x 80mm" },
              { label: "MATERIAL", value: "Cotton Paper" },
            ].map((item) => (
              <div key={item.label} className="flex justify-between font-mono text-[11px]">
                <span className="text-on-surface-variant">{item.label}:</span>
                <span className="text-primary">{item.value}</span>
              </div>
            ))}
          </div>
          <div className="mt-4 p-3 bg-black/40 rounded font-mono text-[9px] text-primary/60">
            <span className="text-primary-container">◈</span> INTERACTIVE_3D // HOVER_TO_ROTATE
          </div>
        </div>
      </div>
    </section>
  )
}
