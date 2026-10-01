/**
 * Feedback inbox.
 *
 * Lists the ratings and messages users have left, from the existing admin-guarded
 * `GET /feedback` endpoint.
 */

import { useCallback, useEffect, useState } from 'react'
import { MessageSquare, Star, AlertCircle } from 'lucide-react'
import { adminApi } from '../../api/auth.js'

function formatDate(value) {
  if (!value) return '—'
  try {
    return new Date(value).toLocaleString(undefined, {
      day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit',
    })
  } catch {
    return '—'
  }
}

function Stars({ value }) {
  return (
    <span className="stars" aria-label={`${value} out of 5`}>
      {[1, 2, 3, 4, 5].map((n) => (
        <Star
          key={n}
          size={14}
          className={n <= value ? 'stars__on' : 'stars__off'}
          aria-hidden="true"
          fill={n <= value ? 'currentColor' : 'none'}
        />
      ))}
    </span>
  )
}

export default function AdminFeedback() {
  const [rows, setRows] = useState([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const res = await adminApi.feedback()
      setRows(res.items || [])
      setTotal(res.total || 0)
    } catch (err) {
      setError(err.message || 'Could not load feedback.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  return (
    <div className="admin__page">
      <header className="admin__page-head">
        <h1><MessageSquare size={24} /> Feedback</h1>
        <p>{total} rating{total === 1 ? '' : 's'} submitted by users.</p>
      </header>

      {error && (
        <div className="auth__alert auth__alert--error" role="alert">
          <AlertCircle size={18} /><span>{error}</span>
        </div>
      )}

      <div className="panel admin__table-wrap">
        {loading ? (
          <div className="admin__loading" role="status" aria-live="polite">
            <span className="spinner spinner--lg" aria-hidden="true" />
            <p className="muted">Loading feedback…</p>
          </div>
        ) : rows.length === 0 ? (
          <p className="muted admin__empty">No feedback has been submitted yet.</p>
        ) : (
          <ul className="admin__feedback">
            {rows.map((row) => (
              <li key={row.id}>
                <Stars value={row.rating} />
                {row.message ? <p>{row.message}</p> : <p className="muted">No message left.</p>}
                <time className="muted">{formatDate(row.submitted_at)}</time>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
