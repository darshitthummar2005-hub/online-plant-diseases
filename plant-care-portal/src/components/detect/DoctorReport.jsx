import { useTranslation } from 'react-i18next'
import { motion } from 'framer-motion'
import {
  Info,
  Stethoscope,
  Bug,
  Sprout,
  Leaf,
  ShieldCheck,
  Flower2,
  Activity,
  CloudSun,
  Siren,
  UserCheck,
  FlaskConical,
  Droplets,
  Thermometer,
  CloudRain,
  Package,
  Microscope,
  Syringe,
  CalendarClock,
  BookOpenText,
  Beaker,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  ScanLine,
  ListChecks,
} from 'lucide-react'

const SEVERITY_COLORS = {
  Mild: '#2f7d4f',
  Low: '#2f7d4f',
  Moderate: '#b07d2b',
  Medium: '#b07d2b',
  Severe: '#b23b2e',
  High: '#b23b2e',
}

function severityColor(value) {
  return SEVERITY_COLORS[value] || SEVERITY_COLORS.Moderate
}

function Section({ icon: Icon, title, tone = 'green', children, empty }) {
  if (empty) return null
  return (
    <motion.section
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      className="report-section"
    >
      <div className={`report-section-head tone-${tone}`}>
        <span className="report-section-icon">
          <Icon size={20} />
        </span>
        <h3>{title}</h3>
      </div>
      <div className="report-section-body">{children}</div>
    </motion.section>
  )
}

function PillList({ items, className = '' }) {
  if (!items?.length) return null
  return (
    <div className={`pill-row ${className}`}>
      {items.map((item, i) => (
        <span key={`${item}-${i}`} className="pill">
          {item}
        </span>
      ))}
    </div>
  )
}

function ItemList({ items, icon: Icon }) {
  if (!items?.length) return null
  return (
    <ul className="item-list">
      {items.map((item, i) => (
        <li key={`${item}-${i}`}>
          {Icon && <Icon size={14} />}
          <span>{item}</span>
        </li>
      ))}
    </ul>
  )
}

/** Numbered quick-action steps shown at the top of the treatment plan. */
function TreatmentSteps({ steps }) {
  if (!steps?.length) return null
  return (
    <div className="treatment-steps">
      {steps.map((step, i) => (
        <div className="treatment-step" key={`${step}-${i}`}>
          <span className="treatment-step-num">{i + 1}</span>
          <span>{step}</span>
        </div>
      ))}
    </div>
  )
}

/** A single treatment method rendered as a clean visual card. */
function MethodCard({ tone = 'organic', icon: Icon, title, children, note }) {
  return (
    <div className={`method-card method-card--${tone}`}>
      <div className="method-head">
        <span className="method-icon">
          <Icon size={20} />
        </span>
        <strong>{title}</strong>
      </div>
      <div className="method-body">{children}</div>
      {note && <p className="method-note">{note}</p>}
    </div>
  )
}

function MethodRow({ icon: Icon, label, value }) {
  if (!value) return null
  return (
    <p className="method-row">
      {Icon && <Icon size={13} />}
      {label && <strong>{label}: </strong>}
      <span>{value}</span>
    </p>
  )
}

