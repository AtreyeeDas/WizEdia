import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { TrophyIcon, StarIcon, FireIcon, BoltIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

interface House {
  name: string;
  points: number;
  color: string;
  gradient: string;
  emblem: string;
  image: string;
  members: number;
  motto: string;
}

interface Achievement {
  id: number;
  title: string;
  description: string;
  points: number;
  category: 'study' | 'collaboration' | 'creativity' | 'leadership';
  date: Date;
  icon: string;
}

const HousePoints: React.FC = () => {
  const [selectedHouse, setSelectedHouse] = useState<string>('gryffindor');

  const houses: House[] = [
    {
      name: 'Gryffindor',
      points: 487,
      color: 'text-red-400',
      gradient: 'from-red-600 to-yellow-600',
      emblem: '🦁',
      image: '/images/gryffindor.jpg',
      members: 127,
      motto: 'Courage, Bravery, Nerve, and Chivalry'
    },
    {
      name: 'Slytherin',
      points: 465,
      color: 'text-green-400',
      gradient: 'from-green-600 to-gray-700',
      emblem: '🐍',
      image: '/images/sytherin.jpg',
      members: 119,
      motto: 'Ambition, Cunning, Leadership, and Resourcefulness'
    },
    {
      name: 'Ravenclaw',
      points: 498,
      color: 'text-blue-400',
      gradient: 'from-blue-600 to-indigo-700',
      emblem: '🦅',
      image: '/images/ravenclaw.jpg',
      members: 134,
      motto: 'Intelligence, Knowledge, Wit, and Learning'
    },
    {
      name: 'Hufflepuff',
      points: 452,
      color: 'text-yellow-400',
      gradient: 'from-yellow-600 to-amber-700',
      emblem: '🦡',
      image: '/images/hufflepuff.jpg',
      members: 142,
      motto: 'Hard Work, Patience, Loyalty, and Fair Play'
    }
  ];

  const recentAchievements: Achievement[] = [
    {
      id: 1,
      title: 'Master of Algorithms',
      description: 'Completed advanced algorithms course with perfect score',
      points: 50,
      category: 'study',
      date: new Date('2024-01-20'),
      icon: '📚'
    },
    {
      id: 2,
      title: 'Team Player',
      description: 'Successfully collaborated on group project',
      points: 30,
      category: 'collaboration',
      date: new Date('2024-01-19'),
      icon: '🤝'
    },
    {
      id: 3,
      title: 'Innovation Wizard',
      description: 'Created an innovative solution for hackathon',
      points: 75,
      category: 'creativity',
      date: new Date('2024-01-18'),
      icon: '💡'
    },
    {
      id: 4,
      title: 'Mentor Supreme',
      description: 'Helped fellow students with their studies',
      points: 40,
      category: 'leadership',
      date: new Date('2024-01-17'),
      icon: '🎓'
    }
  ];

  const categoryColors = {
    study: 'from-blue-500 to-indigo-600',
    collaboration: 'from-green-500 to-emerald-600',
    creativity: 'from-purple-500 to-violet-600',
    leadership: 'from-yellow-500 to-orange-600'
  };

  const maxPoints = Math.max(...houses.map(h => h.points));
  const sortedHouses = [...houses].sort((a, b) => b.points - a.points);
  
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
          <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-gold via-amber-400 to-gold mb-4">
            House Points Championship
          </h1>
          <p className="text-parchment/70 text-lg mb-8">
            The Great Hall displays the eternal competition for the House Cup
          </p>

          {/* Floating House Cup */}
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 1, delay: 0.3 }}
            className="relative mx-auto w-24 h-24 mb-8"
          >
            <motion.div
              animate={{ 
                rotateY: [0, 360],
                scale: [1, 1.1, 1]
              }}
              transition={{ 
                rotateY: { duration: 8, repeat: Infinity, ease: "linear" },
                scale: { duration: 2, repeat: Infinity }
              }}
              className="text-6xl filter drop-shadow-lg"
            >
              🏆
            </motion.div>
            
            {/* Magical aura */}
            <motion.div
              animate={{ 
                opacity: [0.3, 0.8, 0.3],
                scale: [1, 1.3, 1]
              }}
              transition={{ duration: 3, repeat: Infinity }}
              className="absolute inset-0 bg-gradient-to-br from-gold/20 to-amber-400/20 rounded-full blur-lg"
            />
          </motion.div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* House Leaderboard */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ x: -50, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-8 border border-gold/20 backdrop-blur-sm mb-8"
            >
              <h2 className="text-2xl font-['Cormorant_Garamond'] text-parchment mb-8 text-center">
                House Championship Standings
              </h2>

              <div className="space-y-6">
                {sortedHouses.map((house, index) => (
                  <motion.div
                    key={house.name}
                    initial={{ x: -100, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ duration: 0.6, delay: index * 0.2 }}
                    whileHover={{ scale: 1.02 }}
                    onClick={() => setSelectedHouse(house.name.toLowerCase())}
                    className={`group cursor-pointer relative bg-gradient-to-r ${house.gradient} p-6 rounded-xl shadow-xl border-2 border-white/20 hover:border-white/40 transition-all duration-300`}
                  >
                    {/* Ranking Badge */}
                    <div className="absolute -top-3 -left-3 w-10 h-10 bg-gradient-to-br from-gold to-amber-500 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-lg">
                      {index + 1}
                    </div>

                    {/* Crown for first place */}
                    {index === 0 && (
                      <motion.div
                        animate={{ rotate: [0, 5, -5, 0] }}
                        transition={{ duration: 2, repeat: Infinity }}
                        className="absolute -top-6 left-1/2 transform -translate-x-1/2 text-2xl"
                      >
                        👑
                      </motion.div>
                    )}

                    <div className="flex items-center space-x-6">
                      {/* House Image */}
                      <motion.div
                        whileHover={{ scale: 1.2, rotate: 15 }}
                        className="w-16 h-16 rounded-full overflow-hidden border-2 border-white/50 shadow-lg"
                      >
                        <img 
                          src={house.image} 
                          alt={house.name}
                          className="w-full h-full object-cover"
                        />
                      </motion.div>

                      {/* House Info */}
                      <div className="flex-1">
                        <h3 className="text-2xl font-['Cormorant_Garamond'] font-bold text-white mb-2">
                          {house.name}
                        </h3>
                        <p className="text-white/80 text-sm mb-3 italic">
                          "{house.motto}"
                        </p>
                        <div className="flex items-center space-x-4 text-sm text-white/70">
                          <span>👥 {house.members} members</span>
                        </div>
                      </div>

                      {/* Points Display */}
                      <div className="text-right">
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          transition={{ delay: 0.5 + index * 0.1, type: "spring" }}
                          className="text-4xl font-bold text-white mb-2"
                        >
                          {house.points}
                        </motion.div>
                        <div className="text-white/80 text-sm">points</div>
                        
                        {/* Progress Bar */}
                        <div className="w-32 bg-white/20 rounded-full h-2 mt-3 overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${(house.points / maxPoints) * 100}%` }}
                            transition={{ duration: 1, delay: 0.8 + index * 0.1 }}
                            className="h-full bg-gradient-to-r from-white/60 to-white/80"
                          />
                        </div>
                      </div>
                    </div>

                    {/* Magical sparkles */}
                    {index === 0 && (
                      <>
                        {[...Array(6)].map((_, i) => (
                          <motion.div
                            key={i}
                            className="absolute w-1 h-1 bg-gold rounded-full"
                            animate={{
                              scale: [0, 1, 0],
                              opacity: [0, 1, 0],
                              x: [0, Math.sin(i * 60) * 20],
                              y: [0, Math.cos(i * 60) * 20],
                            }}
                            transition={{
                              duration: 2,
                              repeat: Infinity,
                              delay: i * 0.3,
                            }}
                            style={{
                              left: '50%',
                              top: '50%',
                            }}
                          />
                        ))}
                      </>
                    )}
                  </motion.div>
                ))}
              </div>
            </motion.div>

            {/* Recent Achievements */}
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border border-gold/20 backdrop-blur-sm"
            >
              <h2 className="text-xl font-['Cormorant_Garamond'] text-parchment mb-6 flex items-center space-x-2">
                <StarIcon className="w-6 h-6 text-gold" />
                <span>Recent Achievements</span>
              </h2>

              <div className="space-y-4">
                {recentAchievements.map((achievement, index) => (
                  <motion.div
                    key={achievement.id}
                    initial={{ x: -30, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                    className="flex items-center space-x-4 p-4 bg-slate-700/30 rounded-lg border border-gold/10 hover:border-gold/20 transition-colors"
                  >
                    <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${categoryColors[achievement.category]} flex items-center justify-center text-xl shadow-lg`}>
                      {achievement.icon}
                    </div>
                    
                    <div className="flex-1">
                      <h3 className="font-medium text-parchment mb-1">
                        {achievement.title}
                      </h3>
                      <p className="text-sm text-parchment/70 mb-2">
                        {achievement.description}
                      </p>
                      <div className="text-xs text-parchment/50">
                        {achievement.date.toLocaleDateString()}
                      </div>
                    </div>
                    
                    <div className="text-right">
                      <div className="text-gold font-bold text-lg">
                        +{achievement.points}
                      </div>
                      <div className="text-xs text-gold/70">points</div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>

          {/* Personal Stats */}
          <div>
            <motion.div
              initial={{ x: 50, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border border-gold/20 backdrop-blur-sm sticky top-8"
            >
              <h2 className="text-xl font-['Cormorant_Garamond'] text-parchment mb-6 flex items-center space-x-2">
                <TrophyIcon className="w-6 h-6 text-gold" />
                <span>Your Progress</span>
              </h2>

              {/* Personal House */}
              <div className="text-center mb-8">
                <div className="w-16 h-16 mx-auto mb-3 rounded-full overflow-hidden border-2 border-red-400/50 shadow-lg">
                  <img 
                    src="/images/gryffindor.jpg" 
                    alt="Gryffindor"
                    className="w-full h-full object-cover"
                  />
                </div>
                <h3 className="text-lg font-medium text-red-400 mb-2">
                  Gryffindor
                </h3>
                <p className="text-parchment/70 text-sm italic">
                  "Courage, Bravery, Nerve, and Chivalry"
                </p>
              </div>

              {/* Personal Stats */}
              <div className="space-y-4 mb-8">
                <div className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <StarIcon className="w-5 h-5 text-gold" />
                    <span className="text-parchment">Your Points</span>
                  </div>
                  <span className="text-gold font-bold">127</span>
                </div>

                <div className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <FireIcon className="w-5 h-5 text-orange-400" />
                    <span className="text-parchment">Streak</span>
                  </div>
                  <span className="text-orange-400 font-bold">15 days</span>
                </div>

                <div className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <BoltIcon className="w-5 h-5 text-blue-400" />
                    <span className="text-parchment">Rank</span>
                  </div>
                  <span className="text-blue-400 font-bold">#8</span>
                </div>
              </div>

              {/* Level Progress */}
              <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-parchment/70">Level 7 Wizard</span>
                  <span className="text-parchment/70">127/200 XP</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-3 overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: '63.5%' }}
                    transition={{ duration: 1, delay: 1 }}
                    className="h-full bg-gradient-to-r from-gold to-amber-400"
                  />
                </div>
              </div>

              {/* Next Achievements */}
              <div>
                <h3 className="text-parchment/70 font-medium mb-3">Next Achievements:</h3>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2 text-sm text-parchment/60">
                    <div className="w-2 h-2 bg-gold rounded-full opacity-50" />
                    <span>Complete 5 more lessons</span>
                  </div>
                  <div className="flex items-center space-x-2 text-sm text-parchment/60">
                    <div className="w-2 h-2 bg-gold rounded-full opacity-50" />
                    <span>Help 3 fellow students</span>
                  </div>
                  <div className="flex items-center space-x-2 text-sm text-parchment/60">
                    <div className="w-2 h-2 bg-gold rounded-full opacity-50" />
                    <span>Maintain 20-day streak</span>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HousePoints;