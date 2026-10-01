import { useMemo, useState, useEffect } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { useTranslation } from 'react-i18next'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Database as DatabaseIcon,
  Search,
  Plus,
  Trash2,
  Save,
  Bug,
  Sprout,
  HardDrive,
  Cloud,
  WifiOff,
  Lock,
  ChevronDown,
  ChevronUp,
  FlaskConical,
  Leaf,
  ShieldCheck,
  Siren,
} from 'lucide-react'
import PageHeader from '../components/ui/PageHeader.jsx'
import { useApp } from '../context/AppContext.jsx'
import { haptic } from '../utils/haptics.js'
import { db } from '../db/database.js'
import { api } from '../api/client.js'

export default function Database() {
  const { t } = useTranslation()
  const { notify } = useApp()
  const [tab, setTab] = useState('diseases')
  const [query, setQuery] = useState('')
  const [adding, setAdding] = useState(false)
  const [form, setForm] = useState({ name: '', type: 'Disease', details: '' })
  const [mode, setMode] = useState('local') // 'api' (read-only MongoDB) | 'local' (IndexedDB CRUD)
  const [remoteDiseases, setRemoteDiseases] = useState([])
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState({})

  const localDiseases = useLiveQuery(() => db.diseases.toArray(), []) ?? []
  const plants = useLiveQuery(() => db.plants.toArray(), []) ?? []

  useEffect(() => {
    let active = true
    ;(async () => {
      try {
        const data = await api.listDiseases({ page_size: 100 })
        if (!active) return
        setRemoteDiseases(data.items || [])
        setMode('api')
      } catch {
        /* offline — stay in local mode */
      } finally {
        if (active) setLoading(false)
      }
    })()
    return () => {
      active = false
    }
  }, [])

  const diseases = mode === 'api' ? remoteDiseases : localDiseases
  const rows = tab === 'diseases' ? diseases : plants
  const readonly = mode === 'api' && tab === 'diseases'

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return rows
    return rows.filter((r) => JSON.stringify(r).toLowerCase().includes(q))
  }, [rows, query])

  const switchTab = (t2) => {
    haptic('tap')
    setTab(t2)
  }

  const switchMode = (m) => {
    if (m === mode) return
    haptic('tap')
    setMode(m)
    setAdding(false)
    setExpanded({})
  }

  const toggleExpanded = (id) => {
    haptic('tap')
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }))
  }

  const save = async () => {
    if (!form.name.trim()) {
      notify('Name is required', 'error')
      return
    }
    haptic('success')
    const record = { name: form.name, updatedAt: Date.now() }
    if (tab === 'diseases') {
      record.type = form.type
      record.severity = 'Medium'
      record.treatment = form.details || 'Consult a botanist for treatment.'
      record.prevention = 'Maintain healthy growing conditions.'
      await db.diseases.add(record)
    } else {
      record.family = form.type
      record.care = form.details || 'Keep in suitable light and water.'
      await db.plants.add(record)
    }
    setForm({ name: '', type: tab === 'diseases' ? 'Disease' : 'Plant', details: '' })
    setAdding(false)
    notify(t('database.saved'))
  }

  const remove = async (id) => {
    haptic('pop')
    if (tab === 'diseases') await db.diseases.delete(id)
    else await db.plants.delete(id)
    notify(t('database.deleted'))
  }

  const rich = (r) => ({
    chem: r.chemical_treatment || [],
    bio: r.biological_treatment || [],
    org: r.organic_remedies || [],
    fert: r.fertilizer || {},
    tips: r.prevention_tips || [],
    emergency: r.emergency_actions || [],
  })

  return (
    <div className="page">
      <div className="container">
        <PageHeader title={t('database.title')} sub={t('database.sub')} emoji="🗄️" />

        <p
          className="glass"
          style={{
            padding: 12,
            marginBottom: 22,
            fontSize: '0.9rem',
            display: 'flex',
            alignItems: 'center',
            gap: 8,
          }}
        >
          {mode === 'api' ? <Cloud size={16} /> : <WifiOff size={16} />}
          {loading
            ? t('misc.loading')
            : mode === 'api'
              ? t('database.apiLabel')
              : t('database.localLabel')}
        </p>

        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 20, alignItems: 'center' }}>
          <button
            type="button"
            className={`btn btn-sm ${tab === 'diseases' ? '' : 'btn-ghost'}`}
            onClick={() => switchTab('diseases')}
          >
            <Bug size={16} /> {t('database.tabDiseases')}
          </button>
          <button
            type="button"
            className={`btn btn-sm ${tab === 'plants' ? '' : 'btn-ghost'}`}
            onClick={() => switchTab('plants')}
          >
            <Sprout size={16} /> {t('database.tabPlants')}
          </button>

          <div style={{ flex: 1 }} />

          <div className="chip" style={{ padding: 4, gap: 4 }}>
            <button
              type="button"
              className="chip"
              style={{
                border: 'none',
                background: mode === 'api' ? 'var(--green-600)' : 'transparent',
                color: mode === 'api' ? '#fff' : 'var(--green-700)',
              }}
              onClick={() => switchMode('api')}
              disabled={loading || mode === 'api'}
            >
              <Cloud size={14} /> MongoDB
            </button>
            <button
              type="button"
              className="chip"
              style={{
                border: 'none',
                background: mode === 'local' ? 'var(--green-600)' : 'transparent',
                color: mode === 'local' ? '#fff' : 'var(--green-700)',
              }}
              onClick={() => switchMode('local')}
            >
              <HardDrive size={14} /> {t('database.localTab')}
            </button>
          </div>

          {!readonly && (
            <button
              type="button"
              className="btn btn-sm"
              onClick={() => { haptic('tap'); setAdding((v) => !v) }}
            >
              <Plus size={16} /> {t('database.addNew')}
            </button>
          )}
        </div>

        {readonly && (
          <div
            className="glass"
            style={{
              padding: '12px 16px',
              marginBottom: 20,
              fontSize: '0.88rem',
              display: 'flex',
              alignItems: 'center',
              gap: 8,
            }}
          >
            <Lock size={16} /> {t('database.readOnly')}
          </div>
        )}

        <AnimatePresence>
          {adding && !readonly && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="panel"
              style={{ padding: 20, marginBottom: 20, overflow: 'hidden' }}
            >
              <h4 style={{ marginBottom: 14 }}>
                <Plus size={16} style={{ verticalAlign: 'middle', marginRight: 6 }} /> {t('database.addNew')}
              </h4>
              <div className="grid grid--2">
                <div className="field">
                  <label>{t('database.addName')}</label>
                  <input className="input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
                </div>
                <div className="field">
                  <label>{t('database.addType')}</label>
                  <input className="input" value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })} placeholder={tab === 'diseases' ? 'Fungal / Pest / Viral…' : 'Family…'} />
                </div>
              </div>
              <div className="field">
                <label>{t('database.addDetails')}</label>
                <textarea className="textarea" rows={3} value={form.details} onChange={(e) => setForm({ ...form, details: e.target.value })} />
              </div>
              <button type="button" className="btn btn-sm" onClick={save}>
                <Save size={16} /> {t('database.addToDb')}
              </button>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="panel" style={{ padding: 20 }}>
          <div className="field">
            <div style={{ position: 'relative' }}>
              <Search size={18} style={{ position: 'absolute', left: 14, top: 14, color: 'var(--green-400)' }} />
              <input
                className="input"
                style={{ paddingLeft: 42 }}
                placeholder={t('database.search')}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
          </div>

          <div style={{ fontSize: '0.85rem', marginBottom: 12 }} className="muted">
            <DatabaseIcon size={14} style={{ verticalAlign: 'middle', marginRight: 6 }} />
            {filtered.length} {t('database.rows')}
          </div>

          <div style={{ display: 'grid', gap: 10, maxHeight: 640, overflowY: 'auto' }}>
            {filtered.map((r) => {
              const id = r.id ?? r._id
              const isOpen = Boolean(expanded[id])
              const data = tab === 'diseases' ? rich(r) : null
              return (
                <motion.div
                  key={id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="glass"
                  style={{ padding: '14px 16px' }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'center' }}>
                    <div style={{ flex: 1 }}>
                      <strong>{r.name}</strong>
                      <div className="muted" style={{ fontSize: '0.82rem' }}>
                        {tab === 'diseases' ? r.category || r.type : r.family}
                        {tab === 'diseases' && r.severity ? ` · ${r.severity}` : ''}
                        {tab === 'plants' && r.sunlight ? ` · ${r.sunlight}` : ''}
                      </div>
                      {tab === 'diseases' && r.description && (
                        <p style={{ fontSize: '0.85rem', marginTop: 6 }}>{r.description}</p>
                      )}
                      {tab === 'plants' && r.care && (
                        <p style={{ fontSize: '0.85rem', marginTop: 6 }}>{r.care}</p>
                      )}
                    </div>
                    <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                      {tab === 'diseases' && data && (
                        <button
                          type="button"
                          className="btn btn-sm btn-ghost"
                          onClick={() => toggleExpanded(id)}
                          aria-label="Toggle details"
                        >
                          {isOpen ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
                        </button>
                      )}
                      {!readonly && (
                        <button type="button" className="btn btn-sm btn-danger" onClick={() => remove(id)} aria-label="Delete">
                          <Trash2 size={15} />
                        </button>
                      )}
                    </div>
                  </div>

                  {tab === 'diseases' && data && isOpen && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      className="mt-2"
                      style={{ overflow: 'hidden' }}
                    >
                      {data.chem.length > 0 && (
                        <p style={{ fontSize: '0.86rem', marginBottom: 6 }}>
                          <FlaskConical size={14} style={{ verticalAlign: 'middle', marginRight: 6, color: 'var(--green-500)' }} />
                          <strong>Chemical:</strong> {data.chem.map((c) => c.name).join(', ')}
                        </p>
                      )}
                      {data.bio.length > 0 && (
                        <p style={{ fontSize: '0.86rem', marginBottom: 6 }}>
                          <Bug size={14} style={{ verticalAlign: 'middle', marginRight: 6, color: 'var(--green-500)' }} />
                          <strong>Biological:</strong> {data.bio.map((b) => b.agent).join(', ')}
                        </p>
                      )}
                      {data.org.length > 0 && (
                        <p style={{ fontSize: '0.86rem', marginBottom: 6 }}>
                          <Leaf size={14} style={{ verticalAlign: 'middle', marginRight: 6, color: 'var(--green-500)' }} />
                          <strong>Organic:</strong> {data.org.map((o) => o.name).join(', ')}
                        </p>
                      )}
                      {data.fert.npk && (
                        <p style={{ fontSize: '0.86rem', marginBottom: 6 }}>
                          <Sprout size={14} style={{ verticalAlign: 'middle', marginRight: 6, color: 'var(--green-500)' }} />
                          <strong>NPK:</strong> {data.fert.npk}
                        </p>
                      )}
                      {data.tips.length > 0 && (
                        <p style={{ fontSize: '0.86rem', marginBottom: 6 }}>
                          <ShieldCheck size={14} style={{ verticalAlign: 'middle', marginRight: 6, color: 'var(--green-500)' }} />
                          <strong>Prevention:</strong> {data.tips.map((x) => x.title).join(' · ')}
                        </p>
                      )}
                      {data.emergency.length > 0 && (
                        <p style={{ fontSize: '0.86rem', marginBottom: 6 }}>
                          <Siren size={14} style={{ verticalAlign: 'middle', marginRight: 6, color: 'var(--green-500)' }} />
                          <strong>Emergency:</strong> {data.emergency.join(' · ')}
                        </p>
                      )}
                    </motion.div>
                  )}
                </motion.div>
              )
            })}
            {filtered.length === 0 && <p className="muted center mt-2">{t('database.empty')}</p>}
          </div>
        </div>
      </div>
    </div>
  )
}
