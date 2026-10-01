import { motion, AnimatePresence } from 'framer-motion'
import { useApp } from '../../context/AppContext.jsx'
import { Sprout } from 'lucide-react'

export default function Notification() {
  const { notification, clearNotification } = useApp()

  return (
    <AnimatePresence>
      {notification && (
        <motion.div
          className="notification"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 40 }}
          onClick={clearNotification}
          role="status"
        >
          <Sprout size={18} />
          {notification}
        </motion.div>
      )}
    </AnimatePresence>
  )
}
