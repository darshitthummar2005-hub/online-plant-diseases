import { createContext, useContext, useCallback, useState } from 'react'
import { haptic } from '../utils/haptics.js'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [notification, setNotification] = useState(null)

  const notify = useCallback((message, pattern = 'success') => {
    haptic(pattern)
    setNotification(message)
    window.setTimeout(() => setNotification(null), 2600)
  }, [])

  const clearNotification = useCallback(() => setNotification(null), [])

  return (
    <AppContext.Provider value={{ notify, notification, clearNotification }}>
      {children}
    </AppContext.Provider>
  )
}

export function useApp() {
  return useContext(AppContext)
}
