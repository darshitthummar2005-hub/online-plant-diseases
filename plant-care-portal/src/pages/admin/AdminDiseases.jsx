/**
 * Disease knowledge-base management.
 *
 * Reuses the existing admin-guarded `/diseases` endpoints (POST/PATCH/DELETE) so
 * there is no second source of truth for disease content. Deleting a seed disease
 * is allowed here, but the seeder will recreate it on the next backend restart.
 */

import { useCallback, useEffect, useState } from 'react'
import { Leaf, Search, Trash2, Plus, AlertCircle, X } from 'lucide-react'
import { adminApi } from '../../api/auth.js'
import { useApp } from '../../context/AppContext.jsx'

const EMPTY_FORM = { name: '', category: 'Fungal', severity: 'Moderate', description: '' }

function confirmClose() {
  return true
}

export default function AdminDiseases() {
  const { notify } = useApp()
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [q, setQ] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)
  const [busyId, setBusyId] = useState(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const res = await adminApi.diseases({ q: q || undefined })
      setRows(res.items || [])
    } catch (err) {
      setError(err.message || 'Could not load the disease library.')
    } finally {
      setLoading(false)
    }
  }, [q])

  useEffect(() => {
    const t = setTimeout(load, q ? 300 : 0)
    return () => clearTimeout(t)
  }, [load, q])

  async function create(e) {
    e.preventDefault()
    setError('')
    if (form.name.trim().length < 3) {
      setError('Disease name must be at least 3 characters.')
      return
    }
    setSaving(true)
    try {
      await adminApi.createDisease({
        name: form.name.trim(),
        category: form.category,
        severity: form.severity,
        description: form.description.trim(),
        symptoms: [],
        causes: [],
        treatment: [],
        prevention: [],
        affected_plants: [],
      })
      notify(`Added "${form.name.trim()}" to the library`)
      setForm(EMPTY_FORM)
      setShowForm(false)
      await load()
    } catch (err) {
      setError(err.message || 'Could not add that disease.')
    } finally {
      setSaving(false)
    }
  }

  async function remove(row) {
    if (!confirmClose()) return
    if (!window.confirm(`Delete "${row.name}" from the knowledge base?`)) return
    setBusyId(row.id)
    setError('')
    try {
      await adminApi.deleteDisease(row.id)
      notify(`Deleted "${row.name}"`)
      await load()
    } catch (err) {
      setError(err.message || 'Could not delete that disease.')
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div className="admin__page">
      <header className="admin__page-head admin__page-head--row">
        <div>
          <h1><Leaf size={24} /> Disease data</h1>
          <p>{rows.length} record{rows.length === 1 ? '' : 's'} in the knowledge base.</p>
        </div>
        <button className="btn" type="button" onClick={() => setShowForm((v) => !v)}>
          {showForm ? <X size={16} /> : <Plus size={16} />}
          {showForm ? 'Close' : 'Add disease'}
        </button>
      </header>

      {error && (
        <div className="auth__alert auth__alert--error" role="alert">
          <AlertCircle size={18} /><span>{error}</span>
        </div>
      )}

      {showForm && (
        <form className="panel admin__form" onSubmit={create}>
          <div className="admin__form-grid">
            <div className="field">
              <label htmlFor="dzName">Disease name</label>
              <input
                id="dzName" className="input" type="text" value={form.name} required
                onChange={(e) => setForm((s) => ({ ...s, name: e.target.value }))}
                placeholder="Powdery Mildew" disabled={saving}
              />
            </div>
            <div className="field">
              <label htmlFor="dzCat">Category</label>
              <select
                id="dzCat" className="input" value={form.category} disabled={saving}
                onChange={(e) => setForm((s) => ({ ...s, category: e.target.value }))}
              >
                {['Fungal', 'Bacterial', 'Viral', 'Pest', 'Deficiency'].map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
            <div className="field">
              <label htmlFor="dzSev">Severity</label>
              <select
                id="dzSev" className="input" value={form.severity} disabled={saving}
                onChange={(e) => setForm((s) => ({ ...s, severity: e.target.value }))}
              >
                {['Mild', 'Moderate', 'Severe'].map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="field">
            <label htmlFor="dzDesc">Description</label>
            <textarea
              id="dzDesc" className="textarea" rows={3} value={form.description} disabled={saving}
              onChange={(e) => setForm((s) => ({ ...s, description: e.target.value }))}
              placeholder="What causes it, and what does it look like?"
            />
          </div>
          <button className="btn" type="submit" disabled={saving}>
            {saving ? <><span className="spinner" aria-hidden="true" /> Saving…</> : <><Plus size={16} /> Add to library</>}
          </button>
        </form>
      )}

      <div className="admin__toolbar panel">
        <div className="admin__search">
          <Search size={17} aria-hidden="true" />
          <input
            className="input" type="search" value={q} aria-label="Search diseases"
            onChange={(e) => setQ(e.target.value)} placeholder="Search the disease library…"
          />
        </div>
      </div>

      <div className="panel admin__table-wrap">
        {loading ? (
          <div className="admin__loading" role="status" aria-live="polite">
            <span className="spinner spinner--lg" aria-hidden="true" />
            <p className="muted">Loading library…</p>
          </div>
        ) : rows.length === 0 ? (
          <p className="muted admin__empty">No diseases match your search.</p>
        ) : (
          <div className="admin__table-scroll">
            <table className="admin__table">
              <thead>
                <tr>
                  <th scope="col">Name</th>
                  <th scope="col">Category</th>
                  <th scope="col">Severity</th>
                  <th scope="col" className="right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.id}>
                    <td>
                      <strong>{row.name}</strong>
                      {row.scientific_name && <span className="muted"> · {row.scientific_name}</span>}
                    </td>
                    <td><span className="chip">{row.category || '—'}</span></td>
                    <td><span className="chip">{row.severity || '—'}</span></td>
                    <td className="right">
                      <button
                        className="icon-btn icon-btn--danger" type="button"
                        title="Delete disease" aria-label={`Delete ${row.name}`}
                        disabled={busyId === row.id} onClick={() => remove(row)}
                      >
                        <Trash2 size={16} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
