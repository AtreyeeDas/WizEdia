import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Auth from './pages/Auth';
import Dashboard from './pages/Dashboard';
import AskHermione from './pages/AskHermione';
import Pensieve from './pages/Pensieve';
import TimeTurner from './pages/TimeTurner';
import MirrorOfErised from './pages/MirrorOfErised';
import PotionMixer from './pages/PotionMixer';
import ForbiddenLibrary from './pages/ForbiddenLibrary';
import ProphecyEngine from './pages/ProphecyEngine';
import MarauderMap from './pages/MarauderMap';
import ProfessorPods from './pages/ProfessorPods';
import QuidditchQuest from './pages/QuidditchQuest';
import HousePoints from './pages/HousePoints';
import PatronusQuiz from './pages/PatronusQuiz';
import GreatHall from './pages/GreatHall';
import Landing from './pages/Landing';
import './App.css';
import Summarize from './components/Summarize';
import Fact from './components/Fact';
import Source from './components/Source';
import Citation from './components/Citation';
import Research from './components/Research';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showLanding, setShowLanding] = useState(true);
  const [userData, setUserData] = useState<{ email: string; name: string } | null>(null);
  const [userHouse, setUserHouse] = useState<string | null>(null);
  const [userPatronus, setUserPatronus] = useState<string | null>(null);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  const handleReturnToLanding = () => {
    setIsAuthenticated(false);
    setShowLanding(true);
    setUserData(null);
    setUserHouse(null);
    setUserPatronus(null);
  };

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const handleLandingComplete = () => {
    setShowLanding(false);
  };

  const handleAuth = (user: { email: string; name: string }) => {
    setUserData(user);
    setIsAuthenticated(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 text-parchment relative overflow-hidden">
      {/* Magical background effects */}
      <div className="fixed inset-0 opacity-20">
        <div className="absolute top-10 left-10 w-2 h-2 bg-gold rounded-full animate-pulse"></div>
        <div className="absolute top-32 right-20 w-1 h-1 bg-silver rounded-full animate-ping"></div>
        <div className="absolute bottom-20 left-1/4 w-1.5 h-1.5 bg-gold rounded-full animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 right-1/3 w-1 h-1 bg-silver rounded-full animate-ping delay-500"></div>
      </div>

      {/* Wand trail cursor effect */}
      <motion.div
        className="fixed w-6 h-6 pointer-events-none z-50"
        animate={{
          x: mousePosition.x - 12,
          y: mousePosition.y - 12,
        }}
        transition={{
          type: "spring",
          damping: 20,
          stiffness: 300
        }}
      >
        <div className="w-full h-full bg-gold rounded-full opacity-60 blur-sm"></div>
      </motion.div>

      <Router>
        <AnimatePresence mode="wait">
          {showLanding ? (
            <Landing key="landing" onGetStarted={handleLandingComplete} />
          ) : !isAuthenticated ? (
            <Auth key="auth" onAuth={handleAuth} />
          ) : (
            <motion.div
              key="main-app"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex"
            >
              
              <main className="flex-1 ml-16">
                <Routes>
                  <Route path="/" element={<Dashboard userHouse={userHouse} userPatronus={userPatronus} userData={userData} />} />
                  <Route path="/landing" element={<Landing key="landing" onGetStarted={handleLandingComplete} />} />
                  <Route path="/hermione" element={<AskHermione />} />
                  <Route path="/pensieve" element={<Pensieve />} />
                  <Route path="/time-turner" element={<TimeTurner />} />
                  <Route path="/mirror" element={<MirrorOfErised />} />
                  <Route path="/potions" element={<PotionMixer />} />
                  <Route path="/library" element={<ForbiddenLibrary />} />
                  <Route path="/summary" element={<Summarize />} />
                  <Route path="/fact" element={<Fact />} />
                  <Route path="/source" element={<Source />} />
                  <Route path="/citation" element={<Citation />} />
                  <Route path="/research" element={<Research />} />
                  <Route path="/prophecy" element={<ProphecyEngine />} />
                  <Route path="/map" element={<MarauderMap />} />
                  <Route path="/professors" element={<ProfessorPods />} />
                  <Route path="/quidditch" element={<QuidditchQuest />} />
                  <Route path="/house-points" element={<HousePoints />} />
                  <Route path="/patronus-quiz" element={<PatronusQuiz onComplete={(house, patronus) => {
                    setUserHouse(house);
                    setUserPatronus(patronus);
                  }} />} />
                  <Route path="/great-hall" element={<GreatHall />} />
                </Routes>
              </main>
            </motion.div>
          )}
        </AnimatePresence>
      </Router>
    </div>
  );
}

export default App;