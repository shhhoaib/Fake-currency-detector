"use client"

import { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { chatAPI } from "@/lib/api"

interface Message {
  role: "user" | "assistant"
  content: string
}

export default function Chatbot() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Assalam-o-Alaikum! I am PakShield AI. Ask me anything about Pakistani currency detection.",
    },
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || loading) return

    const userMsg = input.trim()
    setInput("")
    setMessages((prev) => [...prev, { role: "user", content: userMsg }])
    setLoading(true)

    try {
      const res = await chatAPI.send(userMsg)
      setMessages((prev) => [...prev, { role: "assistant", content: res.data.reply }])
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Error: Unable to get response." }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            className="fixed bottom-24 right-6 z-50 w-[360px] max-w-[calc(100vw-48px)] glass-panel-strong rounded overflow-hidden shadow-[0_0_30px_rgba(0,241,253,0.2)]"
          >
            <div className="bg-primary-container/20 px-4 py-3 border-b border-outline-variant flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-secondary-container">🤖</span>
                <span className="font-mono text-label-sm text-primary">PAKSHIELD_AI</span>
              </div>
              <button onClick={() => setOpen(false)} className="text-on-surface-variant hover:text-primary transition-colors">
                ✕
              </button>
            </div>

            <div className="h-[300px] overflow-y-auto p-4 space-y-3">
              {messages.map((msg, i) => (
                <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[80%] p-3 rounded font-mono text-[11px] leading-relaxed ${
                      msg.role === "user"
                        ? "bg-primary-container/20 border border-primary-container/30 text-primary"
                        : "bg-black/40 border border-outline-variant/30 text-on-surface-variant"
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-black/40 border border-outline-variant/30 p-3 rounded font-mono text-[11px] text-on-surface-variant">
                    <span className="animate-pulse">Thinking</span>
                    <span className="animate-pulse ml-1">...</span>
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>

            <div className="border-t border-outline-variant p-3 flex gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                placeholder="> Ask about currency..."
                className="flex-1 bg-black/60 border border-outline-variant rounded px-3 py-2 font-mono text-[11px] text-primary placeholder:text-outline focus:border-primary-container focus:outline-none"
              />
              <button
                onClick={handleSend}
                disabled={loading || !input.trim()}
                className="bg-primary-container text-on-primary px-3 py-2 rounded font-mono text-[10px] uppercase hover:opacity-90 disabled:opacity-50 transition-all"
              >
                ➤
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <button
        onClick={() => setOpen(!open)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-secondary-container shadow-[0_0_20px_#00f1fd] flex items-center justify-center group hover:scale-105 active:scale-95 transition-all"
      >
        <div className="absolute inset-0 bg-[radial-gradient(circle,rgba(255,255,255,0.4)_0%,transparent_70%)] animate-pulse rounded-full"></div>
        <span className="text-on-secondary-container text-2xl relative z-10">{open ? "✕" : "🤖"}</span>
      </button>
    </>
  )
}
