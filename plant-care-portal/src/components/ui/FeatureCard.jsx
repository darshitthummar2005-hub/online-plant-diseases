import { Link } from 'react-router-dom'
import TiltCard from './TiltCard.jsx'
import { haptic } from '../../utils/haptics.js'

export default function FeatureCard({ to, emoji, title, desc, color }) {
  return (
    <TiltCard as={Link} to={to} className="panel" maxTilt={14}>
      <div className="tilt-inner" style={{ padding: '26px 22px', height: '100%', display: 'block' }}>
        <div
          className="tilt-pop"
          style={{
            fontSize: '2.6rem',
            width: 64,
            height: 64,
            borderRadius: 18,
            display: 'grid',
            placeItems: 'center',
            background: color ?? 'var(--green-100)',
            marginBottom: 16,
            boxShadow: '0 8px 18px rgba(20,48,28,0.15)',
          }}
        >
          {emoji}
        </div>
        <h3 className="tilt-pop" style={{ marginBottom: 8, fontSize: '1.15rem' }}>
          {title}
        </h3>
        <p className="muted tilt-pop">{desc}</p>
      </div>
    </TiltCard>
  )
}
