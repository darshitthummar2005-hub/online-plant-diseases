import { useEffect, useState } from 'react'
import { NavLink, Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Leaf, Menu, X, LogIn, LayoutDashboard, ShieldCheck, LogOut } from 'lucide-react'
import LanguageSwitcher from './LanguageSwitcher.jsx'
import { haptic } from '../../utils/haptics.js'
import { useAuth } from '../../context/AuthContext.jsx'
import { useApp } from '../../context/AppContext.jsx'

export default function Navbar() {
  const { t } = useTranslation()
  const { user, isAuthenticated, isAdmin, logout } = useAuth()
  const { notify } = useApp()
  const navigate = useNavigate()
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const links = [
    { to: '/', key: 'home', end: true },
    { to: '/detect', key: 'detect' },
    { to: '/identify', key: 'identify' },
    { to: '/problems', key: 'problems' },
    { to: '/blogs', key: 'blogs' },
    { to: '/botanist', key: 'botanist' },
    { to: '/feed', key: 'feed' },
    { to: '/community', key: 'community' },
    { to: '/database', key: 'database' },
  ]

  const onNav = (pattern = 'tap') => {
    haptic(pattern)
    setOpen(false)
  }

  async function onLogout() {
    await logout()
    setOpen(false)
    notify('Signed out successfully')
    navigate('/', { replace: true })
  }

  return (
    <header className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="container nav-inner">
        <Link to="/" className="brand" onClick={() => onNav()}>
          <span className="brand-badge">
            <Leaf size={22} />
          </span>
          <span>
            ONLINE PLANT DISEASES
            <div style={{ fontSize: '0.7rem', fontWeight: 500, color: 'var(--green-600)' }}>
              {t('brand.tagline')}
            </div>
          </span>
        </Link>

        <button
          type="button"
          className="nav-toggle"
          onClick={() => {
            haptic('pop')
            setOpen((v) => !v)
          }}
          aria-label="Toggle menu"
          aria-expanded={open}
        >
          {open ? <X size={20} /> : <Menu size={20} />}
        </button>

        <nav>
          <ul className={`nav-links ${open ? 'open' : ''}`}>
            {links.map((l) => (
              <li key={l.to}>
                <NavLink
                  to={l.to}
                  end={l.end}
                  className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
                  onClick={() => onNav()}
                >
                  {t(`nav.${l.key}`)}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        {/* ---------- Authentication controls ----------
            Kept OUT of the collapsing <ul> so Login / Sign up stay on screen
            and clickable at every width. On narrow screens the page links move
            into the burger menu while these stay pinned in the top bar. */}
        <div className="nav-auth">
          {isAuthenticated ? (
            <>
              {isAdmin && (
                <NavLink
                  to="/admin"
                  className={({ isActive }) => `nav-link nav-link--icon ${isActive ? 'active' : ''}`}
                  onClick={() => onNav()}
                  title="Admin dashboard"
                >
                  <ShieldCheck size={15} />
                  <span className="nav-link__text">Admin</span>
                </NavLink>
              )}

              <NavLink
                to="/dashboard"
                className={({ isActive }) => `nav-link nav-link--icon ${isActive ? 'active' : ''}`}
                onClick={() => onNav()}
                title="My dashboard"
              >
                <LayoutDashboard size={15} />
                <span className="nav-link__text">Dashboard</span>
              </NavLink>

              <span className="nav-auth__user" title={user.email}>
                <span className="nav-auth__avatar" aria-hidden="true">
                  {(user.full_name || user.username).slice(0, 2).toUpperCase()}
                </span>
                <span className="nav-auth__name">{user.full_name || user.username}</span>
              </span>

              <button
                className="btn btn-ghost btn-sm nav-auth__logout"
                type="button"
                onClick={onLogout}
                title="Logout"
              >
                <LogOut size={14} />
                <span className="nav-link__text">Logout</span>
              </button>
            </>
          ) : (
            <>
              <NavLink
                to="/login"
                className={({ isActive }) => `nav-link nav-link--icon ${isActive ? 'active' : ''}`}
                onClick={() => onNav()}
                title="Sign in"
              >
                <LogIn size={15} />
                <span className="nav-link__text">Login</span>
              </NavLink>
              <Link className="btn btn-sm nav-auth__cta" to="/register" onClick={() => onNav()}>
                Sign up
              </Link>
            </>
          )}

          <LanguageSwitcher />
        </div>
      </div>
    </header>
  )
}
