import { motion } from 'framer-motion'
import { Leaf } from 'lucide-react'

export default function PageHeader({ title, sub, emoji = '🌿' }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="mb-2"
    >
      <h1 className="section-title">
        <span aria-hidden="true">{emoji}</span>
        {title}
        <Leaf size={26} style={{ color: 'var(--green-400)' }} />
      </h1>
      <p className="section-sub">{sub}</p>
    </motion.div>
  )
}
