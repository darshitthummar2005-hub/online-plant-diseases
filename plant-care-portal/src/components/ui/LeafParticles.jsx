import { useMemo } from 'react'
import { Leaf } from 'lucide-react'

const LEAF_COLORS = [
  'rgba(74, 124, 89, 0.22)',
  'rgba(104, 166, 120, 0.28)',
  'rgba(38, 82, 58, 0.18)',
  'rgba(143, 192, 169, 0.32)',
  'rgba(74, 124, 89, 0.16)',
]

export default function LeafParticles({ count = 10 }) {
  const leaves = useMemo(
    () =>
      Array.from({ length: count }, (_, i) => ({
        id: i,
        left: `${(i * 97) % 100}%`,
        size: 18 + ((i * 13) % 30),
        duration: 14 + ((i * 7) % 16),
        delay: -((i * 3) % 22),
        color: LEAF_COLORS[i % LEAF_COLORS.length],
        opacity: 0.5 + ((i * 17) % 50) / 100,
      })),
    [count]
  )

  return (
    <div className="leaf-scene" aria-hidden="true">
      {leaves.map((l) => (
        <span
          key={l.id}
          className="leaf-3d"
          style={{
            left: l.left,
            fontSize: l.size,
            animationDuration: `${l.duration}s`,
            animationDelay: `${l.delay}s`,
            color: l.color,
            opacity: l.opacity,
          }}
        >
          <Leaf />
        </span>
      ))}
    </div>
  )
}
