"use client"

import { Toaster } from "react-hot-toast"

export default function ToasterProvider() {
  return (
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
  )
}
