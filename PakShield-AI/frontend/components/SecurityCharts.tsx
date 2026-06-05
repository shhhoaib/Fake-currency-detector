"use client"

import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Cell,
  Tooltip,
} from "recharts"

interface SecurityChartsProps {
  featureScores: Record<string, number>
  securityAnalysis: Record<string, any>
  result: string
}

const FEATURE_LABELS: Record<string, string> = {
  print_quality: "Print Quality",
  color_accuracy: "Color Accuracy",
  watermark_integrity: "Watermark",
  security_thread: "Security Thread",
  texture_authenticity: "Texture",
  pattern_symmetry: "Pattern Symmetry",
  microtext_clarity: "Microtext",
  serial_presence: "Text Detection",
}

const RADAR_ORDER = [
  "print_quality",
  "color_accuracy",
  "watermark_integrity",
  "security_thread",
  "texture_authenticity",
  "pattern_symmetry",
  "microtext_clarity",
  "serial_presence",
]

export default function SecurityCharts({ featureScores, securityAnalysis, result }: SecurityChartsProps) {
  const radarData = RADAR_ORDER
    .filter((k) => k in featureScores)
    .map((k) => ({
      feature: FEATURE_LABELS[k] || k,
      score: Math.round(featureScores[k] || 0),
      fullMark: 100,
    }))

  const barData = RADAR_ORDER
    .filter((k) => k in featureScores)
    .map((k) => ({
      name: FEATURE_LABELS[k] || k,
      score: Math.round(featureScores[k] || 0),
    }))

  const scoreColor = (score: number) => {
    if (score >= 70) return "#4ade80"
    if (score >= 45) return "#facc15"
    return "#f87171"
  }

  return (
    <div className="mt-4 pt-4 border-t border-primary/20 space-y-4">
      <p className="font-mono text-[10px] text-on-surface-variant uppercase tracking-widest">
        SECURITY_FEATURE_ANALYSIS
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-black/40 rounded p-3">
          <p className="font-mono text-[9px] text-primary uppercase mb-2 text-center">
            Feature Score Radar
          </p>
          <ResponsiveContainer width="100%" height={220}>
            <RadarChart data={radarData} cx="50%" cy="50%" outerRadius="70%">
              <PolarGrid stroke="rgba(0, 255, 255, 0.2)" />
              <PolarAngleAxis
                dataKey="feature"
                tick={{ fill: "#8892b0", fontSize: 8 }}
                axisLine={{ stroke: "rgba(0, 255, 255, 0.1)" }}
              />
              <PolarRadiusAxis
                angle={30}
                domain={[0, 100]}
                tick={{ fill: "#8892b0", fontSize: 8 }}
                axisLine={{ stroke: "rgba(0, 255, 255, 0.1)" }}
              />
              <Radar
                name="Score"
                dataKey="score"
                stroke={result === "REAL" ? "#4ade80" : "#f87171"}
                fill={result === "REAL" ? "#4ade80" : "#f87171"}
                fillOpacity={0.2}
                strokeWidth={1.5}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-black/40 rounded p-3">
          <p className="font-mono text-[9px] text-primary uppercase mb-2 text-center">
            Feature Score Breakdown
          </p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={barData} layout="vertical" margin={{ top: 0, right: 20, left: 60, bottom: 0 }}>
              <XAxis type="number" domain={[0, 100]} hide />
              <YAxis
                type="category"
                dataKey="name"
                tick={{ fill: "#8892b0", fontSize: 8 }}
                width={60}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                contentStyle={{
                  background: "#0a0a1a",
                  border: "1px solid rgba(0, 255, 255, 0.3)",
                  borderRadius: "4px",
                  fontSize: "10px",
                }}
                labelStyle={{ color: "#ccd6f6" }}
                formatter={(value: number) => [`${value}/100`, "Score"]}
              />
              <Bar dataKey="score" radius={[0, 3, 3, 0]} barSize={14}>
                {barData.map((entry, index) => (
                  <Cell key={index} fill={scoreColor(entry.score)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {Object.entries(securityAnalysis).map(([key, info]: [string, any]) => {
        const label = FEATURE_LABELS[key] || key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
        const score = info?.score ?? 0
        return (
          <div
            key={key}
            className="bg-black/40 rounded p-3 border-l-2"
            style={{
              borderLeftColor: score >= 70 ? "#4ade80" : score >= 45 ? "#facc15" : "#f87171",
            }}
          >
            <div className="flex items-center justify-between mb-1">
              <p className="font-mono text-[10px] text-primary uppercase tracking-wider">
                {label}
              </p>
              <div className="flex items-center gap-2">
                <div
                  className="h-1.5 w-20 rounded-full bg-black/60 overflow-hidden"
                >
                  <div
                    className="h-full rounded-full transition-all"
                    style={{
                      width: `${score}%`,
                      backgroundColor: score >= 70 ? "#4ade80" : score >= 45 ? "#facc15" : "#f87171",
                    }}
                  />
                </div>
                <span
                  className="font-mono text-[10px]"
                  style={{
                    color: score >= 70 ? "#4ade80" : score >= 45 ? "#facc15" : "#f87171",
                  }}
                >
                  {score}/100
                </span>
              </div>
            </div>
            {info?.details && (
              <p className="font-mono text-[9px] text-on-surface-variant leading-relaxed">
                {info.details}
              </p>
            )}
          </div>
        )
      })}
    </div>
  )
}