export default function DoctorReport({ report, image }) {
  const { t } = useTranslation()
  if (!report) return null

  const confidence = Math.max(0, Math.min(100, report.confidence || 0))
  const confColor =
    confidence >= 85 ? 'var(--green-500)' : confidence >= 70 ? '#b07d2b' : '#b23b2e'
  const severity = report.severity || 'Moderate'
  const expert = report.expert_recommended

  const chem = report.chemical_treatment || []
  const bio = report.biological_treatment || []
  const org = report.organic_remedies || []
  const tips = report.prevention_tips || []
  const fert = report.fertilizer || {}
  const sev = report.severity_levels || {}
  const weather = report.weather_conditions || {}
  const emergency = report.emergency_actions || []
  const causes = report.causes || []

  return (
    <motion.div
      key="report"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      className="doctor-report"
    >
      {/* ===== Diagnosis hero — highlighted disease name + picture ===== */}
      <div className="report-hero report-hero--flash">
        <div className="report-hero-grid">
          <div className="report-hero-main">
            <div className="report-eyebrow">
              <ScanLine size={14} /> {t('detect.report.diagnosis')}
            </div>
            <h2 className="report-hero-title">
              {report.disease_name || t('detect.noResult')}
            </h2>
            {report.scientific_name && (
              <p className="report-sci">
                <Microscope size={13} /> {report.scientific_name}
              </p>
            )}
            {report.plant && (
              <p className="report-sci">
                <Sprout size={13} /> {t('detect.diagnosingFor')}: <strong>{report.plant}</strong>
              </p>
            )}
            <div className="report-badges">
              {report.category && (
                <span className="chip hero-chip">{report.category}</span>
              )}
              <span
                className="chip hero-chip"
                style={{ color: '#fff', background: severityColor(severity) }}
              >
                {severity}
              </span>
            </div>
          </div>

          {image && (
            <div className="report-imgwrap">
              <img
                src={image}
                alt="diagnosed leaf"
                referrerPolicy="no-referrer"
                className="report-image"
              />
              <span className="report-img-badge">
                <Sprout size={12} /> {t('detect.report.yourLeaf')}
              </span>
            </div>
          )}
        </div>

        <div className="report-confidence">
          <div className="report-confidence-label">
            <span>
              <Sparkles size={14} /> {t('detect.confidence')}
            </span>
            <strong style={{ color: confColor }}>{confidence}%</strong>
          </div>
          <div className="confidence-track">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${confidence}%` }}
              transition={{ duration: 0.8, ease: 'easeOut' }}
              style={{ background: confColor }}
            />
          </div>
          <div className="report-meta">
            {report.model_version && (
              <span>
                <Package size={12} /> {report.model_version}
              </span>
            )}
            {report.visual_signals?.length > 0 && (
              <span className="visual-signals">
                <Sparkles size={12} /> {t('detect.report.visualSignals')}:{' '}
                {report.visual_signals.join(', ')}
              </span>
            )}
          </div>
        </div>

        {expert && (
          <motion.div
            initial={{ opacity: 0, scale: 0.97 }}
            animate={{ opacity: 1, scale: 1 }}
            className="expert-banner"
          >
            <UserCheck size={20} />
            <div>
              <strong>{t('detect.report.consultExpert')}</strong>
              {report.consult_reason && <p>{report.consult_reason}</p>}
            </div>
          </motion.div>
        )}
      </div>

      {/* ===== Why it happens — causes ===== */}
      <Section
        icon={AlertTriangle}
        title={t('detect.report.whyItHappens')}
        tone="gold"
        empty={!report.description && !causes.length}
      >
        {report.description && <p className="report-text">{report.description}</p>}
        {causes.length > 0 && (
          <div className="why-grid">
            {causes.map((c, i) => (
              <div className="why-card" key={`${c}-${i}`}>
                <Bug size={16} />
                <span>{c}</span>
              </div>
            ))}
          </div>
        )}
      </Section>

      {/* ===== Symptoms ===== */}
      <Section
        icon={Info}
        title={t('detect.report.overview')}
        empty={!report.symptoms?.length && !report.matched_symptoms?.length && !report.affected_plants?.length}
      >
        {report.symptoms?.length > 0 && (
          <>
            <h4>{t('detect.report.symptoms')}</h4>
            <PillList items={report.symptoms} />
          </>
        )}
        {report.matched_symptoms?.length > 0 && (
          <p className="report-sub">
            <CheckCircle2 size={13} /> {t('detect.report.matched')}:{' '}
            {report.matched_symptoms.join(', ')}
          </p>
        )}
        {report.affected_plants?.length > 0 && (
          <p className="report-sub mt-2">
            <Leaf size={13} /> <strong>{t('detect.report.affectedPlants')}:</strong>{' '}
            {report.affected_plants.join(', ')}
          </p>
        )}
      </Section>

      {/* ===== Treatment plan ===== */}
      <Section
        icon={Stethoscope}
        title={t('detect.treatment')}
        tone="green"
        empty={!report.treatment?.length && !org.length && !bio.length && !chem.length}
      >
        <TreatmentSteps steps={report.treatment} />

        <div className="method-group">
          {org.length > 0 && (
            <div className="method-group-block">
              <h4>
                <Flower2 size={16} /> {t('detect.report.organic')}
              </h4>
              <div className="method-grid">
                {org.map((o, i) => (
                  <MethodCard
                    key={`${o.name}-${i}`}
                    tone="organic"
                    icon={Flower2}
                    title={o.name}
                  >
                    {o.recipe && (
                      <MethodRow icon={BookOpenText} label={t('detect.report.recipe')} value={o.recipe} />
                    )}
                    {o.application && (
                      <MethodRow icon={Beaker} label={t('detect.report.application')} value={o.application} />
                    )}
                    {o.frequency && (
                      <MethodRow icon={CalendarClock} label={t('detect.report.frequency')} value={o.frequency} />
                    )}
                  </MethodCard>
                ))}
              </div>
            </div>
          )}

          {bio.length > 0 && (
            <div className="method-group-block">
              <h4>
                <Bug size={16} /> {t('detect.report.biological')}
              </h4>
              <div className="method-grid">
                {bio.map((b, i) => (
                  <MethodCard
                    key={`${b.agent}-${i}`}
                    tone="bio"
                    icon={Microscope}
                    title={b.agent}
                  >
                    {b.type && <span className="pill pill--cool">{b.type}</span>}
                    {b.application && (
                      <MethodRow icon={Beaker} label={t('detect.report.application')} value={b.application} />
                    )}
                    {b.when_to_apply && (
                      <MethodRow icon={CalendarClock} label={t('detect.report.whenToApply')} value={b.when_to_apply} />
                    )}
                    {b.notes && <p className="method-note">{b.notes}</p>}
                  </MethodCard>
                ))}
              </div>
            </div>
          )}

          {chem.length > 0 && (
            <div className="method-group-block">
              <h4>
                <FlaskConical size={16} /> {t('detect.report.chemical')}
              </h4>
              <div className="method-grid">
                {chem.map((c, i) => (
                  <MethodCard
                    key={`${c.name}-${i}`}
                    tone="chem"
                    icon={Syringe}
                    title={c.name}
                  >
                    {c.brand_names?.length > 0 && (
                      <MethodRow icon={Package} label={t('detect.report.brandNames')} value={c.brand_names.join(', ')} />
                    )}
                    {c.active_ingredients?.length > 0 && (
                      <MethodRow icon={Microscope} label={t('detect.report.activeIngredients')} value={c.active_ingredients.join(', ')} />
                    )}
                    {c.dosage && (
                      <MethodRow icon={Droplets} label={t('detect.report.dosage')} value={c.dosage} />
                    )}
                    {c.waiting_period && (
                      <MethodRow icon={CalendarClock} label={t('detect.report.waitingPeriod')} value={c.waiting_period} />
                    )}
                    {c.safety_precautions?.length > 0 && (
                      <div>
                        <strong className="report-label">
                          {t('detect.report.safetyPrecautions')}
                        </strong>
                        <ItemList items={c.safety_precautions} icon={ShieldCheck} />
                      </div>
                    )}
                  </MethodCard>
                ))}
              </div>
            </div>
          )}
        </div>
      </Section>

      {/* ===== Prevention tips ===== */}
      <Section
        icon={ShieldCheck}
        title={t('detect.report.prevention')}
        tone="green"
        empty={!tips.length && !report.prevention?.length}
      >
        <div className="tip-grid">
          {tips.map((tip, i) => (
            <div className="tip-card" key={`${tip.title}-${i}`}>
              <span className="pill pill--cool">{tip.category}</span>
              <strong>{tip.title}</strong>
              {tip.description && <p>{tip.description}</p>}
            </div>
          ))}
          {tips.length === 0 &&
            (report.prevention || []).map((p, i) => (
              <div className="tip-card" key={`${p}-${i}`}>
                <p>{p}</p>
              </div>
            ))}
        </div>
      </Section>

      {/* ===== Fertilizer ===== */}
      <Section
        icon={Sprout}
        title={t('detect.report.fertilizer')}
        tone="gold"
        empty={!fert.npk && !fert.organic?.length && !fert.micronutrients?.length && !fert.soil_improvement?.length}
      >
        <div className="report-card-grid">
          <div className="report-card">
            {fert.npk && (
              <p className="report-key">
                <strong>
                  <Activity size={14} /> NPK:
                </strong>{' '}
                {fert.npk}
              </p>
            )}
            {fert.organic?.length > 0 && (
              <>
                <h4>{t('detect.report.organicFert')}</h4>
                <ItemList items={fert.organic} icon={Leaf} />
              </>
            )}
            {fert.micronutrients?.length > 0 && (
              <>
                <h4>{t('detect.report.micronutrients')}</h4>
                <ItemList items={fert.micronutrients} icon={Sparkles} />
              </>
            )}
            {fert.soil_improvement?.length > 0 && (
              <>
                <h4>{t('detect.report.soilImprovement')}</h4>
                <ItemList items={fert.soil_improvement} icon={ShieldCheck} />
              </>
            )}
          </div>
        </div>
      </Section>

      {/* ===== Severity levels ===== */}
      <Section
        icon={Activity}
        title={t('detect.report.severityLevels')}
        tone="red"
        empty={!sev.mild && !sev.moderate && !sev.severe}
      >
        <div className="severity-row">
          {['mild', 'moderate', 'severe'].map((key) =>
            sev[key] ? (
              <div className={`severity-box sev-${key}`} key={key}>
                <h4>{t(`detect.report.${key}`)}</h4>
                <p>{sev[key]}</p>
              </div>
            ) : null
          )}
        </div>
      </Section>

      {/* ===== Weather ===== */}
      <Section
        icon={CloudSun}
        title={t('detect.report.weather')}
        tone="blue"
        empty={!weather.humidity && !weather.temperature && !weather.rainfall}
      >
        <div className="weather-grid">
          {weather.humidity && (
            <div className="weather-item">
              <Droplets size={18} />
              <strong>{t('detect.report.humidity')}</strong>
              <span>{weather.humidity}</span>
            </div>
          )}
          {weather.temperature && (
            <div className="weather-item">
              <Thermometer size={18} />
              <strong>{t('detect.report.temperature')}</strong>
              <span>{weather.temperature}</span>
            </div>
          )}
          {weather.rainfall && (
            <div className="weather-item">
              <CloudRain size={18} />
              <strong>{t('detect.report.rainfall')}</strong>
              <span>{weather.rainfall}</span>
            </div>
          )}
        </div>
      </Section>

      {/* ===== Emergency actions ===== */}
      <Section
        icon={Siren}
        title={t('detect.report.emergency')}
        tone="red"
        empty={!emergency.length}
      >
        <ol className="emergency-list">
          {emergency.map((e, i) => (
            <li key={`${e}-${i}`}>{e}</li>
          ))}
        </ol>
        <p className="emergency-note">
          <Siren size={14} /> {t('detect.report.emergencyNote')}
        </p>
      </Section>
    </motion.div>
  )
}
