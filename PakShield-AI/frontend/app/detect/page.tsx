"use client"

import Navbar from "@/components/Navbar"
import Ticker from "@/components/Ticker"
import AIScanner from "@/components/AIScanner"
import Comparison from "@/components/Comparison"
import SecurityFeatures from "@/components/SecurityFeatures"
import Chatbot from "@/components/Chatbot"
import Footer from "@/components/Footer"

export default function DetectPage() {
  return (
    <>
      <Navbar />
      <main className="pt-20 pb-20 px-hud-margin min-h-screen max-w-7xl mx-auto">
        <div className="mb-8 pt-8">
          <h1 className="font-display text-display-lg text-primary uppercase tracking-tighter">
            SCANNER<span className="text-primary-container">_CORE</span>
          </h1>
          <p className="font-mono text-body-md text-on-surface-variant mt-2">
            Upload a Pakistani currency note image for AI-powered authenticity analysis
          </p>
        </div>
        <Ticker />
        <AIScanner />
        <Comparison />
        <SecurityFeatures />
      </main>
      <Footer />
      <Chatbot />
    </>
  )
}
