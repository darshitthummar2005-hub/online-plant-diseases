/**
 * Detection records.
 *
 * Read-only history of every diagnosis run on the portal, from the admin-guarded
 * `GET /admin/detections`. Read-only by design: a detection is a medical-style
 * audit record, so there is no delete action here.
 */

import { useCallback, useEffect, useState } from 'react'
import { Stethoscope, Search, AlertCircle, Activity } from 'lucide-react'
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

function confidenceTone(value) {
  if (value >= 75) return 'ok'
  if (value >= 45) return 'mid'
  return 'low'
}

export default function AdminDetections() {
  const [rows, setRows] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [q, setQ] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const res = await adminApi.detections({ page, page_size: 20, q: q || undefined })
      setRows(res.items || [])
      setTotal(res.total || 0)
    } catch (err) {
      setError(err.message || 'Could not load detection records.')
    } finally {
      setLoading(false)
    }
  }, [page, q])

  useEffect(() => {
    const t = setTimeout(load, q ? 300 : 0)
    return () => clearTimeout(t)
  }, [load, q])

  const pages = Math.max(1, Math.ceil(total / 20))

  return (
    <div className="admin__page">
      <header className="admin__page-head">
        <h1><Stethoscope size={24} /> Detection records</h1>
        <p>Every AI Plant Doctor run on the portal — {total} in total.</p>
      </header>

      {error && (
        <div className="auth__alert auth__alert--error" role="alert">
          <AlertCircle size={18} /><span>{error}</span>
        </div>
      )}

      <div className="admin__toolbar panel">
        <div className="admin__search">
          <Search size={17} aria-hidden="true" />
          <input
            className="input" type="search" value={q} aria-label="Search detections"
            onChange={(e) => { setQ(e.target.value); setPage(1) }}
            placeholder="Search disease name…"
          />
        </div>
      </div>

      <div className="panel admin__table-wrap">
        {loading ? (
          <div className="admin__loading" role="status" aria-live="polite">
            <span className="spinner spinner--lg" aria-hidden="true" />
            <p className="muted">Loading records…</p>
          </div>
        ) : rows.length === 0 ? (
          <p className="muted admin__empty">
            <Activity size={18} /> No detection records yet.
          </p>
        ) : (
          <div className="admin__table-scroll">
            <table className="admin__table">
              <thead>
                <tr>
                  <th scope="col">Diagnosis</th>
                  <th scope="col">User</th>
                  <th scope="col">Confidence</th>
                  <th scope="col">Severity</th>
                  <th scope="col">When</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.id}>
                    <td>
                      <strong>{row.disease_name}</strong>
                      {row.plant && <span className="muted"> · {row.plant}</span>}
                      {row.symptoms?.length > 0 && (
                        <span className="muted admin__symptoms">
                          {row.symptoms.slice(0, 3).join(' · ')}
                        </span>
                      )}
                    </td>
                    <td className="muted">{row.username || 'Guest'}</td>
                    <td>
                      <span className={`conf conf--${confidenceTone(row.confidence)}`}>
                        {row.confidence}%
                      </span>
                    </td>
                    <td>
                      {row.severity ? <span className="chip">{row.severity}</span> : <span className="muted">—</span>}
                    </td>
                    <td className="muted">{formatDate(row.predicted_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {pages > 1 && (
          <div className="admin__pager">
            <button className="btn btn-ghost btn-sm" type="button" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
              Previous
            </button>
            <span className="muted">Page {page} of {pages}</span>
            <button className="btn btn-ghost btn-sm" type="button" disabled={page >= pages} onClick={() => setPage((p) => p + 1)}>
              Next
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
