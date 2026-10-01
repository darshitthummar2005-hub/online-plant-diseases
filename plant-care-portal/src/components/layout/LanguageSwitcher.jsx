import { useTranslation } from 'react-i18next'
import { Languages } from 'lucide-react'
import { haptic } from '../../utils/haptics.js'

const FLAGS = { en: '🇬🇧', hi: '🇮🇳', gu: '🇮🇳', es: '🇪🇸', fr: '🇫🇷' }

export default function LanguageSwitcher() {
  const { i18n } = useTranslation()

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng)
    haptic('tap')
  }

  return (
    <div style={{ position: 'relative', display: 'inline-flex', alignItems: 'center' }}>
      <Languages size={18} style={{ marginRight: 6 }} />
      <select
        className="input"
        style={{ padding: '8px 12px', borderRadius: 999, fontSize: '0.9rem' }}
        value={i18n.resolvedLanguage}
        onChange={(e) => changeLanguage(e.target.value)}
        aria-label="Language"
      >
        {Object.entries(FLAGS).map(([code, flag]) => (
          <option key={code} value={code}>
            {flag} {code.toUpperCase()}
          </option>
        ))}
      </select>
    </div>
  )
}
