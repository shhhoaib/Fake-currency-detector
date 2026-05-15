export default function Footer() {
  return (
    <footer className="border-t border-outline-variant/30 py-8 px-hud-margin">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-primary-container">🛡️</span>
            <span className="font-display text-headline-md text-primary tracking-tighter uppercase">
              PakShield<span className="text-primary-container">_AI</span>
            </span>
          </div>
          <div className="font-mono text-[10px] text-on-surface-variant text-center">
            <p>PAKISTAN_MONETARY_VIGILANCE_SYSTEM</p>
            <p className="mt-1">© {new Date().getFullYear()} PakShield AI — All rights reserved</p>
          </div>
          <div className="flex gap-4 font-mono text-[10px] text-on-surface-variant">
            <span className="hover:text-primary transition-colors cursor-pointer uppercase">SECURITY</span>
            <span className="hover:text-primary transition-colors cursor-pointer uppercase">PRIVACY</span>
            <span className="hover:text-primary transition-colors cursor-pointer uppercase">SBP_LINKS</span>
          </div>
        </div>
        <div className="mt-6 pt-4 border-t border-outline-variant/20 text-center">
          <p className="font-mono text-[8px] text-outline uppercase tracking-[0.3em]">
            DISCLAIMER: This AI system is for educational and verification assistance purposes. Always consult State Bank of Pakistan for official currency validation.
          </p>
        </div>
      </div>
    </footer>
  )
}
