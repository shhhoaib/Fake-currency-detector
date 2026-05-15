"use client"

import { motion } from "framer-motion"

const features = [
  { name: "SERIAL NUMBER PATTERN", real: 95, fake: 35 },
  { name: "WATERMARK INTEGRITY", real: 92, fake: 28 },
  { name: "MICROTEXT CLARITY", real: 88, fake: 45 },
  { name: "SECURITY THREAD", real: 96, fake: 20 },
  { name: "INK FLUORESCENCE", real: 90, fake: 15 },
  { name: "RAISED PRINTING", real: 85, fake: 30 },
]

export default function Comparison() {
  return (
    <section className="mb-12">
      <div className="flex items-center gap-4 mb-8">
        <div className="h-px bg-outline-variant flex-1"></div>
        <h2 className="font-display text-headline-lg text-primary uppercase tracking-widest whitespace-nowrap">
          ⚖ REAL vs FAKE
        </h2>
        <div className="h-px bg-outline-variant flex-1"></div>
      </div>

      <div className="glass-panel p-container-padding">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-4">
            {features.map((f, i) => (
              <motion.div
                key={f.name}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
                viewport={{ once: true }}
              >
                <div className="flex justify-between items-center mb-1">
                  <span className="font-mono text-[10px] text-primary uppercase">{f.name}</span>
                  <span className="font-mono text-[10px] text-on-surface-variant">{f.real}% / {f.fake}%</span>
                </div>
                <div className="flex gap-1 h-3">
                  <div className="flex-1 bg-surface-container-lowest rounded-sm overflow-hidden border border-outline-variant/30">
                    <motion.div
                      initial={{ width: 0 }}
                      whileInView={{ width: `${f.real}%` }}
                      transition={{ duration: 0.8, delay: i * 0.1 }}
                      className="h-full bg-primary-container shadow-[0_0_8px_#39ff14]"
                    />
                  </div>
                  <div className="flex-1 bg-surface-container-lowest rounded-sm overflow-hidden border border-outline-variant/30">
                    <motion.div
                      initial={{ width: 0 }}
                      whileInView={{ width: `${f.fake}%` }}
                      transition={{ duration: 0.8, delay: i * 0.1 }}
                      className="h-full bg-error shadow-[0_0_8px_#ffb4ab]"
                    />
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          <div className="flex flex-col justify-center border-l border-outline-variant/30 pl-8">
            <h3 className="font-mono text-label-sm text-secondary-fixed mb-4 uppercase">AI_OBSERVATIONS</h3>
            <ul className="space-y-3 font-mono text-[11px] text-on-surface-variant">
              <li className="flex gap-2 items-start">
                <span className="text-primary-container mt-0.5">◆</span>
                <span>Real notes show consistent serial number spacing and font alignment</span>
              </li>
              <li className="flex gap-2 items-start">
                <span className="text-primary-container mt-0.5">◆</span>
                <span>Watermark of Quaid-e-Azam has precise facial feature distribution in genuine notes</span>
              </li>
              <li className="flex gap-2 items-start">
                <span className="text-error mt-0.5">◇</span>
                <span>Fake notes exhibit microtext bleeding due to non-intaglio printing methods</span>
              </li>
              <li className="flex gap-2 items-start">
                <span className="text-error mt-0.5">◇</span>
                <span>Security thread pattern mismatch is the strongest indicator of counterfeits</span>
              </li>
              <li className="flex gap-2 items-start">
                <span className="text-error mt-0.5">◇</span>
                <span>UV fluorescence fails to activate in 97% of detected counterfeit samples</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  )
}
