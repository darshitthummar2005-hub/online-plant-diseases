/**
 * Password input with a show/hide toggle.
 *
 * The value is only ever held in component state and submitted straight to the
 * backend — it is never logged, stored or echoed back into the DOM. Switching to
 * `text` only changes how the browser paints the same characters.
 */

import { useState } from 'react'
import { Eye, EyeOff, Lock } from 'lucide-react'

export default function PasswordField({
  id,
  label,
  value,
  onChange,
  placeholder = '••••••••',
  autoComplete = 'current-password',
  error,
  hint,
  required = true,
  disabled = false,
}) {
  const [visible, setVisible] = useState(false)
  const describedBy = [error ? `${id}-error` : null, hint ? `${id}-hint` : null]
    .filter(Boolean)
    .join(' ')

  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <div className={`pw-wrap ${error ? 'pw-wrap--error' : ''}`}>
        <span className="pw-wrap__icon" aria-hidden="true">
          <Lock size={17} />
        </span>
        <input
          id={id}
          className="input pw-wrap__input"
          type={visible ? 'text' : 'password'}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          autoComplete={autoComplete}
          required={required}
          disabled={disabled}
          aria-invalid={error ? 'true' : undefined}
          aria-describedby={describedBy || undefined}
        />
        <button
          type="button"
          className="pw-wrap__toggle"
          onClick={() => setVisible((v) => !v)}
          disabled={disabled}
          aria-label={visible ? 'Hide password' : 'Show password'}
          aria-pressed={visible}
          title={visible ? 'Hide password' : 'Show password'}
        >
          {visible ? <EyeOff size={18} /> : <Eye size={18} />}
        </button>
      </div>
      {hint && !error && (
        <small className="pw-wrap__hint" id={`${id}-hint`}>
          {hint}
        </small>
      )}
      {error && (
        <small className="field-error" id={`${id}-error`} role="alert">
          {error}
        </small>
      )}
    </div>
  )
}
