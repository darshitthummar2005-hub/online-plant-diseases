/**
 * Auth + admin API client.
 *
 * Every call carries the stored JWT in the `Authorization: Bearer` header and the
 * token is attached by the client itself — no component ever handles it. A 401
 * from any request means the session is gone, so the client notifies the app to
 * sign the user out (see `onUnauthorized` in AuthContext).
 *
 * No credentials are ever stored or referenced in this file or anywhere else in
 * the frontend bundle: authentication happens entirely on the backend.
 */

// Dev falls back to the local backend; production falls back to same-origin
// /api so a missing VITE_API_URL can never point browsers at localhost.
const API_BASE = (
  import.meta.env.VITE_API_URL ||
  (import.meta.env.DEV ? 'http://localhost:8000/api' : '/api')
).replace(/\/$/, '')

const TOKEN_KEY = 'opd.auth.token'

export const tokenStore = {
  get: () => {
    try {
      return window.localStorage.getItem(TOKEN_KEY)
    } catch {
      return null
    }
  },
  set: (token) => {
    try {
      if (token) window.localStorage.setItem(TOKEN_KEY, token)
      else window.localStorage.removeItem(TOKEN_KEY)
    } catch {
      /* storage unavailable (private mode) — session lasts for this tab only */
    }
  },
}

/** Called by AuthContext so any 401 anywhere triggers a sign-out. */
let onUnauthorized = () => {}
export function setUnauthorizedHandler(fn) {
  onUnauthorized = fn
}

export class ApiError extends Error {
  constructor(message, status, payload) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.payload = payload
  }
}

async function request(path, { method = 'GET', body, auth = true } = {}) {
  const headers = {}
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  if (auth) {
    const token = tokenStore.get()
    if (token) headers.Authorization = `Bearer ${token}`
  }

  let res
  try {
    res = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
    })
  } catch {
    throw new ApiError(
      'Cannot reach the server. Make sure the backend is running on port 8000.',
      0,
    )
  }

  if (res.status === 401 && auth) {
    onUnauthorized()
  }

  const text = await res.text()
  let data = null
  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      data = text
    }
  }

  if (!res.ok) {
    // FastAPI validation errors arrive as a list of {loc, msg, type} objects.
    let message = data?.detail || `Request failed (${res.status})`
    if (Array.isArray(message)) {
      message = message.map((d) => d?.msg || String(d)).join('. ')
    }
    throw new ApiError(message, res.status, data)
  }
  return data
}

function qs(params = {}) {
  const clean = Object.fromEntries(
    Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== ''),
  )
  const s = new URLSearchParams(clean).toString()
  return s ? `?${s}` : ''
}

export const authApi = {
  /** POST /auth/register — always creates a `user`; the role is server-assigned. */
  register: (payload) => request('/auth/register', { method: 'POST', body: payload, auth: false }),

  /** POST /auth/login — identifier may be a username or an email. */
  login: (identifier, password) =>
    request('/auth/login', {
      method: 'POST',
      body: { identifier, password },
      auth: false,
    }),

  /** GET /auth/me — re-validate a stored token. */
  me: () => request('/auth/me'),

  /** POST /auth/logout — server-side token revocation. */
  logout: () => request('/auth/logout', { method: 'POST' }),

  /** PATCH /users/me — self-service profile update. */
  updateProfile: (payload) => request('/users/me', { method: 'PATCH', body: payload }),
}

export const adminApi = {
  overview: () => request('/admin/overview'),
  stats: () => request('/admin/stats'),
  users: (params) => request(`/admin/users${qs(params)}`),
  updateUser: (id, payload) => request(`/admin/users/${id}`, { method: 'PATCH', body: payload }),
  deleteUser: (id) => request(`/admin/users/${id}`, { method: 'DELETE' }),
  detections: (params) => request(`/admin/detections${qs(params)}`),
  admins: () => request('/admin/admins'),

  // Disease knowledge-base management (these endpoints are already admin-guarded
  // on the backend and are reused here rather than duplicated).
  diseases: (params) => request(`/diseases${qs({ page_size: 100, ...params })}`),
  createDisease: (payload) => request('/diseases', { method: 'POST', body: payload }),
  updateDisease: (id, payload) => request(`/diseases/${id}`, { method: 'PATCH', body: payload }),
  deleteDisease: (id) => request(`/diseases/${id}`, { method: 'DELETE' }),

  feedback: (params) => request(`/feedback${qs({ page_size: 50, ...params })}`),
}
