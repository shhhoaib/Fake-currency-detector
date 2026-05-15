"use client"

import { motion } from "framer-motion"

const features = [
  {
    icon: "⬡",
    title: "WATERMARK SCAN",
    desc: "Deep learning analysis of Quaid-e-Azam watermark portrait for facial feature matching and edge integrity",
    color: "text-primary-container",
  },
  {
    icon: "◈",
    title: "SECURITY THREAD",
    desc: "Color-shifting thread pattern recognition with spectral analysis for denomination verification",
    color: "text-secondary-container",
  },
  {
    icon: "◇",
    title: "MICROTEXT ANALYSIS",
    desc: "Sub-pixel resolution text clarity verification detecting non-intaglio printing anomalies",
    color: "text-primary",
  },
  {
    icon: "○",
    title: "UV FLUORESCENCE",
    desc: "Ultraviolet response mapping to detect counterfeit inks that lack proper fluorescent properties",
    color: "text-secondary-container",
  },
  {
    icon: "□",
    title: "SERIAL VALIDATION",
    desc: "Serial number format verification against SBP issued patterns and checksum algorithms",
    color: "text-primary-container",
  },
  {
    icon: "△",
    title: "RAISED PRINT 3D",
    desc: "Intaglio print depth analysis using shading gradients to verify tactile security elements",
    color: "text-primary",
  },
]

export default function SecurityFeatures() {
  return (
    <section className="mb-12">
      <div className="flex items-center gap-4 mb-8">
        <div className="h-px bg-outline-variant flex-1"></div>
        <h2 className="font-display text-headline-lg text-primary uppercase tracking-widest whitespace-nowrap">
          🛡 SECURITY_OPS
        </h2>
        <div className="h-px bg-outline-variant flex-1"></div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-gutter">
        {features.map((f, i) => (
          <motion.div
            key={f.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            viewport={{ once: true }}
            className="glass-panel p-container-padding relative group hover:border-primary/50 transition-all cursor-default"
          >
            <div className="corner-bracket corner-tl border-primary/30 group-hover:border-primary-container transition-colors"></div>
            <div className="corner-bracket corner-tr border-primary/30 group-hover:border-primary-container transition-colors"></div>
            <div className="corner-bracket corner-bl border-primary/30 group-hover:border-primary-container transition-colors"></div>
            <div className="corner-bracket corner-br border-primary/30 group-hover:border-primary-container transition-colors"></div>

            <div className="flex items-start gap-4">
              <span className={`text-2xl ${f.color} group-hover:scale-110 transition-transform`}>{f.icon}</span>
              <div>
                <h3 className={`font-mono text-label-sm ${f.color} uppercase mb-2`}>{f.title}</h3>
                <p className="font-mono text-[11px] text-on-surface-variant leading-relaxed">{f.desc}</p>
              </div>
            </div>

            <div className="absolute bottom-2 right-2">
              <span className="font-mono text-[8px] text-outline uppercase">NODE_{String(i + 1).padStart(3, "0")}</span>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  )
}
