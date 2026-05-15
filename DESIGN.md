---
name: Cyber-Security Currency Interface
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#3a3939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#baccb0'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#85967c'
  outline-variant: '#3c4b35'
  surface-tint: '#2ae500'
  primary: '#efffe3'
  on-primary: '#053900'
  primary-container: '#39ff14'
  on-primary-container: '#107100'
  inverse-primary: '#106e00'
  secondary: '#dcfdff'
  on-secondary: '#00373a'
  secondary-container: '#00f1fd'
  on-secondary-container: '#006a6f'
  tertiary: '#fff8f7'
  on-tertiary: '#690006'
  tertiary-container: '#ffd3ce'
  on-tertiary-container: '#c50015'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#79ff5b'
  primary-fixed-dim: '#2ae500'
  on-primary-fixed: '#022100'
  on-primary-fixed-variant: '#095300'
  secondary-fixed: '#6ff6ff'
  secondary-fixed-dim: '#00dce6'
  on-secondary-fixed: '#002022'
  on-secondary-fixed-variant: '#004f53'
  tertiary-fixed: '#ffdad6'
  tertiary-fixed-dim: '#ffb4ab'
  on-tertiary-fixed: '#410002'
  on-tertiary-fixed-variant: '#93000c'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-lg:
    fontFamily: Space Grotesk
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-md:
    fontFamily: JetBrains Mono
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.1em
  terminal-code:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  container-padding: 24px
  gutter: 16px
  hud-margin: 32px
---

## Brand & Style

The design system is engineered for a high-stakes, high-tech environment focused on financial integrity and digital vigilance. It targets a tech-savvy user base operating in "street-level" or high-security contexts, evoking a sense of urgency, precision, and futuristic authority.

The aesthetic blends **Cyberpunk** grit with **Modern Fintech** clarity. It utilizes **Glassmorphism** for data overlays, creating a sense of multi-layered depth common in Head-Up Displays (HUDs). To ground the futuristic elements, it incorporates **Brutalist** structural cues—heavy borders, monospaced data readouts, and a rigid digital grid—ensuring the interface feels like a specialized security tool rather than a generic consumer app.

Visual hallmarks include:
- **Digital Grid Underlays:** A persistent 24px background grid to reinforce the "scanning" metaphor.
- **Scanline Overlays:** Subtle horizontal patterns to mimic cathode-ray or holographic projection.
- **Chromatic Aberration:** Minimal fringe effects on high-priority alerts to simulate "glitch" aesthetics in a controlled, professional manner.

## Colors

This design system is strictly dark-mode, utilizing a "Total Black" (#050505) canvas to maximize the luminance of neon accents. 

- **Primary (Neon Green):** Reserved for "Authentic" status, successful scans, and primary action buttons. It represents safety and verification.
- **Secondary (Cyan Blue):** Used for data visualization, technical metadata, and "In-Progress" states. It provides a cool, analytical contrast to the primary green.
- **Tertiary (Neon Red):** Exclusively for "Counterfeit" alerts, errors, and critical system warnings.
- **Neutral/Background:** Deep blacks and dark slate are used to create the glassmorphic background layers, ensuring high legibility for neon text.

## Typography

The typography strategy leverages two distinct voices. **Space Grotesk** provides a geometric, futuristic feel for high-level status readouts and branding. **JetBrains Mono** is used for all functional data, terminal readouts, and currency serial numbers to emphasize the "machine-processed" nature of the application.

All labels should be uppercase with increased letter spacing to mimic technical blueprints. Critical alerts (Counterfeit/Authentic) should use the `display-lg` tier for immediate impact.

## Layout & Spacing

The layout follows a **Fixed HUD Grid**. Content is contained within a "viewfinder" frame, with persistent 32px outer margins that act as the device bezel.

- **Desktop:** 12-column grid with wide 32px gutters to allow the glassmorphic backgrounds to breathe.
- **Mobile:** 4-column grid with 16px gutters. The interface should feel cramped and data-dense, mimicking a handheld industrial scanner.
- **Spacing Rhythm:** All spacing must be multiples of 8px. Use generous padding inside containers (24px+) to prevent the high-contrast neon borders from crowding the content.

## Elevation & Depth

This design system eschews traditional soft shadows in favor of **Luminous Depth**:

1.  **Level 0 (Base):** Deep black (#050505) with a subtle digital grid pattern.
2.  **Level 1 (Panels):** Translucent dark slate (#1E293B) with a 12px backdrop blur (Glassmorphism). Borders are 1px solid slate.
3.  **Level 2 (Active States):** The same translucent panels but with a 1px Neon Green or Cyan border and a 5px outer glow (`box-shadow: 0 0 10px rgba(var(--primary), 0.5)`).
4.  **Level 3 (Modals/Overlays):** High-intensity blur (20px+) with vibrant glow-borders and scanline textures to pull the element forward.

## Shapes

The shape language is **Industrial-Soft**. While the base roundedness is 0.25rem (4px) to provide a modern fintech touch, the visual interest is created through "clipped corners" (chamfers) on buttons and containers.

- **Containers:** 4px border radius with "corner brackets" (L-shaped accents) on the exterior corners.
- **Buttons:** Sharp 2px radius or 45-degree chamfered corners to emphasize a tactical, hardware-like feel.
- **Icons:** Thin-stroke, geometric icons with open paths.

## Components

### Buttons
- **Holographic Primary:** Solid Neon Green background with black text. On hover, apply a rapid "flicker" animation (opacity 0.8 to 1).
- **Ghost Action:** Transparent background with 1px Cyan border. On hover, the background fills with a 10% Cyan tint.

### Terminal Containers
- Used for serial number logs and metadata. These should have a "Header Bar" featuring a small blinking cursor icon and "SYS_LOG" breadcrumbs.

### The Scanner Line
- A horizontal Cyan Blue line that constantly oscillates vertically over the "Currency Preview" area. It should have a 20px feathered glow.

### HUD Chips
- Small, rectangular badges with monospaced text. For example, a "VERIFIED" chip would have a Primary Green border and a small checkmark icon.

### Input Fields
- Terminal-style prompts. Use a `>` prefix instead of standard labels. The bottom border is a thick 2px Cyan line, while the other three sides remain 1px Slate.

### Animated Graphs
- Real-time line charts showing "Authenticity Probability." Lines should be Neon Green with a semi-transparent gradient fill below the stroke.