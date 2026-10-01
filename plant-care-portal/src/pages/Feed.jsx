import { useEffect, useState } from 'react'
import { useLiveQuery } from 'dexie-react-hooks'
import { useTranslation } from 'react-i18next'
import { motion, AnimatePresence } from 'framer-motion'
import { Heart, MessageSquare, Send, Leaf, UserCircle2 } from 'lucide-react'
import PageHeader from '../components/ui/PageHeader.jsx'
import { useApp } from '../context/AppContext.jsx'
import { haptic } from '../utils/haptics.js'
import { db, ensureSeeded } from '../db/database.js'

const AVATAR_COLORS = ['#4a7c59', '#2b6f9d', '#b4603a', '#7a4a9d', '#d99a2b']

export default function Feed() {
  const { t } = useTranslation()
  const { notify } = useApp()
  const [draft, setDraft] = useState('')
  const [commentDrafts, setCommentDrafts] = useState({})

  const posts = useLiveQuery(() => db.posts.orderBy('createdAt').reverse().toArray(), []) ?? []

  useEffect(() => {
    ensureSeeded()
  }, [])

  const post = async () => {
    const text = draft.trim()
    if (!text) {
      notify('Write something first', 'error')
      return
    }
    haptic('success')
    await db.posts.add({
      author: 'You',
      text,
      likes: 0,
      createdAt: Date.now(),
      comments: [],
    })
    setDraft('')
    notify('Posted to the feed')
  }

  const like = async (post) => {
    haptic('pop')
    await db.posts.update(post.id, { likes: post.likes + 1 })
  }

  const comment = async (post) => {
    const text = (commentDrafts[post.id] ?? '').trim()
    if (!text) return
    haptic('tap')
    const comments = [...(post.comments ?? []), { author: 'You', text, createdAt: Date.now() }]
    await db.posts.update(post.id, { comments })
    setCommentDrafts({ ...commentDrafts, [post.id]: '' })
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
      <div className="container" style={{ maxWidth: 760 }}>
        <PageHeader title={t('feed.title')} sub={t('feed.sub')} emoji="💬" />

        {/* Composer */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="panel"
          style={{ padding: 20, marginBottom: 24 }}
        >
          <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
            <span
              style={{
                width: 44,
                height: 44,
                borderRadius: '50%',
                background: 'linear-gradient(135deg, var(--green-400), var(--green-700))',
                color: '#fff',
                display: 'grid',
                placeItems: 'center',
                flexShrink: 0,
              }}
            >
              <UserCircle2 size={26} />
            </span>
            <div style={{ flex: 1 }}>
              <textarea
                className="textarea"
                rows={2}
                placeholder={t('feed.postPlaceholder')}
                value={draft}
                onChange={(e) => setDraft(e.target.value)}
              />
              <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 10 }}>
                <button type="button" className="btn btn-sm" onClick={post}>
                  <Send size={15} /> {t('feed.post')}
                </button>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Posts */}
        <div style={{ display: 'grid', gap: 18 }}>
          <AnimatePresence>
            {posts.map((p, idx) => (
              <motion.article
                key={p.id}
                layout
                initial={{ opacity: 0, y: 24 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="panel"
                style={{ padding: 20 }}
              >
                <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 12 }}>
                  <span
                    style={{
                      width: 42,
                      height: 42,
                      borderRadius: '50%',
                      background: AVATAR_COLORS[idx % AVATAR_COLORS.length],
                      color: '#fff',
                      display: 'grid',
                      placeItems: 'center',
                      fontWeight: 700,
                      flexShrink: 0,
                    }}
                  >
                    {p.author.charAt(0)}
                  </span>
                  <div>
                    <strong>{p.author}</strong>
                    <div className="muted" style={{ fontSize: '0.78rem' }}>{timeAgo(p.createdAt)}</div>
                  </div>
                </div>

                <p style={{ lineHeight: 1.6, marginBottom: 14 }}>{p.text}</p>

                <div style={{ display: 'flex', gap: 8 }}>
                  <button type="button" className="chip" style={{ border: 'none' }} onClick={() => like(p)}>
                    <Heart size={15} style={{ color: '#c04f4f' }} /> {p.likes} {t('feed.likes')}
                  </button>
                  <span className="chip">
                    <MessageSquare size={15} /> {(p.comments ?? []).length} {t('feed.comments')}
                  </span>
                </div>

                <div className="mt-2" style={{ borderTop: '1px solid var(--green-100)', paddingTop: 12 }}>
                  <div style={{ display: 'flex', gap: 8, marginBottom: 10 }}>
                    <input
                      className="input"
                      style={{ flex: 1, padding: '9px 14px', fontSize: '0.9rem' }}
                      placeholder={t('feed.typeComment')}
                      value={commentDrafts[p.id] ?? ''}
                      onChange={(e) =>
                        setCommentDrafts({ ...commentDrafts, [p.id]: e.target.value })
                      }
                    />
                    <button type="button" className="btn btn-sm" onClick={() => comment(p)}>
                      <Send size={14} />
                    </button>
                  </div>
                  {(p.comments ?? []).length > 0 && (
                    <div style={{ display: 'grid', gap: 8 }}>
                      <p style={{ fontWeight: 600, fontSize: '0.85rem' }}>{t('feed.commentsTitle')}</p>
                      {p.comments.map((c, i) => (
                        <div key={i} className="glass" style={{ padding: '8px 12px', fontSize: '0.9rem' }}>
                          <strong>{c.author}:</strong> {c.text}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </motion.article>
            ))}
          </AnimatePresence>
          {posts.length === 0 && (
            <div className="glass" style={{ padding: 30, textAlign: 'center' }}>
              <Leaf size={34} style={{ color: 'var(--green-300)', margin: '0 auto 10px' }} />
              <p className="muted">{t('misc.loading')}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
