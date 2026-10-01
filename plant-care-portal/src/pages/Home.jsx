import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { motion } from 'framer-motion'
import {
  ScanSearch,
  Leaf,
  Bug,
  NotebookPen,
  GraduationCap,
  MessagesSquare,
  Wheat,
  Database as DatabaseIcon,
  ArrowRight,
  Camera,
  Stethoscope,
  Sprout,
} from 'lucide-react'
import TiltCard from '../components/ui/TiltCard.jsx'
import FeatureCard from '../components/ui/FeatureCard.jsx'
import { haptic } from '../utils/haptics.js'
import { ensureSeeded } from '../db/database.js'

const heroFeatureIcons = {
  detection: <ScanSearch size={26} />,
  identify: <Leaf size={26} />,
  problems: <Bug size={26} />,
  blogs: <NotebookPen size={26} />,
  botanist: <GraduationCap size={26} />,
  feed: <MessagesSquare size={26} />,
  community: <Wheat size={26} />,
  database: <DatabaseIcon size={26} />,
}

export default function Home() {
  const { t } = useTranslation()
  const [stats, setStats] = useState({ diseaseCount: 0, plantCount: 0 })

  useEffect(() => {
    ensureSeeded().then(({ diseaseCount, plantCount }) =>
      setStats({ diseaseCount, plantCount })
    )
  }, [])

  const features = [
    { to: '/detect', key: 'detection', emoji: '🔍', color: '#d7ebdb' },
    { to: '/identify', key: 'identify', emoji: '🌿', color: '#cde9cf' },
    { to: '/problems', key: 'problems', emoji: '🐛', color: '#f6e2c3' },
    { to: '/blogs', key: 'blogs', emoji: '📝', color: '#d9e8f5' },
    { to: '/botanist', key: 'botanist', emoji: '🎓', color: '#e3d9f2' },
    { to: '/feed', key: 'feed', emoji: '💬', color: '#f2dbe8' },
    { to: '/community', key: 'community', emoji: '🌾', color: '#f0e6b8' },
    { to: '/database', key: 'database', emoji: '🗄️', color: '#c9eef0' },
  ]

  const how = [
    { icon: Camera, title: t('home.how1'), desc: t('home.how1d') },
    { icon: Stethoscope, title: t('home.how2'), desc: t('home.how2d') },
    { icon: Sprout, title: t('home.how3'), desc: t('home.how3d') },
  ]

  return (
    <div className="page">
      <div className="container">
        {/* Hero */}
        <section className="grid grid--hero" style={{ padding: '40px 0 60px' }}>
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
          >
            <span className="chip mb-2">
              <Sprout size={14} />
              {t('hero.badge')}
            </span>
            <h1 style={{ fontSize: 'clamp(2.2rem, 5vw, 3.6rem)', marginBottom: 14 }}>
              {t('hero.title')}{' '}
              <span style={{ color: 'var(--green-500)' }}>{t('hero.titleAccent')}</span>
            </h1>
            <p style={{ fontSize: '1.1rem', maxWidth: 560, marginBottom: 26 }}>{t('hero.subtitle')}</p>
            <div style={{ display: 'flex', gap: 14, flexWrap: 'wrap' }}>
              <Link to="/detect" className="btn" onClick={() => haptic('press')}>
                <ScanSearch size={18} /> {t('hero.cta1')}
              </Link>
              <Link to="/identify" className="btn btn-ghost" onClick={() => haptic('tap')}>
                <Leaf size={18} /> {t('hero.cta2')}
              </Link>
            </div>

            <div className="grid grid--3" style={{ marginTop: 40 }}>
              <div className="glass stat-card">
                <strong>{stats.diseaseCount}+</strong>
                <span className="muted">{t('hero.stat1')}</span>
              </div>
              <div className="glass stat-card">
                <strong>{stats.plantCount}+</strong>
                <span className="muted">{t('hero.stat2')}</span>
              </div>
              <div className="glass stat-card">
                <strong>12k+</strong>
                <span className="muted">{t('hero.stat3')}</span>
              </div>
            </div>
          </motion.div>

          {/* 3D hero visual */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, delay: 0.15 }}
          >
            <TiltCard className="glass" maxTilt={16} scale={1.04}>
              <div className="tilt-inner" style={{ padding: 40, textAlign: 'center' }}>
                <div
                  className="tilt-pop"
                  style={{
                    width: 120,
                    height: 120,
                    margin: '0 auto 18px',
                    borderRadius: '50%',
                    display: 'grid',
                    placeItems: 'center',
                    fontSize: '3.4rem',
                    background: 'linear-gradient(135deg, var(--green-200), var(--green-400))',
                    boxShadow: '0 18px 40px var(--leaf-glow)',
                    animation: 'pulse-glow 3s ease-in-out infinite',
                  }}
                >
                  🍃
                </div>
                <h3 className="tilt-pop" style={{ marginBottom: 8 }}>Healthy. Detected.</h3>
                <p className="muted tilt-pop">
                  {t('home.featuresSub')}
                </p>
                <div
                  className="tilt-pop"
                  style={{
                    marginTop: 20,
                    display: 'flex',
                    justifyContent: 'center',
                    gap: 10,
                    flexWrap: 'wrap',
                  }}
                >
                  {Object.values(heroFeatureIcons).map((IconEl, i) => (
                    <span
                      key={i}
                      className="chip"
                      style={{ width: 44, height: 44, placeItems: 'center', fontSize: 20 }}
                    >
                      {IconEl}
                    </span>
                  ))}
                </div>
              </div>
            </TiltCard>
          </motion.div>
        </section>

        {/* Features */}
        <section className="mt-3" style={{ paddingTop: 20 }}>
          <h2 className="section-title">{t('home.features')}</h2>
          <p className="section-sub">{t('home.featuresSub')}</p>
          <div className="grid grid--features">
            {features.map((f) => (
              <FeatureCard
                key={f.to}
                to={f.to}
                emoji={f.emoji}
                color={f.color}
                title={t(`home.${f.key}`)}
                desc={t(`home.${f.key}Desc`)}
              />
            ))}
          </div>
        </section>

        {/* How it works */}
        <section className="mt-3" style={{ paddingTop: 50 }}>
          <h2 className="section-title">{t('home.howTitle')}</h2>
          <p className="section-sub">{t('home.howSub')}</p>
          <div className="timeline">
            {how.map((step, i) => (
              <div key={i} className="timeline-item tilt-wrap" style={{ display: 'flex', gap: 18, alignItems: 'flex-start' }}>
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.15 }}
                  className="panel tilt-card"
                  style={{ padding: 20, flex: 1, maxWidth: 480 }}
                  onMouseMove={(e) => {
                    const el = e.currentTarget
                    const r = el.getBoundingClientRect()
                    const ry = ((e.clientX - r.left) / r.width - 0.5) * 12
                    el.style.transform = `rotateY(${ry}deg)`
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'rotateY(0deg)'
                  }}
                >
                  <div className="tilt-inner" style={{ display: 'flex', gap: 14, alignItems: 'center' }}>
                    <span
                      style={{
                        width: 52,
                        height: 52,
                        borderRadius: 16,
                        display: 'grid',
                        placeItems: 'center',
                        background: 'var(--green-100)',
                        color: 'var(--green-700)',
                        fontSize: 26,
                      }}
                    >
                      <step.icon />
                    </span>
                    <div>
                      <h4>{step.title}</h4>
                      <p className="muted" style={{ fontSize: '0.92rem' }}>{step.desc}</p>
                    </div>
                  </div>
                </motion.div>
              </div>
            ))}
          </div>
        </section>

        {/* Quote */}
        <section className="center" style={{ padding: '60px 0 10px' }}>
          <blockquote
            style={{
              fontStyle: 'italic',
              fontSize: '1.25rem',
              maxWidth: 700,
              margin: '0 auto',
              color: 'var(--green-700)',
            }}
          >
            🌳 {t('home.quote')}
          </blockquote>
          <p className="muted mt-1">{t('home.quoteBy')}</p>
          <Link to="/detect" className="btn mt-3" onClick={() => haptic('press')}>
            {t('home.detection')} <ArrowRight size={18} />
          </Link>
        </section>
      </div>
    </div>
  )
}
