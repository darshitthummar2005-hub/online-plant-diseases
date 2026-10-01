export function supportsHaptics() {
  return typeof navigator !== 'undefined' && typeof navigator.vibrate === 'function'
}

const PATTERNS = {
  tap: 10,
  press: [15, 30, 15],
  success: [20, 40, 20, 40, 30],
  error: [60, 40, 60],
  pop: 25,
}

export function haptic(type = 'tap') {
  if (!supportsHaptics()) return
  try {
    navigator.vibrate(PATTERNS[type] ?? PATTERNS.tap)
  } catch {
    /* ignore unsupported patterns */
  }
}
