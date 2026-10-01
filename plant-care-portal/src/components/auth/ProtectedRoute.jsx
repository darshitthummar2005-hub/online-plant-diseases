/**
 * Route guard.
 *
 * `role` is optional:
 *   - omitted  → any signed-in user may view the page
 *   - 'admin'  → only an account whose role is "admin" may view it
 *
 * Anonymous visitors are sent to /login (remembering where they were headed) and
 * non-admins are bounced off admin pages, so typing an admin URL gets you
 * nowhere. This is a UX convenience only: the same rule is enforced server-side
 * by `get_current_admin`, so a hand-crafted request is rejected with 403 too.
 */

import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext.jsx'
import { Leaf } from 'lucide-react'

function FullPageLoader() {
  return (
    <div className="auth-gate" role="status" aria-live="polite">
      <div className="auth-gate__spinner" aria-hidden="true">
        <Leaf size={26} />
      </div>
      <p className="muted">Checking your session…</p>
    </div>
  )
}

export default function ProtectedRoute({ role, children }) {
  const { isAuthenticated, isAdmin, initialising, user } = useAuth()
  const location = useLocation()

  // Wait for the stored token to be validated before deciding anything.
  if (initialising) return <FullPageLoader />

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }

  if (role === 'admin' && !isAdmin) {
    return (
      <div className="auth-gate">
        <div className="auth-gate__card panel">
          <span className="auth-gate__icon" aria-hidden="true">
            <Leaf size={28} />
          </span>
          <h1>Admins only</h1>
          <p className="muted">
            You are signed in as <strong>{user.username}</strong>, which is a standard user
            account. The admin dashboard is not available for this account.
          </p>
          <a className="btn" href="/#/dashboard">
            Go to my dashboard
          </a>
        </div>
      </div>
    )
  }

  return children
}
