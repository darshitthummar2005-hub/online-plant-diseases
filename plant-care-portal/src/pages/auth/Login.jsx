/**
 * Sign-in page for ONLINE PLANT DISEASES.
 *
 * Submits the identifier + password to the backend, which verifies the bcrypt
 * hash and returns a JWT plus the account's role. The role decides the landing
 * page: admins go to /admin, everyone else to their dashboard (or the page they
 * originally asked for).
 */

import { useEffect, useState } from 'react'
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Leaf, LogIn, ShieldCheck, Sprout, Stethoscope, User as UserIcon, AlertCircle } from 'lucide-react'
import { useAuth } from '../../context/AuthContext.jsx'
import { useApp } from '../../context/AppContext.jsx'
import PasswordField from '../../components/auth/PasswordField.jsx'

const HIGHLIGHTS = [
  { icon: Stethoscope, title: 'Instant disease diagnosis', text: 'Upload a leaf and match symptoms against the full disease library.' },
  { icon: Sprout, title: 'Personal dashboard', text: 'Keep your profile and revisit every diagnosis you have run.' },
  { icon: ShieldCheck, title: 'Secure by design', text: 'Passwords are hashed server-side and never stored in your browser.' },
]

export default function Login() {
  const { login, isAuthenticated, isAdmin } = useAuth()
  const { notify } = useApp()
  const navigate = useNavigate()
  const location = useLocation()

  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')
  const [errors, setErrors] = useState({})
  const [formError, setFormError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const from = location.state?.from

  // Already signed in → go straight where they belong.
  useEffect(() => {
    if (isAuthenticated) navigate(isAdmin ? '/admin' : from || '/dashboard', { replace: true })
  }, [isAuthenticated, isAdmin, from, navigate])

  function validate() {
    const next = {}
    const id = identifier.trim()
    if (!id) next.identifier = 'Enter your username or email address.'
    else if (id.length < 3) next.identifier = 'That is too short to be a username or email.'
    if (!password) next.password = 'Enter your password.'
    setErrors(next)
    return Object.keys(next).length === 0
  }

  async function onSubmit(e) {
    e.preventDefault()
    setFormError('')
    if (!validate()) return

    setSubmitting(true)
    try {
      const user = await login(identifier.trim(), password)
      setPassword('') // never keep the plaintext around after submitting
      notify(`Welcome back, ${user.full_name || user.username}!`)
      navigate(user.role === 'admin' ? '/admin' : from || '/dashboard', { replace: true })
    } catch (err) {
      setFormError(err.message || 'Unable to sign in. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  if (isAuthenticated) return <Navigate to={isAdmin ? '/admin' : '/dashboard'} replace />

  return (
    <div className="auth">
      {/* ---------- Brand / marketing panel ---------- */}
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
            Protect every leaf in your garden with <em>one</em> diagnosis away from the cure.
          </h2>

          <ul className="auth__highlights">
            {HIGHLIGHTS.map(({ icon: Icon, title, text }) => (
              <li key={title}>
                <span className="auth__highlight-icon">
                  <Icon size={18} />
                </span>
                <div>
                  <strong>{title}</strong>
                  <p>{text}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
        <Leaf className="auth__blob auth__blob--1" size={220} />
        <Leaf className="auth__blob auth__blob--2" size={150} />
      </aside>

      {/* ---------- Form panel ---------- */}
      <main className="auth__panel">
        <motion.div
          className="auth__card"
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: 'easeOut' }}
        >
          <div className="auth__card-logo" aria-hidden="true">
            <Leaf size={26} />
          </div>
          <h1 className="auth__title">Sign in</h1>
          <p className="auth__sub">Welcome back to ONLINE PLANT DISEASES.</p>

          {formError && (
            <div className="auth__alert auth__alert--error" role="alert">
              <AlertCircle size={18} />
              <span>{formError}</span>
            </div>
          )}

          <form onSubmit={onSubmit} noValidate>
            <div className="field">
              <label htmlFor="identifier">Username or email</label>
              <div className={`pw-wrap ${errors.identifier ? 'pw-wrap--error' : ''}`}>
                <span className="pw-wrap__icon" aria-hidden="true">
                  <UserIcon size={17} />
                </span>
                <input
                  id="identifier"
                  className="input pw-wrap__input"
                  type="text"
                  value={identifier}
                  onChange={(e) => {
                    setIdentifier(e.target.value)
                    if (errors.identifier) setErrors((s) => ({ ...s, identifier: undefined }))
                  }}
                  placeholder="your-username"
                  autoComplete="username"
                  autoCapitalize="none"
                  spellCheck="false"
                  disabled={submitting}
                  aria-invalid={errors.identifier ? 'true' : undefined}
                  aria-describedby={errors.identifier ? 'identifier-error' : undefined}
                />
              </div>
              {errors.identifier && (
                <small className="field-error" id="identifier-error" role="alert">
                  {errors.identifier}
                </small>
              )}
            </div>

            <PasswordField
              id="password"
              label="Password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value)
                if (errors.password) setErrors((s) => ({ ...s, password: undefined }))
              }}
              autoComplete="current-password"
              error={errors.password}
              disabled={submitting}
            />

            <button className="btn auth__submit" type="submit" disabled={submitting}>
              {submitting ? (
                <>
                  <span className="spinner" aria-hidden="true" />
                  Signing in…
                </>
              ) : (
                <>
                  <LogIn size={18} />
                  Sign in
                </>
              )}
            </button>
          </form>

          <p className="auth__switch">
            New to the portal? <Link to="/register">Create an account</Link>
          </p>
          <Link className="auth__back" to="/">
            ← Back to the website
          </Link>
        </motion.div>
      </main>
    </div>
  )
}
