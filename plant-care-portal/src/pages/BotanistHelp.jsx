import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { motion } from 'framer-motion'
import { CalendarCheck, Star, Send, GraduationCap, MessageCircleQuestion } from 'lucide-react'
import PageHeader from '../components/ui/PageHeader.jsx'
import TiltCard from '../components/ui/TiltCard.jsx'
import { useApp } from '../context/AppContext.jsx'
import { haptic } from '../utils/haptics.js'
import { botanists, botanistReplies } from '../data/botanists.js'

export default function BotanistHelp() {
  const { t } = useTranslation()
  const { notify } = useApp()
  const [picked, setPicked] = useState(botanists[0])
  const [form, setForm] = useState({ name: '', email: '', botanist: botanists[0].id, date: '', message: '' })

  const submit = (e) => {
    e.preventDefault()
    if (!form.name || !form.email || !form.date || !form.message) {
      notify('Please fill every field', 'error')
      return
    }
    haptic('success')
    notify(t('botanist.booked'))
    setForm({ name: '', email: '', botanist: picked.id, date: '', message: '' })
  }

  return (
    <div className="page">
      <div className="container">
        <PageHeader title={t('botanist.title')} sub={t('botanist.sub')} emoji="🎓" />

        <div className="grid grid--2" style={{ alignItems: 'start' }}>
          {/* Panel */}
          <div>
            <div className="panel" style={{ padding: 24, marginBottom: 22 }}>
              <h3 style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 12 }}>
                <GraduationCap size={20} /> {t('botanist.introTitle')}
              </h3>
              <p className="muted">{t('botanist.intro')}</p>
            </div>

            <p style={{ fontWeight: 600, marginBottom: 12 }}>
              <CalendarCheck size={16} style={{ verticalAlign: 'middle', marginRight: 6 }} />
              {t('botanist.availability')}
            </p>
            <div className="grid grid--list">
              {botanists.map((b) => (
                <TiltCard
                  key={b.id}
                  className="glass"
                  maxTilt={12}
                  as="button"
                  style={{
                    textAlign: 'left',
                    padding: 16,
                    border: picked.id === b.id ? '2px solid var(--green-500)' : '1px solid var(--green-200)',
                    background: picked.id === b.id ? '#fff' : 'rgba(255,255,255,0.72)',
                    cursor: 'pointer',
                  }}
                  onClick={() => {
                    haptic('tap')
                    setPicked(b)
                    setForm((f) => ({ ...f, botanist: b.id }))
                  }}
                >
                  <div className="tilt-inner" style={{ display: 'block' }}>
                    <div className="tilt-pop" style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 8 }}>
                      <span style={{ fontSize: '1.8rem' }}>{b.emoji}</span>
                      <div>
                        <strong>{b.name}</strong>
                        <div className="muted" style={{ fontSize: '0.82rem' }}>{b.specialty}</div>
                      </div>
                    </div>
                    <div className="tilt-pop" style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                      <span className="chip">{b.experience}</span>
                      <span className="chip chip--cool">
                        <Star size={12} style={{ fill: 'currentColor' }} /> {b.rating}
                      </span>
                      <span className="chip">{b.available}</span>
                    </div>
                    {picked.id === b.id && (
                      <p className="muted mt-2 tilt-pop" style={{ fontSize: '0.85rem' }}>
                        💬 {botanistReplies[b.id]}
                      </p>
                    )}
                  </div>
                </TiltCard>
              ))}
            </div>
          </div>

          {/* Form */}
          <motion.form
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            className="panel"
            style={{ padding: 26 }}
            onSubmit={submit}
          >
            <h3 style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 18 }}>
              <MessageCircleQuestion size={20} /> {t('botanist.yourForm')}
            </h3>

            <div className="field">
              <label>{t('botanist.yourName')}</label>
              <input
                className="input"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
              />
            </div>
            <div className="field">
              <label>{t('botanist.yourEmail')}</label>
              <input
                className="input"
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />
            </div>
            <div className="field">
              <label>{t('botanist.botanistLabel')}</label>
              <select
                className="input"
                value={form.botanist}
                onChange={(e) => setForm({ ...form, botanist: Number(e.target.value) })}
              >
                {botanists.map((b) => (
                  <option key={b.id} value={b.id}>
                    {b.name} — {b.specialty}
                  </option>
                ))}
              </select>
            </div>
            <div className="field">
              <label>{t('botanist.date')}</label>
              <input
                className="input"
                type="date"
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
              />
            </div>
            <div className="field">
              <label>{t('botanist.message')}</label>
              <textarea
                className="textarea"
                rows={4}
                value={form.message}
                onChange={(e) => setForm({ ...form, message: e.target.value })}
              />
            </div>
            <button className="btn" style={{ width: '100%' }}>
              <Send size={18} /> {t('botanist.send')}
            </button>
          </motion.form>
        </div>
      </div>
    </div>
  )
}
