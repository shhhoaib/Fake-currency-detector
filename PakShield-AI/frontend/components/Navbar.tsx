"use client"

import { useState } from "react"
import Link from "next/link"
import { motion, AnimatePresence } from "framer-motion"

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <>
      <header className="fixed top-0 w-full z-50 bg-surface/80 backdrop-blur-xl border-b border-outline-variant shadow-[0_0_15px_rgba(42,229,0,0.3)]">
        <div className="flex justify-between items-center px-hud-margin py-3">
          <div className="flex items-center gap-4">
            <Link href="/" className="flex items-center gap-2">
              <span className="text-primary-container text-xl">🛡️</span>
              <span className="font-display text-headline-md text-primary tracking-tighter uppercase">
                PakShield<span className="text-primary-container">Ai.</span>
              </span>
            </Link>
            <nav className="hidden md:flex gap-6 ml-8">
              <Link href="/" className="text-primary font-bold border-b-2 border-primary font-mono text-terminal-code">
                HOME
              </Link>
              <Link href="/detect" className="text-on-surface-variant font-medium font-mono text-terminal-code hover:text-secondary-fixed transition-colors">
                SCANNER
              </Link>
              <Link href="/dashboard" className="text-on-surface-variant font-medium font-mono text-terminal-code hover:text-secondary-fixed transition-colors">
                DASHBOARD
              </Link>
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-2 glass-panel px-3 py-1.5 rounded">
              <span className="w-2 h-2 rounded-full bg-primary-container animate-pulse"></span>
              <span className="font-mono text-[10px] text-primary">PUBLIC_ACCESS</span>
            </div>
            <button className="md:hidden text-primary text-xl" onClick={() => setMobileOpen(!mobileOpen)}>
              {mobileOpen ? "✕" : "☰"}
            </button>
          </div>
        </div>
      </header>

      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="fixed top-16 left-0 right-0 z-40 bg-surface-container-high/95 backdrop-blur-xl border-b border-outline-variant p-6 md:hidden"
          >
            <nav className="flex flex-col gap-4">
              <Link href="/" className="font-mono text-primary" onClick={() => setMobileOpen(false)}>HOME</Link>
              <Link href="/detect" className="font-mono text-on-surface-variant" onClick={() => setMobileOpen(false)}>SCANNER</Link>
              <Link href="/dashboard" className="font-mono text-on-surface-variant" onClick={() => setMobileOpen(false)}>DASHBOARD</Link>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
