/**
 * User dashboard.
 *
 * A signed-in user's home: their profile, the role they hold, a quick jump back
 * into the detection tool, and self-service updates for display name / password.
 * Every save goes through the protected `PATCH /users/me` endpoint, so it requires
 * a valid token and can only ever change the caller's own account.
 */

import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Leaf, LogOut, Pencil, Stethoscope, ShieldCheck, User as UserIcon,
  Mail, CalendarDays, AlertCircle, CheckCircle2, KeyRound,
} from 'lucide-react'
import { useAuth } from '../../context/AuthContext.jsx'
import { useApp } from '../../context/AppContext.jsx'
import { authApi } from '../../api/auth.js'
import PasswordField from '../../components/auth/PasswordField.jsx'

const QUICK_LINKS = [
  { to: '/detect', icon: Stethoscope, title: 'Run a diagnosis', text: 'Upload a leaf photo and get a treatment plan.' },
  { to: '/problems', icon: Leaf, title: 'Browse diseases', text: 'Pests, fungi, viruses and nutrient problems.' },
  { to: '/database', icon: ShieldCheck, title: 'Plant database', text: 'Search the full offline knowledge base.' },
]

function formatDate(value) {
  if (!value) return '—'
  try {
    return new Date(value).toLocaleDateString(undefined, { day: 'numeric', month: 'long', year: 'numeric' })
  } catch {
    return '—'
  }
}

export default function UserDashboard() {
  const { user, logout, refresh, isAdmin } = useAuth()
  const { notify } = useApp()
  const navigate = useNavigate()

  const [editing, setEditing] = useState(false)
  const [fullName, setFullName] = useState(user?.full_name || '')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [errors, setErrors] = useState({})
  const [formError, setFormError] = useState('')
  const [saving, setSaving] = useState(false)

  if (!user) return null

  async function saveProfile(e) {
    e.preventDefault()
    setFormError('')
    const next = {}
    if (password) {
      if (password.length < 8 || !/[A-Z]/.test(password) || !/\d/.test(password)) {
        next.password = 'Password needs 8+ characters, an uppercase letter and a number.'
      }
      if (password !== confirm) next.confirm = 'The two passwords do not match.'
    }
    setErrors(next)
    if (Object.keys(next).length) return

    setSaving(true)
    try {
      const payload = {}
      if (fullName.trim() !== (user.full_name || '')) payload.full_name = fullName.trim() || null
      if (password) payload.password = password
      if (Object.keys(payload).length) {
        await authApi.updateProfile(payload)
        await refresh()
        notify('Profile updated')
      }
      setPassword('')
      setConfirm('')
      setEditing(false)
    } catch (err) {
      setFormError(err.message || 'Could not save your changes.')
    } finally {
      setSaving(false)
    }
  }

  async function onLogout() {
    await logout()
    notify('Signed out successfully')
    navigate('/', { replace: true })
  }

  const initials = (user.full_name || user.username).slice(0, 2).toUpperCase()

  return (
    <div className="page container dash">
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }}>
        {/* ---------- Header ---------- */}
        <div className="dash__head panel">
          <div className="dash__avatar" aria-hidden="true">{initials}</div>
          <div className="dash__head-main">
            <p className="dash__eyebrow">My account</p>
            <h1>Welcome, {user.full_name || user.username}</h1>
            <div className="dash__meta">
              <span className="chip">
                <ShieldCheck size={14} />
                {isAdmin ? 'Administrator' : 'User'}
              </span>
              <span className="muted">
                <Mail size={14} /> {user.email}
              </span>
              <span className="muted">
                <CalendarDays size={14} /> Joined {formatDate(user.created_at)}
              </span>
            </div>
          </div>
          <div className="dash__head-actions">
            {isAdmin && (
              <Link className="btn btn-ghost btn-sm" to="/admin">Admin dashboard</Link>
            )}
            <button className="btn btn-sm" type="button" onClick={onLogout}>
              <LogOut size={15} /> Logout
            </button>
          </div>
        </div>

        {/* ---------- Quick links ---------- */}
        <div className="grid grid--3 mt-2">
          {QUICK_LINKS.map(({ to, icon: Icon, title, text }) => (
            <Link key={to} to={to} className="panel dash__quick">
              <span className="dash__quick-icon"><Icon size={20} /></span>
              <strong>{title}</strong>
              <p className="muted">{text}</p>
            </Link>
          ))}
        </div>

        {/* ---------- Profile ---------- */}
        <section className="panel mt-3 dash__section">
          <div className="dash__section-head">
            <h2><UserIcon size={20} /> Profile details</h2>
            <button className="btn btn-ghost btn-sm" type="button" onClick={() => setEditing((v) => !v)}>
              <Pencil size={14} /> {editing ? 'Cancel' : 'Edit profile'}
            </button>
          </div>

          {formError && (
            <div className="auth__alert auth__alert--error" role="alert">
              <AlertCircle size={18} /><span>{formError}</span>
            </div>
          )}

          {editing ? (
            <form onSubmit={saveProfile} noValidate>
              <div className="field">
                <label htmlFor="dashName">Full name</label>
                <input
                  id="dashName" className="input" type="text" value={fullName}
                  onChange={(e) => setFullName(e.target.value)} disabled={saving}
                />
              </div>
              <PasswordField
                id="dashPassword" label="New password" value={password}
                onChange={(e) => { setPassword(e.target.value); setErrors((s) => ({ ...s, password: undefined })) }}
                autoComplete="new-password" error={errors.password}
                hint="Leave blank to keep your current password." disabled={saving}
              />
              {password && (
                <PasswordField
                  id="dashConfirm" label="Confirm new password" value={confirm}
                  onChange={(e) => { setConfirm(e.target.value); setErrors((s) => ({ ...s, confirm: undefined })) }}
                  autoComplete="new-password" error={errors.confirm} disabled={saving}
                />
              )}
              <div className="dash__actions">
                <button className="btn" type="submit" disabled={saving}>
                  {saving ? <><span className="spinner" aria-hidden="true" /> Saving…</> : <><CheckCircle2 size={16} /> Save changes</>}
                </button>
                <button className="btn btn-ghost" type="button" onClick={() => setEditing(false)} disabled={saving}>
                  Cancel
                </button>
              </div>
            </form>
          ) : (
            <dl className="dash__details">
              <div><dt>Full name</dt><dd>{user.full_name || '—'}</dd></div>
              <div><dt>Username</dt><dd>{user.username}</dd></div>
              <div><dt>Email</dt><dd>{user.email}</dd></div>
              <div><dt>Role</dt><dd><span className="chip">{isAdmin ? 'Administrator' : 'User'}</span></dd></div>
              <div><dt>Status</dt><dd><span className="chip">Active</span></dd></div>
              <div><dt>Member since</dt><dd>{formatDate(user.created_at)}</dd></div>
            </dl>
          )}
        </section>

        <p className="dash__note">
          <KeyRound size={14} />
          Your password is hashed with bcrypt on the server and is never sent back to this browser.
        </p>
      </motion.div>
    </div>
  )
}
