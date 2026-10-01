import { useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { motion, AnimatePresence } from 'framer-motion'
import {
  UploadCloud,
  ScanSearch,
  RotateCcw,
  Image as ImageIcon,
  Link2,
  AlertCircle,
  Cloud,
  WifiOff,
  X,
} from 'lucide-react'
import PageHeader from '../components/ui/PageHeader.jsx'
import DoctorReport from '../components/detect/DoctorReport.jsx'
import { useApp } from '../context/AppContext.jsx'
import { haptic } from '../utils/haptics.js'
import { api, fileToDataUrl, localDetect } from '../api/client.js'

const SYMPTOM_OPTIONS = [
  'white', 'powder', 'brown', 'spots', 'yellow', 'wilting', 'curled',
  'sticky', 'webbing', 'mushy', 'stunted', 'holes', 'rust', 'blight',
]

export default function DiseaseDetection() {
  const { t } = useTranslation()
  const { notify } = useApp()
  const inputRef = useRef(null)
  const [drag, setDrag] = useState(false)
  const [image, setImage] = useState(null)
  const [imageKind, setImageKind] = useState('file')
  const [imageError, setImageError] = useState(false)
  const [urlInput, setUrlInput] = useState('')
  const [selected, setSelected] = useState([])
  const [result, setResult] = useState(null)
  const [running, setRunning] = useState(false)
  const [source, setSource] = useState(null) // 'api' | 'local'

  const onFiles = async (files) => {
    const file = files?.[0]
    if (!file || !file.type.startsWith('image/')) return
    haptic('pop')
    setImageError(false)
    try {
      const dataUrl = await fileToDataUrl(file)
      setImage(dataUrl)
      setImageKind('file')
    } catch (err) {
      notify(err.message || t('detect.imageError'), 'error')
    }
  }

  const toggleSymptom = (s) => {
    haptic('tap')
    setSelected((prev) =>
      prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s]
    )
  }

  const loadUrl = () => {
    const url = urlInput.trim()
    if (!/^https?:\/\/.+/.test(url)) {
      haptic('error')
      notify(t('detect.linkInvalid'), 'error')
      return
    }
    haptic('pop')
    setImage(url)
    setImageKind('url')
    setImageError(false)
    notify(t('detect.linkLoaded'))
  }

  const runDetection = async () => {
    haptic('press')
    if (!image && selected.length === 0) {
      notify(t('detect.emptyInput'), 'error')
      return
    }
    setRunning(true)
    setResult(null)
    setSource(null)

    let report = null
    try {
      report = await api.runDetection({
        symptoms: selected,
        image_present: Boolean(image),
        image_data: imageKind === 'file' ? image : undefined,
        image_url: imageKind === 'url' ? image : undefined,
      })
      setSource('api')
    } catch (err) {
      console.warn('Backend detection failed, using offline fallback:', err)
      report = await localDetect(selected, Boolean(image))
      setSource('local')
    }

    await new Promise((r) => setTimeout(r, 350))
    setResult(report)
    setRunning(false)
    if (report?.disease_name) {
      notify(`${t('detect.result')} · ${report.disease_name}`)
    }
  }

  const reset = () => {
    haptic('tap')
    setImage(null)
    setImageKind('file')
    setImageError(false)
    setUrlInput('')
    setSelected([])
    setResult(null)
    setSource(null)
    if (inputRef.current) inputRef.current.value = ''
  }

  return (
    <div className="page">
      <div className="container">
        <PageHeader title={t('detect.title')} sub={t('detect.sub')} emoji="🔍" />

        <div className="grid grid--2" style={{ alignItems: 'start' }}>
          {/* ===== Input panel ===== */}
          <div className="panel" style={{ padding: 26 }}>
            <input
              ref={inputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={(e) => onFiles(e.target.files)}
            />
            <div
              className={`drop-zone ${drag ? 'drag' : ''}`}
              onClick={() => {
                haptic('tap')
                inputRef.current?.click()
              }}
              onDragOver={(e) => {
                e.preventDefault()
                setDrag(true)
              }}
              onDragLeave={() => setDrag(false)}
              onDrop={(e) => {
                e.preventDefault()
                setDrag(false)
                onFiles(e.dataTransfer.files)
              }}
            >
              {image ? (
                <div className="preview-wrap">
                  <img
                    src={image}
                    alt="preview"
                    referrerPolicy="no-referrer"
                    onError={() => {
                      if (imageKind === 'url') setImageError(true)
                    }}
                    className="preview-img"
                  />
                  <button
                    type="button"
                    className="preview-clear"
                    aria-label="Remove image"
                    onClick={(e) => {
                      e.stopPropagation()
                      haptic('pop')
                      setImage(null)
                      setImageError(false)
                      if (inputRef.current) inputRef.current.value = ''
                    }}
                  >
                    <X size={16} />
                  </button>
                  {imageError && (
                    <span className="preview-error">
                      <AlertCircle size={14} /> {t('detect.imageError')}
                    </span>
                  )}
                </div>
              ) : (
                <>
                  <UploadCloud size={44} style={{ color: 'var(--green-500)', margin: '0 auto 12px' }} />
                  <p>
                    <strong>{t('detect.upload')}</strong>
                  </p>
                  <span className="btn btn-sm btn-ghost mt-2">
                    <ImageIcon size={16} /> {t('detect.chooseImage')}
                  </span>
                </>
              )}
            </div>

            <p className="mt-3 center muted" style={{ fontWeight: 600 }}>
              {t('detect.orLink')}
            </p>

            <div className="mt-2" style={{ display: 'flex', gap: 8 }}>
              <input
                type="url"
                className="input"
                style={{ flex: 1 }}
                placeholder={t('detect.linkPlaceholder')}
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') loadUrl()
                }}
              />
              <button type="button" className="btn btn-ghost" onClick={loadUrl}>
                <Link2 size={16} /> {t('detect.linkLoad')}
              </button>
            </div>

            <p className="mt-3 center muted" style={{ fontWeight: 600 }}>
              {t('detect.or')}
            </p>

            <div className="mt-2">
              <p className="field label" style={{ marginBottom: 10 }}>
                {t('detect.symptoms')}
              </p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                {SYMPTOM_OPTIONS.map((s) => (
                  <button
                    type="button"
                    key={s}
                    className={`chip ${selected.includes(s) ? 'chip--cool' : ''}`}
                    style={{
                      background: selected.includes(s) ? 'var(--green-600)' : 'var(--green-100)',
                      color: selected.includes(s) ? '#fff' : 'var(--green-700)',
                      border: 'none',
                      padding: '8px 16px',
                    }}
                    onClick={() => toggleSymptom(s)}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>

              <div className="mt-3" style={{ display: 'flex', gap: 12 }}>
              <button type="button" className="btn" onClick={runDetection} disabled={running}>
                <ScanSearch size={18} />
                {running ? t('misc.loading') : t('detect.run')}
              </button>
              <button type="button" className="btn btn-ghost" onClick={reset}>
                <RotateCcw size={18} /> {t('detect.reset')}
              </button>
              </div>

            <p
              className="mt-3 muted"
              style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: '0.8rem' }}
            >
              {source === 'api' ? <Cloud size={14} /> : <WifiOff size={14} />}
              {source === 'api'
                ? t('detect.apiPowered')
                : source === 'local'
                  ? t('detect.offlineFallback')
                  : t('detect.apiReady')}
            </p>
          </div>

          {/* ===== Result panel ===== */}
          <div>
            <AnimatePresence mode="wait">
              {running ? (
                <motion.div
                  key="loading"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="glass"
                  style={{ padding: 40, textAlign: 'center' }}
                >
                  <div className="scan-loader">
                    <ScanSearch size={40} />
                  </div>
                  <p className="muted mt-2">{t('detect.scanning')}</p>
                </motion.div>
              ) : result ? (
                <motion.div key="result" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                  <DoctorReport report={result} image={image} />
                </motion.div>
              ) : (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="glass"
                  style={{ padding: 30, textAlign: 'center' }}
                >
                  <ScanSearch size={40} style={{ color: 'var(--green-300)', margin: '0 auto 12px' }} />
                  <p className="muted">{t('detect.noResult')}</p>
                </motion.div>
              )}
            </AnimatePresence>
            <div className="glass mt-2" style={{ padding: 16, marginTop: 22 }}>
              <p style={{ fontSize: '0.85rem' }}>
                <strong>{t('detect.note')}:</strong> {t('detect.noteText')}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
