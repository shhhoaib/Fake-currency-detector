import type { Metadata } from "next"
import "./globals.css"
import ToasterProvider from "./ToasterProvider"

export const metadata: Metadata = {
  title: "PakShield AI | Pakistani Currency Detector",
  description: "AI-powered Pakistani currency authenticity detection system",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="font-mono text-on-background">
        <ToasterProvider />
        {children}
      </body>
    </html>
  )
}
