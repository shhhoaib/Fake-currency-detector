"use client"

import { Toaster } from "react-hot-toast"
import "./globals.css"

export default function RootLayout({ children }: { children: React.ReactNode }) {

  return (
    <html lang="en" className="dark">
      <head>
        <title>PakShield AI | Pakistani Currency Detector</title>
        <meta name="description" content="AI-powered Pakistani currency authenticity detection system" />
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🛡️</text></svg>" />
      </head>
      <body className="font-mono text-on-background">
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: "#1c1b1b",
              color: "#e5e2e1",
              border: "1px solid rgba(42, 229, 0, 0.3)",
              fontFamily: "JetBrains Mono, monospace",
              fontSize: "12px",
            },
          }}
        />
        {children}
      </body>
    </html>
  )
}
