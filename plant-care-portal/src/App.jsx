import { useEffect } from 'react'
import { HashRouter, Routes, Route, useLocation } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import Navbar from './components/layout/Navbar.jsx'
import Footer from './components/layout/Footer.jsx'
import Notification from './components/ui/Notification.jsx'
import LeafParticles from './components/ui/LeafParticles.jsx'
import ProtectedRoute from './components/auth/ProtectedRoute.jsx'
import Home from './pages/Home.jsx'
import DiseaseDetection from './pages/DiseaseDetection.jsx'
import PlantIdentifier from './pages/PlantIdentifier.jsx'
import AllProblems from './pages/AllProblems.jsx'
import Blogs from './pages/Blogs.jsx'
import BotanistHelp from './pages/BotanistHelp.jsx'
import Feed from './pages/Feed.jsx'
import WeedCommunity from './pages/WeedCommunity.jsx'
import Database from './pages/Database.jsx'
import Login from './pages/auth/Login.jsx'
import Register from './pages/auth/Register.jsx'
import UserDashboard from './pages/auth/UserDashboard.jsx'
import AdminLayout from './pages/admin/AdminLayout.jsx'
import AdminOverview from './pages/admin/AdminOverview.jsx'
import AdminUsers from './pages/admin/AdminUsers.jsx'
import AdminDetections from './pages/admin/AdminDetections.jsx'
import AdminDiseases from './pages/admin/AdminDiseases.jsx'
import AdminFeedback from './pages/admin/AdminFeedback.jsx'
import { ensureSeeded } from './db/database.js'

function ScrollToTop() {
  const { pathname } = useLocation()
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' })
  }, [pathname])
  return null
}

function PageTransition({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -14 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  )
}

/**
 * The public site keeps its own navbar/footer and page transitions, exactly as
 * before authentication was added. The admin console is deliberately excluded:
 * `AdminLayout` renders its own full-screen shell with a sidebar and brand, so
 * the public chrome would double up on it.
 */
function SiteChrome() {
  const { pathname } = useLocation()
  const isAdmin = pathname.startsWith('/admin')

  return (
    <>
      {!isAdmin && <Navbar />}
      {isAdmin ? (
        // AdminLayout brings its own <main> as part of its full-screen shell.
        <AnimatedRoutes />
      ) : (
        <main style={{ position: 'relative', zIndex: 1 }}>
          <AnimatedRoutes />
        </main>
      )}
      {!isAdmin && <Footer />}
    </>
  )
}

function AnimatedRoutes() {
  const location = useLocation()
  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        {/* ---------- Authentication ---------- */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* ---------- User (any signed-in account) ---------- */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <PageTransition>
                <UserDashboard />
              </PageTransition>
            </ProtectedRoute>
          }
        />

        {/* ---------- Admin: every child requires the admin role ---------- */}
        <Route
          path="/admin"
          element={
            <ProtectedRoute role="admin">
              <AdminLayout />
            </ProtectedRoute>
          }
        >
          <Route index element={<AdminOverview />} />
          <Route path="users" element={<AdminUsers />} />
          <Route path="detections" element={<AdminDetections />} />
          <Route path="diseases" element={<AdminDiseases />} />
          <Route path="feedback" element={<AdminFeedback />} />
        </Route>

        {/* ---------- Existing public pages (unchanged) ---------- */}
        <Route path="/" element={<PageTransition><Home /></PageTransition>} />
        <Route path="/detect" element={<PageTransition><DiseaseDetection /></PageTransition>} />
        <Route path="/identify" element={<PageTransition><PlantIdentifier /></PageTransition>} />
        <Route path="/problems" element={<PageTransition><AllProblems /></PageTransition>} />
        <Route path="/blogs" element={<PageTransition><Blogs /></PageTransition>} />
        <Route path="/botanist" element={<PageTransition><BotanistHelp /></PageTransition>} />
        <Route path="/feed" element={<PageTransition><Feed /></PageTransition>} />
        <Route path="/community" element={<PageTransition><WeedCommunity /></PageTransition>} />
        <Route path="/database" element={<PageTransition><Database /></PageTransition>} />
        <Route path="*" element={<PageTransition><Home /></PageTransition>} />
      </Routes>
    </AnimatePresence>
  )
}

export default function App() {
  useEffect(() => {
    ensureSeeded()
  }, [])

  return (
    <HashRouter>
      <ScrollToTop />
      <LeafParticles count={9} />
      <SiteChrome />
      <Notification />
    </HashRouter>
  )
}
