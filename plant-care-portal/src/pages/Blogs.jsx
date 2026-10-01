import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowLeft, Clock, User, BookOpen } from 'lucide-react'
import PageHeader from '../components/ui/PageHeader.jsx'
import TiltCard from '../components/ui/TiltCard.jsx'
import { haptic } from '../utils/haptics.js'
import { blogs } from '../data/blogs.js'

export default function Blogs() {
  const { t } = useTranslation()
  const [active, setActive] = useState(null)

  const open = (blog) => {
    haptic('pop')
    setActive(blog)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const close = () => {
    haptic('tap')
    setActive(null)
  }

  return (
    <div className="page">
      <div className="container">
        <PageHeader title={t('blogs.title')} sub={t('blogs.sub')} emoji="📝" />

        <AnimatePresence mode="wait">
          {active ? (
            <motion.article
              key={active.id}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="panel"
              style={{ padding: '34px 30px', maxWidth: 860, margin: '0 auto' }}
            >
              <button type="button" className="btn btn-ghost btn-sm mb-2" onClick={close}>
                <ArrowLeft size={16} /> {t('blogs.back')}
              </button>
              <div style={{ fontSize: '3rem', marginBottom: 12 }}>{active.emoji}</div>
              <h1 style={{ marginBottom: 10 }}>{active.title}</h1>
              <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap', marginBottom: 20 }}>
                <span className="chip"><User size={14} /> {active.author}</span>
                <span className="chip"><Clock size={14} /> {active.date}</span>
                <span className="chip"><BookOpen size={14} /> {active.readMins} {t('blogs.mins')}</span>
                {active.tags.map((tag) => (
                  <span key={tag} className="chip chip--cool">{tag}</span>
                ))}
              </div>
              {active.content.map((para, i) => (
                <p key={i} style={{ marginBottom: 14, lineHeight: 1.75, color: 'var(--green-800)' }}>
                  {para}
                </p>
              ))}
            </motion.article>
          ) : (
            <motion.div key="list" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="grid grid--list">
              {blogs.map((blog) => (
                <TiltCard key={blog.id} className="panel" maxTilt={12}>
                  <div className="tilt-inner" style={{ padding: 22, display: 'block', height: '100%' }}>
                    <div className="tilt-pop" style={{ fontSize: '2.2rem', marginBottom: 10 }}>{blog.emoji}</div>
                    <h3 className="tilt-pop" style={{ marginBottom: 8, fontSize: '1.1rem' }}>{blog.title}</h3>
                    <p className="muted tilt-pop" style={{ fontSize: '0.92rem', marginBottom: 14 }}>{blog.excerpt}</p>
                    <div className="tilt-pop" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'auto' }}>
                      <span className="chip"><User size={13} /> {blog.author}</span>
                      <span className="chip"><Clock size={13} /> {blog.readMins} {t('blogs.mins')}</span>
                    </div>
                    <button type="button" className="btn btn-sm mt-2 tilt-pop" style={{ width: '100%' }} onClick={() => open(blog)}>
                      {t('blogs.read')} <BookOpen size={15} />
                    </button>
                  </div>
                </TiltCard>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
