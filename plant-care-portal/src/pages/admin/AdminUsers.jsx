/**
 * User management.
 *
 * Lists every account with search and a role filter, and lets an admin rename,
 * enable/disable, promote/demote or delete an account. The backend enforces the
 * real rules (no self-demotion, no removing the last active admin) and this UI
 * simply hides the controls that would fail.
 */

import { useCallback, useEffect, useState } from 'react'
import {
  Users, Search, ShieldCheck, UserX, UserCheck, Trash2, AlertCircle,
  RotateCcw, Check, X as XIcon,
} from 'lucide-react'
import { adminApi } from '../../api/auth.js'
import { useAuth } from '../../context/AuthContext.jsx'
import { useApp } from '../../context/AppContext.jsx'

const ROLES = [
  { value: '', label: 'All roles' },
  { value: 'user', label: 'Users' },
  { value: 'admin', label: 'Admins' },
]

function formatDate(value) {
  if (!value) return '—'
  try {
    return new Date(value).toLocaleDateString(undefined, { day: '2-digit', month: 'short', year: 'numeric' })
  } catch {
    return '—'
  }
}

export default function AdminUsers() {
  const { user: me } = useAuth()
  const { notify } = useApp()

  const [rows, setRows] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pageSize] = useState(15)
  const [q, setQ] = useState('')
  const [role, setRole] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [busyId, setBusyId] = useState(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const res = await adminApi.users({ page, page_size: pageSize, q: q || undefined, role: role || undefined })
      setRows(res.items || [])
      setTotal(res.total || 0)
    } catch (err) {
      setError(err.message || 'Could not load users.')
    } finally {
      setLoading(false)
    }
  }, [page, pageSize, q, role])

  useEffect(() => {
    // Debounce so typing in the search box does not fire a request per keystroke.
    const t = setTimeout(load, q ? 300 : 0)
    return () => clearTimeout(t)
  }, [load, q])

  async function act(id, payload, successMsg) {
    setBusyId(id)
    setError('')
    try {
      await adminApi.updateUser(id, payload)
      notify(successMsg)
      await load()
    } catch (err) {
      setError(err.message || 'That change could not be applied.')
    } finally {
      setBusyId(null)
    }
  }

  async function remove(row) {
    const name = row.full_name || row.username
    if (!window.confirm(`Delete ${name} (${row.username})? This cannot be undone.`)) return
    setBusyId(row.id)
    setError('')
    try {
      await adminApi.deleteUser(row.id)
      notify(`Deleted ${row.username}`)
      if (rows.length === 1 && page > 1) setPage((p) => p - 1)
      else await load()
    } catch (err) {
      setError(err.message || 'That account could not be deleted.')
    } finally {
      setBusyId(null)
    }
  }

  const pages = Math.max(1, Math.ceil(total / pageSize))

  return (
    <div className="admin__page">
      <header className="admin__page-head">
        <h1><Users size={24} /> User management</h1>
        <p>{total} registered {total === 1 ? 'account' : 'accounts'}. Search, filter and manage access.</p>
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
            className="input"
            type="search"
            value={q}
            onChange={(e) => { setQ(e.target.value); setPage(1) }}
            placeholder="Search name, username or email…"
            aria-label="Search users"
          />
        </div>
        <div className="admin__filters" role="group" aria-label="Filter by role">
          {ROLES.map((r) => (
            <button
              key={r.value}
              type="button"
              className={`chip ${role === r.value ? 'chip--on' : ''}`}
              onClick={() => { setRole(r.value); setPage(1) }}
              aria-pressed={role === r.value}
            >
              {r.value === '' && <Check size={13} />}
              {r.label}
            </button>
          ))}
        </div>
      </div>

      <div className="panel admin__table-wrap">
        {loading ? (
          <div className="admin__loading" role="status" aria-live="polite">
            <span className="spinner spinner--lg" aria-hidden="true" />
            <p className="muted">Loading users…</p>
          </div>
        ) : rows.length === 0 ? (
          <p className="muted admin__empty">No accounts match your search.</p>
        ) : (
          <div className="admin__table-scroll">
            <table className="admin__table">
              <thead>
                <tr>
                  <th scope="col">User</th>
                  <th scope="col">Role</th>
                  <th scope="col">Status</th>
                  <th scope="col">Joined</th>
                  <th scope="col" className="right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => {
                  const isSelf = row.id === me?.id
                  const busy = busyId === row.id
                  return (
                    <tr key={row.id} className={isSelf ? 'is-self' : undefined}>
                      <td>
                        <div className="admin__user-cell">
                          <span className="admin__mini-avatar" aria-hidden="true">
                            {(row.full_name || row.username).slice(0, 2).toUpperCase()}
                          </span>
                          <div>
                            <strong>{row.full_name || row.username}</strong>
                            <span className="muted">@{row.username} · {row.email}</span>
                          </div>
                        </div>
                      </td>
                      <td>
                        <span className={`chip ${row.role === 'admin' ? 'chip--admin' : ''}`}>
                          {row.role === 'admin' && <ShieldCheck size={13} />}
                          {row.role}
                        </span>
                      </td>
                      <td>
                        <span className={`chip ${row.is_active ? 'chip--ok' : 'chip--off'}`}>
                          {row.is_active ? 'Active' : 'Disabled'}
                        </span>
                      </td>
                      <td className="muted">{formatDate(row.created_at)}</td>
                      <td className="right">
                        <div className="admin__row-actions">
                          <button
                            className="icon-btn"
                            type="button"
                            title={row.role === 'admin' ? 'Demote to user' : 'Promote to admin'}
                            aria-label={row.role === 'admin' ? `Demote ${row.username}` : `Promote ${row.username}`}
                            disabled={busy || isSelf}
                            onClick={() =>
                              act(row.id, { role: row.role === 'admin' ? 'user' : 'admin' },
                                row.role === 'admin' ? `${row.username} is now a user` : `${row.username} is now an admin`)
                            }
                          >
                            {row.role === 'admin' ? <UserX size={16} /> : <ShieldCheck size={16} />}
                          </button>

                          <button
                            className="icon-btn"
                            type="button"
                            title={row.is_active ? 'Disable account' : 'Enable account'}
                            aria-label={row.is_active ? `Disable ${row.username}` : `Enable ${row.username}`}
                            disabled={busy || isSelf}
                            onClick={() =>
                              act(row.id, { is_active: !row.is_active },
                                row.is_active ? `${row.username} disabled` : `${row.username} enabled`)
                            }
                          >
                            {row.is_active ? <UserX size={16} /> : <UserCheck size={16} />}
                          </button>

                          <button
                            className="icon-btn icon-btn--danger"
                            type="button"
                            title="Delete account"
                            aria-label={`Delete ${row.username}`}
                            disabled={busy || isSelf}
                            onClick={() => remove(row)}
                          >
                            <Trash2 size={16} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  )
                })}
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

      <p className="admin__note">
        <RotateCcw size={15} />
        You cannot change your own role or delete your own account, and the last active admin is
        always protected.
      </p>
    </div>
  )
}
