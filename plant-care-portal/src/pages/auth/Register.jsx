/**
 * Sign-up page for ONLINE PLANT DISEASES.
 *
 * Collects a full name, a username *or* an email, a password and a confirmation.
 * The backend derives whichever identifier was left out, hashes the password
 * with bcrypt and hard-assigns the `user` role — there is no way to self-register
 * as an admin from this form or from the API.
 */

import { useMemo, useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Leaf, Mail, User as UserIcon, UserPlus, AlertCircle, CheckCircle2 } from 'lucide-react'
import { useAuth } from '../../context/AuthContext.jsx'
import { useApp } from '../../context/AppContext.jsx'
import PasswordField from '../../components/auth/PasswordField.jsx'

/** Mirrors the server rule: 8+ chars, at least one uppercase and one digit. */
function scorePassword(value) {
  const checks = [
    { label: '8+ characters', ok: value.length >= 8 },
    { label: 'An uppercase letter', ok: /[A-Z]/.test(value) },
    { label: 'A number', ok: /\d/.test(value) },
  ]
  return { checks, passed: checks.filter((c) => c.ok).length }
}

export default function Register() {
  const { register, login, isAuthenticated, isAdmin } = useAuth()
  const { notify } = useApp()
  const navigate = useNavigate()

  const [form, setForm] = useState({ fullName: '', identifier: '', password: '', confirm: '' })
  const [errors, setErrors] = useState({})
  const [formError, setFormError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const strength = useMemo(() => scorePassword(form.password), [form.password])

  function update(key, value) {
    setForm((s) => ({ ...s, [key]: value }))
    setErrors((s) => ({ ...s, [key]: undefined, confirm: undefined }))
    setFormError('')
  }

  function validate() {
    const next = {}
    const id = form.identifier.trim()

    if (!form.fullName.trim()) next.fullName = 'Tell us your name.'
    else if (form.fullName.trim().length < 2) next.fullName = 'That name looks too short.'

    if (!id) next.identifier = 'Choose a username or enter your email.'
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(id) && !/^[a-zA-Z0-9_]{3,30}$/.test(id)) {
      next.identifier = 'Use 3–30 letters, digits or underscores, or a valid email address.'
    }

    if (!form.password) next.password = 'Choose a password.'
    else if (strength.passed < 3) next.password = 'Password needs 8+ characters, an uppercase letter and a number.'

    if (!form.confirm) next.confirm = 'Re-enter your password.'
    else if (form.confirm !== form.password) next.confirm = 'The two passwords do not match.'

    setErrors(next)
    return Object.keys(next).length === 0
  }

  async function onSubmit(e) {
    e.preventDefault()
    setFormError('')
    if (!validate()) return

    setSubmitting(true)
    try {
      const id = form.identifier.trim()
      const isEmail = id.includes('@')

      // Send the single identifier; the backend derives the missing one.
      await register({
        full_name: form.fullName.trim(),
        username: isEmail ? undefined : id,
        email: isEmail ? id : undefined,
        password: form.password,
      })

      // Sign the new account straight in — no second form for the same user.
      const user = await login(id, form.password)
      setForm({ fullName: '', identifier: '', password: '', confirm: '' })
      notify(`Welcome to ONLINE PLANT DISEASES, ${user.full_name || user.username}!`)
      navigate('/dashboard', { replace: true })
    } catch (err) {
      setFormError(err.message || 'Unable to create your account. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  if (isAuthenticated) return <Navigate to={isAdmin ? '/admin' : '/dashboard'} replace />

  return (
    <div className="auth">
      <aside className="auth__aside" aria-hidden="true">
        <div className="auth__aside-inner">
          <div className="auth__logo">
            <span className="brand-badge">
              <Leaf size={24} />
            </span>
            <div>
              <strong>ONLINE PLANT DISEASES</strong>
              <small>Grow healthy. Detect early.</small>
            </div>
          </div>
          <h2 className="auth__pitch">
            Join a community that spots disease <em>before</em> it takes the whole crop.
          </h2>
          <ul className="auth__highlights">
            <li>
              <span className="auth__highlight-icon"><CheckCircle2 size={18} /></span>
              <div><strong>Free forever</strong><p>Unlimited detections, no card required.</p></div>
            </li>
            <li>
              <span className="auth__highlight-icon"><CheckCircle2 size={18} /></span>
              <div><strong>Your own dashboard</strong><p>Every diagnosis and profile in one place.</p></div>
            </li>
            <li>
              <span className="auth__highlight-icon"><CheckCircle2 size={18} /></span>
              <div><strong>Standard account</strong><p>New sign-ups are always regular users.</p></div>
            </li>
          </ul>
        </div>
        <Leaf className="auth__blob auth__blob--1" size={220} />
        <Leaf className="auth__blob auth__blob--2" size={150} />
      </aside>

      <main className="auth__panel">
        <motion.div
          className="auth__card"
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: 'easeOut' }}
        >
          <div className="auth__card-logo" aria-hidden="true"><Leaf size={26} /></div>
          <h1 className="auth__title">Create your account</h1>
          <p className="auth__sub">Free access to the full disease library and AI Plant Doctor.</p>

          {formError && (
            <div className="auth__alert auth__alert--error" role="alert">
              <AlertCircle size={18} /><span>{formError}</span>
            </div>
          )}

          <form onSubmit={onSubmit} noValidate>
            <div className="field">
              <label htmlFor="fullName">Full name</label>
              <div className={`pw-wrap ${errors.fullName ? 'pw-wrap--error' : ''}`}>
                <span className="pw-wrap__icon" aria-hidden="true"><UserIcon size={17} /></span>
                <input
                  id="fullName" className="input pw-wrap__input" type="text"
                  value={form.fullName} onChange={(e) => update('fullName', e.target.value)}
                  placeholder="Priya Sharma" autoComplete="name" disabled={submitting}
                  aria-invalid={errors.fullName ? 'true' : undefined}
                />
              </div>
              {errors.fullName && <small className="field-error" role="alert">{errors.fullName}</small>}
            </div>

            <div className="field">
              <label htmlFor="identifier">Username or email</label>
              <div className={`pw-wrap ${errors.identifier ? 'pw-wrap--error' : ''}`}>
                <span className="pw-wrap__icon" aria-hidden="true"><Mail size={17} /></span>
                <input
                  id="identifier" className="input pw-wrap__input" type="text"
                  value={form.identifier} onChange={(e) => update('identifier', e.target.value)}
                  placeholder="priya_garden or priya@example.com"
                  autoComplete="username" autoCapitalize="none" spellCheck="false"
                  disabled={submitting}
                  aria-invalid={errors.identifier ? 'true' : undefined}
                />
              </div>
              {errors.identifier && <small className="field-error" role="alert">{errors.identifier}</small>}
            </div>

            <PasswordField
              id="newPassword" label="Password" value={form.password}
              onChange={(e) => update('password', e.target.value)}
              autoComplete="new-password" error={errors.password} disabled={submitting}
            />

            {form.password && (
              <ul className="pw-strength" aria-label="Password requirements">
                {strength.checks.map((c) => (
                  <li key={c.label} className={c.ok ? 'ok' : ''}>
                    {c.ok ? <CheckCircle2 size={13} /> : <span className="dot" />} {c.label}
                  </li>
                ))}
              </ul>
            )}

            <PasswordField
              id="confirmPassword" label="Confirm password" value={form.confirm}
              onChange={(e) => update('confirm', e.target.value)}
              autoComplete="new-password" error={errors.confirm} disabled={submitting}
            />

            <button className="btn auth__submit" type="submit" disabled={submitting}>
              {submitting ? (
                <><span className="spinner" aria-hidden="true" /> Creating account…</>
              ) : (
                <><UserPlus size={18} /> Create account</>
              )}
            </button>
          </form>

          <p className="auth__switch">
            Already registered? <Link to="/login">Sign in</Link>
          </p>
          <Link className="auth__back" to="/">← Back to the website</Link>
        </motion.div>
      </main>
    </div>
  )
}
