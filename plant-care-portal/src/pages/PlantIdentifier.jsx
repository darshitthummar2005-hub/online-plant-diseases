import { useEffect, useMemo, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Sun, Droplets, Sprout, Sparkles, Users } from 'lucide-react'
import PageHeader from '../components/ui/PageHeader.jsx'
import TiltCard from '../components/ui/TiltCard.jsx'
import { haptic } from '../utils/haptics.js'
import { db } from '../db/database.js'

export default function PlantIdentifier() {
  const { t } = useTranslation()
  const [plants, setPlants] = useState([])
  const [query, setQuery] = useState('')
  const [selectedId, setSelectedId] = useState(null)

  useEffect(() => {
    db.plants.orderBy('name').toArray().then(setPlants)
  }, [])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return plants
    return plants.filter((p) =>
      `${p.name} ${p.family} ${p.sunlight} ${p.water} ${p.care}`.toLowerCase().includes(q)
    )
  }, [plants, query])

  const selected = plants.find((p) => p.id === selectedId)

  const pick = (p) => {
    haptic('pop')
    setSelectedId(p.id)
  }

  return (
    <div className="page">
      <div className="container">
        <PageHeader title={t('identify.title')} sub={t('identify.sub')} emoji="🌿" />

        <div className="grid grid--2" style={{ alignItems: 'start' }}>
          {/* List */}
          <div className="panel" style={{ padding: 22 }}>
            <div className="field">
              <label>{t('identify.name')}</label>
              <div style={{ position: 'relative' }}>
                <Search
                  size={18}
                  style={{ position: 'absolute', left: 14, top: 14, color: 'var(--green-400)' }}
                />
                <input
                  className="input"
                  style={{ paddingLeft: 42 }}
                  placeholder={t('identify.placeholders')}
                  value={query}
                  onChange={(e) => {
                    haptic('tap')
                    setQuery(e.target.value)
                  }}
                />
              </div>
            </div>
            <div style={{ maxHeight: 480, overflowY: 'auto', display: 'grid', gap: 10 }}>
              {filtered.map((p) => (
                <button
                  type="button"
                  key={p.id}
                  className="chip"
                  style={{
                    justifyContent: 'space-between',
                    padding: '12px 16px',
                    fontSize: '0.95rem',
                    textAlign: 'left',
                    background: selectedId === p.id ? 'var(--green-600)' : '#fff',
                    color: selectedId === p.id ? '#fff' : 'var(--green-800)',
                    border: selectedId === p.id ? 'none' : '2px solid var(--green-200)',
                    cursor: 'pointer',
                    borderRadius: 14,
                    display: 'flex',
                  }}
                  onClick={() => pick(p)}
                >
                  <span>{p.name}</span>
                  <span className="muted" style={{ color: selectedId === p.id ? '#c3e0c9' : undefined }}>
                    {p.family}
                  </span>
                </button>
              ))}
              {filtered.length === 0 && <p className="muted center mt-2">{t('identify.noResults')}</p>}
            </div>
          </div>

          {/* Detail */}
          <AnimatePresence mode="wait">
            {selected ? (
              <motion.div
                key={selected.id}
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <TiltCard className="panel" maxTilt={10}>
                  <div className="tilt-inner" style={{ padding: 28 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 18 }}>
                      <span
                        className="tilt-pop"
                        style={{
                          width: 72,
                          height: 72,
                          borderRadius: 20,
                          display: 'grid',
                          placeItems: 'center',
                          fontSize: '2.4rem',
                          background: 'linear-gradient(135deg, var(--green-100), var(--green-300))',
                        }}
                      >
                        🌱
                      </span>
                      <div>
                        <h2 className="tilt-pop">{selected.name}</h2>
                        <span className="chip">{t('identify.plantFamily')}: {selected.family}</span>
                      </div>
                    </div>

                    <div className="grid grid--3">
                      <div className="glass tilt-pop" style={{ padding: 14, textAlign: 'center' }}>
                        <Sun size={20} style={{ margin: '0 auto 6px', color: '#d99a2b' }} />
                        <small className="muted">{t('identify.sunlight')}</small>
                        <div style={{ fontWeight: 600 }}>{selected.sunlight}</div>
                      </div>
                      <div className="glass tilt-pop" style={{ padding: 14, textAlign: 'center' }}>
                        <Droplets size={20} style={{ margin: '0 auto 6px', color: '#2b6f9d' }} />
                        <small className="muted">{t('identify.water')}</small>
                        <div style={{ fontWeight: 600 }}>{selected.water}</div>
                      </div>
                      <div className="glass tilt-pop" style={{ padding: 14, textAlign: 'center' }}>
                        <Sprout size={20} style={{ margin: '0 auto 6px', color: 'var(--green-500)' }} />
                        <small className="muted">{t('identify.plantFamily')}</small>
                        <div style={{ fontWeight: 600 }}>{selected.family}</div>
                      </div>
                    </div>

                    <h4 className="mt-3 tilt-pop" style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                      <Sprout size={18} /> {t('identify.careTitle')}
                    </h4>
                    <p className="muted tilt-pop">{selected.care}</p>

                    <h4 className="mt-2 tilt-pop" style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                      <Sparkles size={18} /> {t('identify.funFacts')}
                    </h4>
                    <p className="muted tilt-pop">{selected.facts}</p>
                  </div>
                </TiltCard>
              </motion.div>
            ) : (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="glass"
                style={{ padding: 40, textAlign: 'center' }}
              >
                <Users size={40} style={{ color: 'var(--green-300)', margin: '0 auto 12px' }} />
                <p className="muted">{t('identify.search')}</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}
