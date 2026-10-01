import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Leaf, Mail, MapPin, Github } from 'lucide-react'
import { haptic } from '../../utils/haptics.js'

const tap = () => haptic('tap')

export default function Footer() {
  const { t } = useTranslation()

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-inner">
          <div>
            <h4>
              <Leaf size={18} style={{ verticalAlign: 'middle', marginRight: 6 }} />
              GreenRoot
            </h4>
            <p>{t('misc.footerTag')}</p>
          </div>
          <div>
            <h4>Explore</h4>
            <Link to="/detect" onClick={tap}>{t('nav.detect')}</Link>
            <br />
            <Link to="/identify" onClick={tap}>{t('nav.identify')}</Link>
            <br />
            <Link to="/blogs" onClick={tap}>{t('nav.blogs')}</Link>
            <br />
            <Link to="/database" onClick={tap}>{t('nav.database')}</Link>
          </div>
          <div>
            <h4>Community</h4>
            <Link to="/feed" onClick={tap}>{t('nav.feed')}</Link>
            <br />
            <Link to="/community" onClick={tap}>{t('nav.community')}</Link>
            <br />
            <Link to="/botanist" onClick={tap}>{t('nav.botanist')}</Link>
            <br />
            <Link to="/problems" onClick={tap}>{t('nav.problems')}</Link>
          </div>
          <div>
            <h4>Contact</h4>
            <p>
              <Mail size={14} style={{ verticalAlign: 'middle', marginRight: 6 }} />
              hello@greenroot.portal
            </p>
            <p>
              <MapPin size={14} style={{ verticalAlign: 'middle', marginRight: 6 }} />
              Everywhere the grass grows
            </p>
            <p>
              <Github size={14} style={{ verticalAlign: 'middle', marginRight: 6 }} />
              greenroot
            </p>
          </div>
        </div>
        <div className="footer-bottom">
          © {new Date().getFullYear()} GreenRoot · Online Plant Disease Detection Portal
        </div>
      </div>
    </footer>
  )
}
