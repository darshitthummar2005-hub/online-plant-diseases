import { useRef, useState, useCallback } from 'react'

export default function TiltCard({
  children,
  className = '',
  maxTilt = 12,
  scale = 1.02,
  as: Tag = 'div',
  style: userStyle,
  ...rest
}) {
  const ref = useRef(null)
  const [style, setStyle] = useState({})

  const onMove = useCallback(
    (e) => {
      const el = ref.current
      if (!el) return
      const rect = el.getBoundingClientRect()
      const px = (e.clientX - rect.left) / rect.width
      const py = (e.clientY - rect.top) / rect.height
      const rx = (0.5 - py) * maxTilt
      const ry = (px - 0.5) * maxTilt
      setStyle({
        '--rx': `${rx.toFixed(2)}deg`,
        '--ry': `${ry.toFixed(2)}deg`,
        transform: `perspective(1100px) rotateX(${rx.toFixed(2)}deg) rotateY(${ry.toFixed(2)}deg) scale(${scale})`,
      })
    },
    [maxTilt, scale]
  )

  const onLeave = useCallback(() => {
    setStyle({ transform: 'perspective(1100px) rotateX(0deg) rotateY(0deg) scale(1)' })
  }, [])

  return (
    <Tag
      ref={ref}
      className={`tilt-card ${className}`}
      style={{ ...style, ...userStyle }}
      onMouseMove={onMove}
      onMouseLeave={onLeave}
      {...rest}
    >
      {children}
    </Tag>
  )
}
