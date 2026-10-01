import { useMemo, useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Bug,
  Filter,
  AlertTriangle,
  Stethoscope,
  ChevronDown,
  ChevronUp,
  FlaskConical,
  Leaf,
  ShieldCheck,
  Sprout,
  CloudRain,
} from 'lucide-react'
import PageHeader from '../components/ui/PageHeader.jsx'
import TiltCard from '../components/ui/TiltCard.jsx'
import { haptic } from '../utils/haptics.js'
import { problems } from '../data/problems.js'
import { api } from '../api/client.js'

const CATEGORIES = ['All', 'Pest', 'Fungal', 'Deficiency', 'Viral']

const norm = (s = '') => s.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()

export default function AllProblems() {
  const { t } = useTranslation()
  const [cat, setCat] = useState('All')
  const [enriched, setEnriched] = useState({}) // name -> rich record
  const [expanded, setExpanded] = useState({})

  useEffect(() => {
    let active = true
    ;(async () => {
      try {
        const data = await api.listDiseases({ page_size: 100 })
        if (!active) return
        const map = {}
        for (const d of data.items || []) map[norm(d.name)] = d
        setEnriched(map)
      } catch {
        /* offline — fall back to static data only */
      }
    })()
    return () => {
      active = false
    }
  }, [])

  const filtered = useMemo(
    () => (cat === 'All' ? problems : problems.filter((p) => p.category === cat)),
    [cat]
  )

  const setCategory = (c) => {
    haptic('tap')
    setCat(c)
  }

  const toggle = (id) => {
    haptic('tap')
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }))
  }

  return (
    <div className="page">
      <div className="container">
        <PageHeader title={t('problems.title')} sub={t('problems.sub')} emoji="🐛" />

        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 28 }}>
          <Filter size={20} style={{ color: 'var(--green-500)', alignSelf: 'center' }} />
          {CATEGORIES.map((c) => (
            <button
              type="button"
              key={c}
              className={`chip ${cat === c ? 'chip--cool' : ''}`}
              style={{
                background: cat === c ? 'var(--green-600)' : 'var(--green-100)',
                color: cat === c ? '#fff' : 'var(--green-700)',
                border: 'none',
                padding: '10px 18px',
              }}
              onClick={() => setCategory(c)}
            >
              {t(`problems.filter${c}`)}
            </button>
          ))}
        </div>

        <motion.div layout className="grid grid--list">
          <AnimatePresence mode="popLayout">
            {filtered.map((p) => {
              const rich = enriched[norm(p.name)]
              const isOpen = Boolean(expanded[p.id])
              return (
                <motion.div
                  layout
                  key={p.id}
                  initial={{ opacity: 0, scale: 0.92 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                >
                  <TiltCard className="panel" maxTilt={12} style={{ height: '100%' }}>
                    <div className="tilt-inner" style={{ padding: 22, display: 'block' }}>
                      <div className="tilt-pop" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                        <span style={{ fontSize: '2rem' }}>{p.emoji}</span>
                        <span className="chip" style={{ background: p.category === 'Pest' ? '#fde8d8' : p.category === 'Fungal' ? '#e2f0e3' : p.category === 'Deficiency' ? '#e4effa' : '#f3dcdc', color: '#5a4030', borderColor: 'transparent' }}>
                          {t(`problems.filter${p.category}`)}
                        </span>
                      </div>
                      <h3 className="tilt-pop" style={{ marginBottom: 4 }}>{p.name}</h3>
                      <p className="tilt-pop" style={{ fontSize: '0.8rem', marginBottom: 12 }}>
                        <AlertTriangle size={13} style={{ verticalAlign: 'middle', marginRight: 4 }} />
                        {t('problems.severity')}: <strong>{p.severity}</strong> · {t('problems.plantTitle')}: {p.affects}
                      </p>
                      <p className="muted tilt-pop" style={{ fontSize: '0.9rem', marginBottom: 8 }}>
                        <Bug size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} />
                        <strong>{t('problems.symptomTitle')}:</strong> {p.symptoms}
                      </p>
                      <p className="muted tilt-pop" style={{ fontSize: '0.9rem', marginBottom: 12 }}>
                        <Stethoscope size={14} style={{ verticalAlign: 'middle', marginRight: 4 }} />
                        <strong>{t('problems.fixTitle')}:</strong> {p.remedy}
                      </p>

                      {rich ? (
                        <>
                          <button type="button" className="btn btn-sm btn-ghost" style={{ width: '100%' }} onClick={() => toggle(p.id)}>
                            {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                            {isOpen ? t('problems.hidePlan') : t('problems.showPlan')}
                          </button>

                          {isOpen && (
                            <motion.div
                              initial={{ opacity: 0, height: 0 }}
                              animate={{ opacity: 1, height: 'auto' }}
                              exit={{ opacity: 0, height: 0 }}
                              style={{ overflow: 'hidden' }}
                              className="mt-2"
                            >
                              {rich.description && (
                                <p className="report-text" style={{ fontSize: '0.85rem' }}>{rich.description}</p>
                              )}

                              {(rich.chemical_treatment || []).length > 0 && (
                                <>
                                  <h4 style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.9rem', marginBottom: 6 }}>
                                    <FlaskConical size={14} style={{ color: 'var(--green-500)' }} />
                                    {t('problems.chemical')}
                                  </h4>
                                  <div className="pill-row" style={{ marginBottom: 10 }}>
                                    {rich.chemical_treatment.map((c, i) => (
                                      <span className="pill" key={i}>{c.name}</span>
                                    ))}
                                  </div>
                                </>
                              )}

                              {(rich.biological_treatment || []).length > 0 && (
                                <>
                                  <h4 style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.9rem', marginBottom: 6 }}>
                                    <Bug size={14} style={{ color: 'var(--green-500)' }} />
                                    {t('problems.biological')}
                                  </h4>
                                  <div className="pill-row pill--cool" style={{ marginBottom: 10 }}>
                                    {rich.biological_treatment.map((b, i) => (
                                      <span className="pill pill--cool" key={i}>{b.agent}</span>
                                    ))}
                                  </div>
                                </>
                              )}

                              {(rich.organic_remedies || []).length > 0 && (
                                <>
                                  <h4 style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.9rem', marginBottom: 6 }}>
                                    <Leaf size={14} style={{ color: 'var(--green-500)' }} />
                                    {t('problems.organic')}
                                  </h4>
                                  <div className="pill-row" style={{ marginBottom: 10 }}>
                                    {rich.organic_remedies.map((o, i) => (
                                      <span className="pill" key={i}>{o.name}</span>
                                    ))}
                                  </div>
                                </>
                              )}

                              {rich.fertilizer && (rich.fertilizer.npk || rich.fertilizer.type) && (
                                <p className="report-text" style={{ fontSize: '0.85rem', marginBottom: 8 }}>
                                  <Sprout size={14} style={{ verticalAlign: 'middle', marginRight: 6, color: 'var(--green-500)' }} />
                                  <strong>{t('problems.fertilizer')}:</strong>{' '}
                                  {[rich.fertilizer.npk, rich.fertilizer.type, rich.fertilizer.organic].filter(Boolean).join(' · ')}
                                </p>
                              )}

                              {(rich.prevention_tips || []).length > 0 && (
                                <p className="report-text" style={{ fontSize: '0.85rem', marginBottom: 8 }}>
                                  <ShieldCheck size={14} style={{ verticalAlign: 'middle', marginRight: 6, color: 'var(--green-500)' }} />
                                  <strong>{t('problems.prevention')}:</strong>{' '}
                                  {rich.prevention_tips.map((x) => x.title).join(' · ')}
                                </p>
                              )}

                              {rich.severity_levels && rich.severity_levels.severe && (
                                <div className={`severity-box sev-severe`} style={{ marginBottom: 8 }}>
                                  <h4 style={{ fontSize: '0.85rem' }}>⚠ {t('problems.severity')}: Severe</h4>
                                  <p style={{ fontSize: '0.82rem' }}>{rich.severity_levels.severe}</p>
                                </div>
                              )}

                              {rich.weather_conditions && (rich.weather_conditions.humidity || rich.weather_conditions.temperature || rich.weather_conditions.rainfall) && (
                                <p className="report-text" style={{ fontSize: '0.85rem', marginBottom: 8 }}>
                                  <CloudRain size={14} style={{ verticalAlign: 'middle', marginRight: 6, color: 'var(--green-500)' }} />
                                  <strong>{t('problems.weather')}:</strong>{' '}
                                  {[
                                    rich.weather_conditions.humidity,
                                    rich.weather_conditions.temperature,
                                    rich.weather_conditions.rainfall,
                                  ].filter(Boolean).join(' · ')}
                                </p>
                              )}

                              {(rich.emergency_actions || []).length > 0 && (
                                <ul className="emergency-list" style={{ marginTop: 8 }}>
                                  {rich.emergency_actions.map((a, i) => (
                                    <li key={i}>{a}</li>
                                  ))}
                                </ul>
                              )}
                            </motion.div>
                          )}
                        </>
                      ) : null}
                    </div>
                  </TiltCard>
                </motion.div>
              )
            })}
          </AnimatePresence>
        </motion.div>
      </div>
    </div>
  )
}
