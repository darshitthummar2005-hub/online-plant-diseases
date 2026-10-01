import { db } from '../db/database.js'
import { PLANT_GROUPS } from '../db/seed.js'

// Dev falls back to the local backend; production falls back to same-origin
// /api so a missing VITE_API_URL can never point browsers at localhost.
const API_BASE = (
  import.meta.env.VITE_API_URL ||
  (import.meta.env.DEV ? 'http://localhost:8000/api' : '/api')
).replace(/\/$/, '')

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text()
    let detail = text
    try {
      detail = JSON.parse(text)?.detail || text
    } catch {
      /* keep raw text */
    }
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail))
  }
  return res.json()
}

function qs(params = {}) {
  const clean = Object.fromEntries(Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== ''))
  const s = new URLSearchParams(clean).toString()
  return s ? `?${s}` : ''
}

export const api = {
  base: API_BASE,

  /** Cheap reachability probe — throws if the backend is offline. */
  async ping() {
    await fetch(API_BASE.replace(/\/api$/, '') + '/health', { method: 'GET' })
  },

  /** GET /diseases — paginated list. */
  listDiseases(params = {}) {
    return request(`/diseases${qs({ page_size: 100, ...params })}`)
  },

  /** GET /diseases/:id — one full disease record. */
  getDisease(id) {
    return request(`/diseases/${id}`)
  },

  /** POST /detect — full AI Plant Doctor diagnosis report. */
  runDetection(payload) {
    return request('/detect', { method: 'POST', body: JSON.stringify(payload) })
  },
}

/** Downscale an image File into a compact base64 data-URL (JPEG) for API upload. */
export function fileToDataUrl(file, maxDim = 900) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file)
    const img = new Image()
    img.onload = () => {
      try {
        const scale = Math.min(1, maxDim / Math.max(img.width, img.height))
        const w = Math.max(1, Math.round(img.width * scale))
        const h = Math.max(1, Math.round(img.height * scale))
        const canvas = document.createElement('canvas')
        canvas.width = w
        canvas.height = h
        canvas.getContext('2d').drawImage(img, 0, 0, w, h)
        URL.revokeObjectURL(url)
        resolve(canvas.toDataURL('image/jpeg', 0.82))
      } catch (err) {
        URL.revokeObjectURL(url)
        reject(err)
      }
    }
    img.onerror = () => {
      URL.revokeObjectURL(url)
      reject(new Error('Could not read the selected image'))
    }
    img.src = url
  })
}

const cleanName = (value) =>
  String(value || '').toLowerCase().replace(/[^a-z ]/g, ' ').trim()

const plantEquivalent = (affected, plant) => {
  const a = cleanName(affected)
  const p = cleanName(plant)
  if (!a || !p) return false
  if (a === p) return true
  if (a.startsWith(p) && a.length <= p.length + 3) return true
  if (p.startsWith(a) && p.length <= a.length + 3) return true
  if ((PLANT_GROUPS[a] || []).includes(p)) return true
  const aTokens = new Set(a.split(' '))
  const pTokens = new Set(p.split(' '))
  return [...aTokens].some((t) => pTokens.has(t))
}

const plantScore = (d, plant) => {
  if (!plant) return false
  const affected = (d.affectedPlants || d.affected_plants || []).map(cleanName).filter(Boolean)
  return affected.some((a) => plantEquivalent(a, plant))
}

/**
 * Offline fallback: rank diseases by symptom keywords + selected plant and
 * shape the result like the backend DetectResponse.
 */
export async function localDetect(symptoms = [], imagePresent = false, plant = null) {
  const all = await db.diseases.toArray()
  const cleaned = cleanName(plant)
  const scored = all
    .map((d) => {
      const kw = [...(d.symptomKeywords ?? []), ...String(d.name).toLowerCase().split(' ')]
      const matched = symptoms.filter((k) => kw.some((x) => x.includes(k) || k.includes(x)))
      const pMatch = plantScore(d, cleaned)
      return { d, matched, pMatch }
    })
    .filter((x) => x.matched.length > 0)
    .sort((a, b) => {
      const aScore = a.matched.length * 10 + (a.pMatch ? 60 : -45)
      const bScore = b.matched.length * 10 + (b.pMatch ? 60 : -45)
      if (bScore !== aScore) return bScore - aScore
      return b.matched.length - a.matched.length
    })

  const top = scored[0]
  const plantUnknown = Boolean(cleaned) && !scored.some((x) => x.pMatch)
  const base = top ? top.matched.length : 0
  let confidence = top
    ? Math.min(97, 55 + base * 9 + (imagePresent ? 6 : 0))
    : 0
  if (top && !top.pMatch && cleaned) confidence = Math.max(0, confidence - 15)
  const severity = top?.d?.severity || 'Moderate'

  return {
    disease_id: top ? String(top.d.id) : null,
    disease_name: top?.d?.name || 'Unknown',
    plant: plant || null,
    confidence,
    severity,
    matched_symptoms: top?.matched || [],
    unmatched_symptoms: symptoms.filter((s) => !(top?.matched || []).includes(s)),
    visual_signals: [],
    expert_recommended: !top || confidence < 70 || /high|severe/i.test(severity) || plantUnknown,
    consult_reason: !top
      ? plant
        ? `No disease could be identified for ${plant} from the knowledge base.`
        : 'No disease could be identified from the knowledge base.'
      : plantUnknown
        ? `No disease in our database is known to affect ${plant} — the diagnosis below is based on symptoms only and should be confirmed.`
        : confidence < 70
          ? 'Confidence is below 70% — this diagnosis should be confirmed by an expert.'
          : null,
    model_version: 'local-offline-v1',
    predicted_at: new Date().toISOString(),
    category: top?.d?.type,
    scientific_name: null,
    description: top?.d?.description || null,
    symptoms: top?.d?.symptomKeywords || [],
    causes: [],
    treatment: top?.d?.treatment ? [top.d.treatment] : [],
    prevention: top?.d?.prevention ? [top.d.prevention] : [],
    affected_plants: top?.d?.affectedPlants || top?.d?.affected_plants || [],
    chemical_treatment: [],
    biological_treatment: [],
    organic_remedies: [],
    prevention_tips: [],
    fertilizer: {},
    severity_levels: {},
    weather_conditions: {},
    emergency_actions: [],
    extra: {},
  }
}
