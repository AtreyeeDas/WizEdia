import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { EyeIcon, CalendarIcon, ClockIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

interface Prophecy {
  id: number;
  title: string;
  description: string;
  daysUntil: number;
  urgency: 'low' | 'medium' | 'high' | 'critical';
  type: 'assignment' | 'exam' | 'project' | 'deadline' | 'event';
}

const ProphecyEngine: React.FC = () => {
  const [prophecies, setProphecies] = useState<Prophecy[]>([
    {
      id: 1,
      title: "The Great Transfiguration Exam",
      description: "Professor McGonagall's challenging examination approaches. The stars suggest thorough preparation of advanced transformation spells.",
      daysUntil: 3,
      urgency: 'high',
      type: 'exam'
    },
    {
      id: 2,
      title: "Potions Essay Deadline",
      description: "The ancient scrolls whisper of a brewing deadline. Your essay on advanced potion-making must be submitted.",
      daysUntil: 7,
      urgency: 'medium',
      type: 'assignment'
    },
    {
      id: 3,
      title: "Defense Against Dark Arts Project",
      description: "A project of great importance shall test your knowledge of protective spells and counter-curses.",
      daysUntil: 14,
      urgency: 'low',
      type: 'project'
    },
    {
      id: 4,
      title: "Quidditch Championship Finals",
      description: "The mystical orb reveals an approaching sporting event that will test both mind and body.",
      daysUntil: 21,
      urgency: 'medium',
      type: 'event'
    }
  ]);

  const [selectedProphecy, setSelectedProphecy] = useState<Prophecy | null>(null);
  const [crystalBallActive, setCrystalBallActive] = useState(false);

  const urgencyColors = {
    low: 'from-blue-400 to-blue-600',
    medium: 'from-yellow-400 to-orange-500',
    high: 'from-orange-500 to-red-500',
    critical: 'from-red-600 to-red-800'
  };

  const urgencyBorders = {
    low: 'border-blue-400/30',
    medium: 'border-yellow-400/30',
    high: 'border-orange-400/30',
    critical: 'border-red-400/30'
  };

  const typeIcons = {
    assignment: '📝',
    exam: '📋',
    project: '🚀',
    deadline: '⏰',
    event: '⭐'
  };

  const getUrgencyText = (urgency: Prophecy['urgency']) => {
    switch (urgency) {
      case 'low': return 'Distant Future';
      case 'medium': return 'Approaching';
      case 'high': return 'Imminent';
      case 'critical': return 'Critical';
    }
  };

  const activateCrystalBall = () => {
    setCrystalBallActive(true);
    setTimeout(() => setCrystalBallActive(false), 3000);
  };

  const revealProphecy = (prophecy: Prophecy) => {
    setSelectedProphecy(prophecy);
    activateCrystalBall();
  };
  
  const navigate=useNavigate()

  return (
    <div className="min-h-screen p-8">
      <Navbar />
      <button
        onClick={() => navigate(-1)}
        className="absolute top-6 right-6 bg-rose-600/60 hover:bg-rose-500 text-parchment px-4 py-2 rounded-md border border-slate-500/50 shadow-md transition"
      >
        Back
      </button>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-indigo-400 mb-4">
            The Prophecy Engine
          </h1>
          <p className="text-parchment/70 text-lg mb-8">
            Gaze into the crystal ball and foresee your academic future
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Crystal Ball */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 1, delay: 0.3 }}
              className="sticky top-8"
            >
              <div className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-8 border border-indigo-400/20 backdrop-blur-sm text-center">
                <h2 className="text-xl font-['Cormorant_Garamond'] text-indigo-300 mb-6">
                  Crystal Ball of Foresight
                </h2>

                {/* Crystal Ball */}
                <motion.div
                  animate={crystalBallActive ? {
                    scale: [1, 1.1, 1],
                    rotateY: [0, 360],
                  } : {}}
                  transition={{ duration: 2 }}
                  className="relative mx-auto w-48 h-48 mb-6 cursor-pointer"
                  onClick={activateCrystalBall}
                >
                  {/* Ball Base */}
                  <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-32 h-8 bg-gradient-to-r from-amber-600 to-gold rounded-full opacity-80" />
                  
                  {/* Crystal Ball */}
                  <div className="relative w-full h-full">
                    <div className="absolute inset-4 bg-gradient-to-br from-indigo-200/20 via-purple-300/30 to-indigo-400/40 rounded-full border-4 border-indigo-300/30 shadow-2xl backdrop-blur-sm overflow-hidden">
                      {/* Swirling mist */}
                      <motion.div
                        animate={{ 
                          rotate: 360,
                          scale: [1, 1.2, 1],
                        }}
                        transition={{ 
                          rotate: { duration: 20, repeat: Infinity, ease: "linear" },
                          scale: { duration: 4, repeat: Infinity }
                        }}
                        className="absolute inset-0 bg-gradient-to-br from-purple-400/20 via-indigo-300/30 to-purple-500/20 rounded-full"
                      />
                      
                      {/* Inner glow */}
                      <motion.div
                        animate={{
                          opacity: [0.3, 0.8, 0.3],
                          scale: [0.8, 1.2, 0.8],
                        }}
                        transition={{ duration: 3, repeat: Infinity }}
                        className="absolute inset-6 bg-gradient-to-br from-indigo-400/40 to-purple-600/40 rounded-full blur-sm"
                      />

                      {/* Prophecy Preview */}
                      {selectedProphecy && crystalBallActive && (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.5 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className="absolute inset-0 flex items-center justify-center text-center p-4"
                        >
                          <div className="text-white">
                            <div className="text-2xl mb-2">
                              {typeIcons[selectedProphecy.type]}
                            </div>
                            <div className="text-xs font-medium">
                              {selectedProphecy.daysUntil} days
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </div>

                    {/* Magical particles */}
                    {crystalBallActive && (
                      <>
                        {[...Array(12)].map((_, i) => (
                          <motion.div
                            key={i}
                            className="absolute w-1 h-1 bg-indigo-400 rounded-full"
                            animate={{
                              scale: [0, 1, 0],
                              y: [0, -40, -80],
                              x: [0, Math.sin(i * 30) * 30, Math.sin(i * 60) * 50],
                              opacity: [0, 1, 0],
                            }}
                            transition={{
                              duration: 2,
                              repeat: Infinity,
                              delay: i * 0.1,
                            }}
                            style={{
                              left: `${50}%`,
                              top: `${80}%`,
                            }}
                          />
                        ))}
                      </>
                    )}
                  </div>
                </motion.div>

                <p className="text-parchment/60 text-sm mb-4">
                  Click the crystal ball to reveal visions
                </p>

                {selectedProphecy && (
                  <motion.div
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    className="bg-slate-700/30 rounded-lg p-4 border border-indigo-400/20"
                  >
                    <h3 className="text-indigo-300 font-medium mb-2">
                      Last Vision Revealed
                    </h3>
                    <p className="text-parchment/80 text-sm">
                      {selectedProphecy.title}
                    </p>
                  </motion.div>
                )}
              </div>
            </motion.div>
          </div>

          {/* Prophecies List */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ x: 50, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              <h2 className="text-2xl font-['Cormorant_Garamond'] text-parchment mb-6 flex items-center space-x-2">
                <EyeIcon className="w-6 h-6 text-indigo-400" />
                <span>Upcoming Prophecies</span>
              </h2>

              <div className="space-y-4">
                {prophecies
                  .sort((a, b) => a.daysUntil - b.daysUntil)
                  .map((prophecy, index) => (
                    <motion.div
                      key={prophecy.id}
                      initial={{ y: 50, opacity: 0 }}
                      animate={{ y: 0, opacity: 1 }}
                      transition={{ duration: 0.6, delay: index * 0.1 }}
                      whileHover={{ scale: 1.02, y: -2 }}
                      onClick={() => revealProphecy(prophecy)}
                      className={`group cursor-pointer bg-gradient-to-br from-slate-800/40 to-slate-900/60 rounded-xl p-6 border ${urgencyBorders[prophecy.urgency]} backdrop-blur-sm hover:border-indigo-400/40 transition-all duration-300`}
                    >
                      <div className="flex items-start space-x-4">
                        {/* Icon & Urgency */}
                        <div className="flex flex-col items-center">
                          <div className={`w-12 h-12 rounded-full bg-gradient-to-br ${urgencyColors[prophecy.urgency]} flex items-center justify-center text-xl mb-2 shadow-lg`}>
                            {typeIcons[prophecy.type]}
                          </div>
                          <span className={`text-xs px-2 py-1 rounded-full bg-gradient-to-r ${urgencyColors[prophecy.urgency]} text-white font-medium`}>
                            {getUrgencyText(prophecy.urgency)}
                          </span>
                        </div>

                        {/* Content */}
                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="text-xl font-['Cormorant_Garamond'] text-parchment group-hover:text-indigo-300 transition-colors">
                              {prophecy.title}
                            </h3>
                            <div className="flex items-center space-x-2 text-indigo-400">
                              <CalendarIcon className="w-4 h-4" />
                              <span className="text-sm font-medium">
                                {prophecy.daysUntil === 0 ? 'Today' : 
                                 prophecy.daysUntil === 1 ? 'Tomorrow' : 
                                 `${prophecy.daysUntil} days`}
                              </span>
                            </div>
                          </div>

                          <p className="text-parchment/70 leading-relaxed mb-4 italic">
                            {prophecy.description}
                          </p>

                          <div className="flex items-center justify-between">
                            <span className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full bg-gradient-to-r ${urgencyColors[prophecy.urgency]} text-white text-sm`}>
                              <span className="capitalize">{prophecy.type}</span>
                            </span>

                            {prophecy.daysUntil <= 3 && (
                              <div className="flex items-center space-x-1 text-orange-400">
                                <ExclamationTriangleIcon className="w-4 h-4" />
                                <span className="text-sm font-medium">Urgent</span>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Hover effect */}
                      <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-indigo-400/0 via-indigo-400/5 to-indigo-400/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    </motion.div>
                  ))}
              </div>

              {/* Constellation Background */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 2, delay: 1 }}
                className="mt-12 relative h-32 rounded-xl bg-gradient-to-br from-slate-900/40 to-indigo-900/40 border border-indigo-400/10 overflow-hidden"
              >
                <div className="absolute inset-0 flex items-center justify-center">
                  <p className="text-indigo-300/60 text-center italic">
                    "The future belongs to those who prepare for it today"
                    <br />
                    <span className="text-sm">— Professor Trelawney's Wisdom</span>
                  </p>
                </div>

                {/* Stars */}
                {[...Array(20)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="absolute w-1 h-1 bg-indigo-400 rounded-full"
                    animate={{ 
                      opacity: [0.3, 1, 0.3],
                      scale: [0.8, 1.2, 0.8]
                    }}
                    transition={{ 
                      duration: 2 + Math.random() * 2,
                      repeat: Infinity,
                      delay: Math.random() * 2
                    }}
                    style={{
                      left: `${Math.random() * 100}%`,
                      top: `${Math.random() * 100}%`,
                    }}
                  />
                ))}
              </motion.div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProphecyEngine;