"use client"

import Navbar from "@/components/Navbar"
import Hero from "@/components/Hero"
import Ticker from "@/components/Ticker"
import AIScanner from "@/components/AIScanner"
import Comparison from "@/components/Comparison"
import SecurityFeatures from "@/components/SecurityFeatures"
import Currency3D from "@/components/Currency3D"
import Timeline from "@/components/Timeline"
import Chatbot from "@/components/Chatbot"
import Footer from "@/components/Footer"

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main className="pt-20 pb-20 px-hud-margin min-h-screen max-w-7xl mx-auto">
        <Hero />
        <Ticker />
        <AIScanner />
        <Comparison />
        <SecurityFeatures />
        <Currency3D />
        <Timeline />
      </main>
      <Footer />
      <Chatbot />

      <nav className="md:hidden fixed bottom-0 w-full z-50 rounded-t-xl bg-surface-container-high/95 backdrop-blur-lg border-t border-primary/30 shadow-[0_-4px_20px_rgba(0,241,253,0.2)] flex justify-around items-center p-2">
        {[
          { href: "/", icon: "⌂", label: "Home" },
          { href: "/detect", icon: "◻", label: "Scan" },
          { href: "/dashboard", icon: "⬡", label: "Data" },
        ].map((item) => (
          <a
            key={item.href}
            href={item.href}
            className="flex flex-col items-center justify-center text-on-surface-variant px-4 py-1 hover:text-primary transition-colors"
          >
            <span className="text-lg">{item.icon}</span>
            <span className="font-mono text-[8px] uppercase tracking-widest">{item.label}</span>
          </a>
        ))}
      </nav>
    </>
  )
}
