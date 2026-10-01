import { useEffect, useState } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { useTranslation } from 'react-i18next'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowLeft, MessageCircle, Eye, Plus, Send, Wheat } from 'lucide-react'
import PageHeader from '../components/ui/PageHeader.jsx'
import { useApp } from '../context/AppContext.jsx'
import { haptic } from '../utils/haptics.js'
import { db, ensureSeeded } from '../db/database.js'
import { threadReplies } from '../data/threadReplies.js'

export default function WeedCommunity() {
  const { t } = useTranslation()
  const { notify } = useApp()
  const [activeThread, setActiveThread] = useState(null)
  const [newThread, setNewThread] = useState(null)
  const [form, setForm] = useState({ title: '', body: '' })
  const [reply, setReply] = useState('')

  const threads =
    useLiveQuery(() => db.threads.orderBy('createdAt').reverse().toArray(), []) ?? []

  useEffect(() => {
    ensureSeeded()
  }, [])

  const openThread = async (thread) => {
    haptic('pop')
    setActiveThread(thread)
    await db.threads.update(thread.id, { views: thread.views + 1 })
  }

  const startThread = async () => {
    if (!form.title.trim() || !form.body.trim()) {
      notify('Add a title and body', 'error')
      return
    }
    haptic('success')
    const now = Date.now()
    await db.threads.add({ title: form.title, author: 'You', replies: 0, views: 0, createdAt: now })
    setNewThread(null)
    setForm({ title: '', body: '' })
    notify('Thread started!')
  }

  const submitReply = async () => {
    if (!reply.trim()) return
    haptic('tap')
    const authorKey = activeThread.author
    const existing = threadReplies[authorKey] ?? []
    if (!existing.includes(reply)) existing.push(reply)
    await db.threads.update(activeThread.id, {
      replies: activeThread.replies + 1,
    })
    setReply('')
    setActiveThread((a) => ({ ...a, replies: a.replies + 1, _newReply: reply }))
  }

  const back = () => {
    haptic('tap')
    setActiveThread(null)
    setNewThread(null)
  }

  const timeAgo = (ts) => {
    const mins = Math.max(1, Math.round((Date.now() - ts) / 60000))
    if (mins < 60) return `${mins}m`
    const hrs = Math.round(mins / 60)
    if (hrs < 24) return `${hrs}h`
    return `${Math.round(hrs / 24)}d`
  }

  return (
    <div className="page">
      <div className="container" style={{ maxWidth: 880 }}>
        <PageHeader title={t('community.title')} sub={t('community.sub')} emoji="🌾" />

        <AnimatePresence mode="wait">
          {activeThread ? (
            <motion.article
              key="thread"
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="panel"
              style={{ padding: 26 }}
            >
              <button type="button" className="btn btn-ghost btn-sm mb-2" onClick={back}>
                <ArrowLeft size={16} /> {t('community.backToForums')}
              </button>
              <h2>{activeThread.title}</h2>
              <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', margin: '10px 0 18px' }}>
                <span className="chip"><Wheat size={14} /> {activeThread.author}</span>
                <span className="chip"><MessageCircle size={14} /> {activeThread.replies} {t('community.replies')}</span>
                <span className="chip"><Eye size={14} /> {activeThread.views} {t('community.views')}</span>
              </div>

              <p className="muted" style={{ lineHeight: 1.7, marginBottom: 20 }}>
                {form.body && activeThread.author === 'You' ? form.body : threadReplies[activeThread.author]?.[0] ?? 'Share your experience and tips below!'}
              </p>

              <h4 style={{ marginBottom: 12 }}>{t('community.repliesTitle')}</h4>
              <div style={{ display: 'grid', gap: 10 }}>
                {(threadReplies[activeThread.author] ?? []).map((r, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -14 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.05 }}
                    className="glass"
                    style={{ padding: '12px 16px' }}
                  >
                    <strong style={{ fontSize: '0.85rem', color: 'var(--green-600)' }}>
                      @gardener_{i + 1}
                    </strong>
                    <p style={{ fontSize: '0.95rem' }}>{r}</p>
                  </motion.div>
                ))}
                {activeThread._newReply && (
                  <div className="glass" style={{ padding: '12px 16px', borderColor: 'var(--green-400)' }}>
                    <strong style={{ fontSize: '0.85rem', color: 'var(--green-600)' }}>@you</strong>
                    <p style={{ fontSize: '0.95rem' }}>{activeThread._newReply}</p>
                  </div>
                )}
              </div>

              <div className="mt-2" style={{ display: 'flex', gap: 8 }}>
                <input
                  className="input"
                  style={{ flex: 1 }}
                  placeholder={t('community.replyPlaceholder')}
                  value={reply}
                  onChange={(e) => setReply(e.target.value)}
                />
                <button type="button" className="btn btn-sm" onClick={submitReply}>
                  <Send size={15} /> {t('community.reply')}
                </button>
              </div>
            </motion.article>
          ) : newThread ? (
            <motion.div
              key="new"
              initial={{ opacity: 0, y: 24 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="panel"
              style={{ padding: 26 }}
            >
              <button type="button" className="btn btn-ghost btn-sm mb-2" onClick={back}>
                <ArrowLeft size={16} /> {t('community.backToForums')}
              </button>
              <h2 style={{ marginBottom: 16 }}>{t('community.newTopic')}</h2>
              <div className="field">
                <label>{t('community.startTitle')}</label>
                <input className="input" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
              </div>
              <div className="field">
                <label>{t('community.startBody')}</label>
                <textarea className="textarea" rows={5} value={form.body} onChange={(e) => setForm({ ...form, body: e.target.value })} />
              </div>
              <button type="button" className="btn" onClick={startThread}>
                <Plus size={18} /> {t('community.startPost')}
              </button>
            </motion.div>
          ) : (
            <motion.div key="list" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 18 }}>
                <button type="button" className="btn" onClick={() => { haptic('tap'); setNewThread(true) }}>
                  <Plus size={18} /> {t('community.newTopic')}
                </button>
              </div>
              <div style={{ display: 'grid', gap: 12 }}>
                {threads.map((th, idx) => (
                  <motion.button
                    key={th.id}
                    initial={{ opacity: 0, y: 16 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.04 }}
                    className="panel"
                    style={{
                      textAlign: 'left',
                      padding: 18,
                      cursor: 'pointer',
                      display: 'block',
                      width: '100%',
                      color: 'var(--green-900)',
                      fontFamily: 'inherit',
                    }}
                    onClick={() => openThread(th)}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'center' }}>
                      <div>
                        <h3 style={{ fontSize: '1.05rem' }}>{th.title}</h3>
                        <span className="chip mt-1"><Wheat size={13} /> {th.author}</span>
                        <span className="muted" style={{ fontSize: '0.78rem', marginLeft: 8 }}>{timeAgo(th.createdAt)}</span>
                      </div>
                      <div style={{ textAlign: 'right', flexShrink: 0 }}>
                        <div className="chip"><MessageCircle size={13} /> {th.replies} {t('community.replies')}</div>
                        <div className="chip chip--cool" style={{ marginTop: 6 }}><Eye size={13} /> {th.views} {t('community.views')}</div>
                      </div>
                    </div>
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
