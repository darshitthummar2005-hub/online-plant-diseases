/**
 * Admin overview.
 *
 * Greeting for the signed-in admin plus the platform counters, a disease-category
 * breakdown and a recent-activity feed — everything from one `GET /admin/overview`
 * round trip so the page paints in a single request.
 */

import { useEffect, useState } from 'react'
import {
  Users, UserPlus, Stethoscope, Leaf, Star, ShieldCheck, TrendingUp,
  AlertCircle, Activity, Sprout,
} from 'lucide-react'
import { adminApi } from '../../api/auth.js'
import { useAuth } from '../../context/AuthContext.jsx'

const CARDS = [
  { key: 'total_users', icon: Users, label: 'Total users', tone: 'green' },
  { key: 'new_users_7d', icon: UserPlus, label: 'New this week', tone: 'mint' },
  { key: 'total_admins', icon: ShieldCheck, label: 'Administrators', tone: 'amber' },
  { key: 'total_predictions', icon: Stethoscope, label: 'Detections run', tone: 'blue' },
  { key: 'total_diseases', icon: Leaf, label: 'Diseases on record', tone: 'green' },
  { key: 'average_rating', icon: Star, label: 'Average rating', tone: 'amber', suffix: '/5' },
]

function timeAgo(value) {
  if (!value) return ''
  const diff = Date.now() - new Date(value).getTime()
  const mins = Math.round(diff / 60000)
  if (mins < 1) return 'just now'
  if (mins < 60) return `${mins}m ago`
  const hours = Math.round(mins / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.round(hours / 24)
  return days < 30 ? `${days}d ago` : new Date(value).toLocaleDateString()
}

export default function AdminOverview() {
  const { user } = useAuth()
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    adminApi
      .overview()
      .then((res) => { if (!cancelled) setData(res) })
      .catch((err) => { if (!cancelled) setError(err.message || 'Could not load the dashboard.') })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [])

  if (loading) {
    return (
      <div className="admin__loading" role="status" aria-live="polite">
        <span className="spinner spinner--lg" aria-hidden="true" />
        <p className="muted">Loading dashboard…</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="auth__alert auth__alert--error" role="alert">
        <AlertCircle size={18} /><span>{error}</span>
      </div>
    )
  }

  const { stats, disease_categories: categories = [], recent_activity: activity = [] } = data || {}
  const maxCategory = Math.max(1, ...categories.map((c) => c.count))

  return (
    <div className="admin__page">
      <header className="admin__page-head">
        <h1>Welcome, {user?.full_name || user?.username}</h1>
        <p>Here is what is happening across ONLINE PLANT DISEASES right now.</p>
      </header>

      {/* ---------- Stat cards ---------- */}
      <div className="admin__cards">
        {CARDS.map(({ key, icon: Icon, label, tone, suffix }) => {
          const raw = stats?.[key] ?? 0
          const value = key === 'average_rating' ? Number(raw).toFixed(1) : Number(raw).toLocaleString()
          return (
            <div className={`admin__card admin__card--${tone}`} key={key}>
              <span className="admin__card-icon"><Icon size={19} /></span>
              <div>
                <strong>{value}{suffix || ''}</strong>
                <span className="muted">{label}</span>
              </div>
            </div>
          )
        })}
      </div>

      <div className="admin__split">
        {/* ---------- Category breakdown ---------- */}
        <section className="panel admin__panel">
          <h2><Sprout size={18} /> Disease library breakdown</h2>
          {categories.length === 0 ? (
            <p className="muted">No disease records found.</p>
          ) : (
            <ul className="admin__bars">
              {categories.map((c) => (
                <li key={c.label}>
                  <div className="admin__bar-head">
                    <span>{c.label}</span>
                    <strong>{c.count}</strong>
                  </div>
                  <div className="admin__bar-track">
                    <div
                      className="admin__bar-fill"
                      style={{ width: `${Math.max(4, (c.count / maxCategory) * 100)}%` }}
                    />
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>

        {/* ---------- Activity feed ---------- */}
        <section className="panel admin__panel">
          <h2><Activity size={18} /> Recent activity</h2>
          {activity.length === 0 ? (
            <p className="muted">Nothing has happened yet.</p>
          ) : (
            <ul className="admin__feed">
              {activity.map((item, i) => (
                <li key={`${item.at}-${i}`}>
                  <span className={`admin__feed-dot admin__feed-dot--${item.kind}`} aria-hidden="true" />
                  <div>
                    <strong>{item.title}</strong>
                    {item.detail && <p className="muted">{item.detail}</p>}
                  </div>
                  <time className="muted">{timeAgo(item.at)}</time>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>

      <p className="admin__note">
        <TrendingUp size={15} />
        Detections in the last 7 days: <strong>{stats?.detections_7d ?? 0}</strong> · Feedback
        entries: <strong>{stats?.total_feedback ?? 0}</strong>
      </p>
    </div>
  )
}
