/**
 * Admin dashboard shell.
 *
 * Provides the responsive sidebar, the topbar with the signed-in admin's name and
 * role pill, and the nested routes for each admin section. Mounted only behind
 * <ProtectedRoute role="admin">, and every API call it makes is independently
 * rejected server-side for non-admins.
 */

import { useEffect, useState } from 'react'
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  LayoutDashboard, Users, Stethoscope, Leaf, MessageSquare, Menu, X,
  LogOut, ShieldCheck, ExternalLink,
} from 'lucide-react'
import { useAuth } from '../../context/AuthContext.jsx'
import { useApp } from '../../context/AppContext.jsx'

const SECTIONS = [
  { to: '/admin', end: true, icon: LayoutDashboard, label: 'Overview' },
  { to: '/admin/users', icon: Users, label: 'Users' },
  { to: '/admin/detections', icon: Stethoscope, label: 'Detections' },
  { to: '/admin/diseases', icon: Leaf, label: 'Disease data' },
  { to: '/admin/feedback', icon: MessageSquare, label: 'Feedback' },
]

export default function AdminLayout() {
  const { user, logout, isAdmin } = useAuth()
  const { notify } = useApp()
  const navigate = useNavigate()
  const location = useLocation()
  const [open, setOpen] = useState(false)

  // Close the mobile drawer whenever the route changes.
  useEffect(() => setOpen(false), [location.pathname])

  if (!user || !isAdmin) return null

  const current = SECTIONS.find((s) => (s.end ? location.pathname === s.to : location.pathname.startsWith(s.to)))

  async function onLogout() {
    await logout()
    notify('Signed out successfully')
    navigate('/', { replace: true })
  }

  return (
    <div className="admin">
      {/* ---------- Sidebar ---------- */}
      <aside className={`admin__sidebar ${open ? 'open' : ''}`}>
        <div className="admin__brand">
          <span className="brand-badge"><Leaf size={20} /></span>
          <div>
            <strong>ONLINE PLANT DISEASES</strong>
            <small>Admin console</small>
          </div>
        </div>

        <nav className="admin__nav" aria-label="Admin sections">
          {SECTIONS.map(({ to, end, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) => `admin__nav-link ${isActive ? 'active' : ''}`}
            >
              <Icon size={18} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="admin__sidebar-foot">
          <a className="admin__nav-link" href="/#/" target="_blank" rel="noreferrer">
            <ExternalLink size={18} />
            <span>View website</span>
          </a>
          <button className="admin__nav-link admin__nav-link--danger" type="button" onClick={onLogout}>
            <LogOut size={18} />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {open && <div className="admin__scrim" onClick={() => setOpen(false)} aria-hidden="true" />}

      {/* ---------- Main column ---------- */}
      <div className="admin__main">
        <header className="admin__topbar">
          <button
            className="admin__burger"
            type="button"
            onClick={() => setOpen((v) => !v)}
            aria-label={open ? 'Close menu' : 'Open menu'}
            aria-expanded={open}
          >
            {open ? <X size={20} /> : <Menu size={20} />}
          </button>

          <div className="admin__topbar-main">
            <p className="admin__topbar-title">{current?.label || 'Overview'}</p>
            <p className="admin__topbar-sub">ONLINE PLANT DISEASES control panel</p>
          </div>

          <div className="admin__identity">
            <div className="admin__identity-text">
              <strong>{user.full_name || user.username}</strong>
              <span className="admin__role">ADMIN</span>
            </div>
            <span className="admin__avatar" aria-hidden="true">
              {(user.full_name || user.username).slice(0, 2).toUpperCase()}
            </span>
          </div>
        </header>

        <motion.main
          className="admin__content"
          key={location.pathname}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.28, ease: 'easeOut' }}
        >
          <Outlet />
        </motion.main>
      </div>
    </div>
  )
}
