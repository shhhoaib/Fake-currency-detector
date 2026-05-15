"use client"

import { motion } from "framer-motion"
import Link from "next/link"

export default function Hero() {
  return (
    <section className="relative min-h-[80vh] flex items-center">
      <div className="absolute inset-0 hex-grid opacity-30 pointer-events-none"></div>
      <div className="absolute top-20 left-1/4 w-96 h-96 bg-primary-container/5 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-20 right-1/4 w-80 h-80 bg-secondary-container/5 rounded-full blur-[100px] pointer-events-none"></div>

      <div className="relative z-10 w-full">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center lg:text-left lg:max-w-4xl mx-auto px-hud-margin"
        >
          <div className="flex items-center gap-3 mb-6 justify-center lg:justify-start">
            <span className="w-2 h-2 rounded-full bg-error live-feed-pulse"></span>
            <span className="font-mono text-[10px] text-primary tracking-[0.2em] uppercase">
              NEURAL NETWORK ACTIVE // VERSION 1.0.0
            </span>
          </div>

          <h1 className="font-display text-display-lg text-primary mb-4 uppercase leading-[1.1]">
            Detect Fake
            <br />
            <span className="text-primary-container">Pakistani Currency</span>
            <br />
            Instantly
          </h1>

          <p className="font-mono text-body-md text-on-surface-variant max-w-2xl mb-8 mx-auto lg:mx-0">
            AI-powered deep learning engine analyzes banknote security features,
            watermark integrity, and microtext patterns with 99.8% accuracy.
          </p>

          <div className="flex flex-wrap gap-4 justify-center lg:justify-start">
            <Link
              href="/detect"
              className="bg-primary-container text-on-primary font-bold px-8 py-3 rounded uppercase tracking-widest text-sm hover:opacity-90 active:scale-95 transition-all flex items-center gap-2 shadow-[0_0_20px_rgba(57,255,20,0.3)]"
            >
              <span>⬡</span> START SCANNING
            </Link>
            <Link
              href="/dashboard"
              className="border border-secondary-container text-secondary-container px-8 py-3 rounded uppercase tracking-widest text-sm hover:bg-secondary-container/10 active:scale-95 transition-all"
            >
              VIEW DASHBOARD
            </Link>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-16 max-w-3xl mx-auto lg:mx-0">
            {[
              { value: "99.8%", label: "ACCURACY_RATE" },
              { value: "12ms", label: "SCAN_LATENCY" },
              { value: "50K+", label: "NOTES_SCANNED" },
              { value: "24/7", label: "UPTIME" },
            ].map((stat) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="glass-panel p-4 text-center rounded"
              >
                <p className="font-display text-headline-lg text-primary-container">{stat.value}</p>
                <p className="font-mono text-[10px] text-on-surface-variant tracking-widest">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>

      <div className="absolute bottom-8 left-0 right-0 flex justify-center">
        <div className="w-px h-16 bg-gradient-to-b from-primary-container to-transparent"></div>
      </div>
    </section>
  )
}
