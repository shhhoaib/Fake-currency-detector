"use client"

import { motion } from "framer-motion"

const denominations = [
  { value: "Rs. 10", color: "bg-emerald-500", desc: "Jinnah's portrait, landmark vignette" },
  { value: "Rs. 20", color: "bg-orange-500", desc: "Green-orange, Khojak Tunnel" },
  { value: "Rs. 50", color: "bg-purple-500", desc: "Purple, Khunjerab Pass" },
  { value: "Rs. 100", color: "bg-red-500", desc: "Red, Quaid-e-Azam Residency" },
  { value: "Rs. 500", color: "bg-sky-600", desc: "Deep green, Badshahi Mosque" },
  { value: "Rs. 1000", color: "bg-blue-700", desc: "Blue, Islamia College" },
  { value: "Rs. 5000", color: "bg-yellow-600", desc: "Mustard green, Faisal Mosque" },
]

const securityFeatures = [
  { name: "WATERMARK", desc: "Quaid-e-Azam watermark visible when held to light" },
  { name: "SECURITY THREAD", desc: "Embedded metallic thread with denomination text" },
  { name: "MICROTEXT", desc: "Urdu text 'State Bank of Pakistan' in micro-printing" },
  { name: "INTAGLIO PRINT", desc: "Raised ink feel on portrait and numerical values" },
  { name: "UV FLUORESCENCE", desc: "Hidden numerals glow under ultraviolet light" },
  { name: "SEE-THROUGH REGISTER", desc: "Front-back alignment creates complete denomination" },
]

export default function Comparison() {
  return (
    <section className="mb-12">
      <div className="flex items-center gap-4 mb-8">
        <div className="h-px bg-outline-variant flex-1"></div>
        <h2 className="font-display text-headline-lg text-primary uppercase tracking-widest whitespace-nowrap">
          ₨ PAKISTANI CURRENCY
        </h2>
        <div className="h-px bg-outline-variant flex-1"></div>
      </div>

      <div className="glass-panel p-container-padding">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-5">
            <h3 className="font-mono text-label-sm text-secondary-fixed mb-2 uppercase">CIRCULATING NOTES</h3>
            <div className="grid grid-cols-2 gap-2">
              {denominations.map((d, i) => (
                <motion.div
                  key={d.value}
                  initial={{ opacity: 0, y: 10 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.08 }}
                  viewport={{ once: true }}
                  className="bg-black/40 border border-outline-variant/30 rounded p-3 flex items-center gap-3"
                >
                  <div className={`w-10 h-6 rounded ${d.color} opacity-80 shrink-0 flex items-center justify-center text-[8px] font-bold text-black`}>
                    {d.value}
                  </div>
                  <div>
                    <span className="font-mono text-[11px] text-primary">{d.value}</span>
                    <p className="font-mono text-[9px] text-on-surface-variant mt-0.5">{d.desc}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          <div className="flex flex-col justify-center border-l border-outline-variant/30 pl-8">
            <h3 className="font-mono text-label-sm text-secondary-fixed mb-4 uppercase">SECURITY_FEATURES</h3>
            <ul className="space-y-3 font-mono text-[11px] text-on-surface-variant">
              {securityFeatures.map((sf, i) => (
                <motion.li
                  key={sf.name}
                  initial={{ opacity: 0, x: 10 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 }}
                  viewport={{ once: true }}
                  className="flex gap-2 items-start"
                >
                  <span className="text-primary-container mt-0.5">◈</span>
                  <div>
                    <span className="text-primary uppercase">{sf.name}</span>
                    <p className="text-[10px] mt-0.5">{sf.desc}</p>
                  </div>
                </motion.li>
              ))}
            </ul>
            <div className="mt-6 pt-4 border-t border-outline-variant/20">
              <p className="font-mono text-[9px] text-on-surface-variant uppercase leading-relaxed">
                Issued by <span className="text-primary">State Bank of Pakistan</span> — Urdu text & numerical values appear on all genuine notes.
                The SBP introduced enhanced security features in the 2006 & 2011 series to combat counterfeiting.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
