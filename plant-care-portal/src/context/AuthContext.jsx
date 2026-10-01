/**
 * Authentication context for ONLINE PLANT DISEASES.
 *
 * Responsibilities:
 *   - hold the current `user` (never a password) and the session status;
 *   - log in / register against the backend and persist the returned JWT;
 *   - re-validate a stored token on mount via `GET /auth/me`, so a revoked or
 *     expired session cannot survive a page refresh;
 *   - log out, asking the backend to revoke the token before clearing it.
 *
 * The role shown here comes from the server response. It is used only to decide
 * what to render — the real authorization gate is on the API, so tampering with
 * the frontend state grants nothing.
 */

import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import { authApi, setUnauthorizedHandler, tokenStore } from '../api/auth.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [initialising, setInitialising] = useState(true)
  // Guards against a second logout call firing while the first is in flight.
  const loggingOut = useRef(false)

  const clearSession = useCallback(() => {
    tokenStore.set(null)
    setUser(null)
  }, [])

  // Any 401 from the API client means this session is no longer valid.
  useEffect(() => {
    setUnauthorizedHandler(() => {
      tokenStore.set(null)
      setUser(null)
    })
  }, [])

  // Restore + re-validate a stored session on first load.
  useEffect(() => {
    let cancelled = false

    async function restore() {
      const token = tokenStore.get()
      if (!token) {
        setInitialising(false)
        return
      }
      try {
        const me = await authApi.me()
        if (!cancelled) setUser(me)
      } catch {
        // Expired, revoked or invalid — drop it silently and show the site as
        // signed out rather than flashing an error at the user.
        tokenStore.set(null)
        if (!cancelled) setUser(null)
      } finally {
        if (!cancelled) setInitialising(false)
      }
    }

    restore()
    return () => {
      cancelled = true
    }
  }, [])

  const login = useCallback(async (identifier, password) => {
    const data = await authApi.login(identifier, password)
    tokenStore.set(data.access_token)
    setUser(data.user)
    return data.user
  }, [])

  const register = useCallback(async (payload) => authApi.register(payload), [])

  const logout = useCallback(async () => {
    if (loggingOut.current) return
    loggingOut.current = true
    try {
      // Revoke server-side so a copied token stops working immediately.
      await authApi.logout()
    } catch {
      /* already invalid or offline — clearing locally is still correct */
    } finally {
      clearSession()
      loggingOut.current = false
    }
  }, [clearSession])

  const refresh = useCallback(async () => {
    const me = await authApi.me()
    setUser(me)
    return me
  }, [])

  const value = useMemo(
    () => ({
      user,
      initialising,
      isAuthenticated: Boolean(user),
      isAdmin: user?.role === 'admin',
      login,
      register,
      logout,
      refresh,
    }),
    [user, initialising, login, register, logout, refresh],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>')
  return ctx
}
