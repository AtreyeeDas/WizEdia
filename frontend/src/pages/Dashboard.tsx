import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ChatBubbleLeftIcon,
  BookOpenIcon,
  ClockIcon,
  EyeIcon,
  BeakerIcon,
  BuildingLibraryIcon,
  GlobeAltIcon,
  MapIcon,
  AcademicCapIcon,
  SparklesIcon,
  TrophyIcon,
} from '@heroicons/react/24/outline';

interface DashboardProps {
  userHouse: string | null;
  userPatronus: string | null;
  userData: { email: string; name: string } | null;
}

const Dashboard: React.FC<DashboardProps> = ({ userHouse, userPatronus, userData }) => {
  const features = [
    {
      title: 'Ask Hermione',
      description: 'Seek wisdom from the brightest witch of her age',
      icon: ChatBubbleLeftIcon,
      path: '/hermione',
      color: 'from-blue-500 to-indigo-600',
      bgPattern: 'bg-gradient-to-br from-blue-900/20 to-indigo-900/20'
    },
    {
      title: 'Pensieve Log',
      description: 'Store and reflect upon your thoughts and memories',
      icon: BookOpenIcon,
      path: '/pensieve',
      color: 'from-gray-400 to-gray-600',
      bgPattern: 'bg-gradient-to-br from-gray-800/20 to-gray-900/20'
    },
    {
      title: 'Time Turner',
      description: 'Manage your schedule and never miss a deadline',
      icon: ClockIcon,
      path: '/time-turner',
      color: 'from-yellow-500 to-amber-600',
      bgPattern: 'bg-gradient-to-br from-yellow-900/20 to-amber-900/20'
    },
    {
      title: 'Mirror of Erised',
      description: 'Discover your deepest desires and aspirations',
      icon: EyeIcon,
      path: '/mirror',
      color: 'from-purple-500 to-violet-600',
      bgPattern: 'bg-gradient-to-br from-purple-900/20 to-violet-900/20'
    },
    {
      title: 'Potions Lab',
      description: 'Mix complex concepts into understandable solutions',
      icon: BeakerIcon,
      path: '/potions',
      color: 'from-green-500 to-emerald-600',
      bgPattern: 'bg-gradient-to-br from-green-900/20 to-emerald-900/20'
    },
    {
      title: 'Forbidden Library',
      description: 'Check your work for originality and authenticity',
      icon: BuildingLibraryIcon,
      path: '/library',
      color: 'from-red-600 to-red-800',
      bgPattern: 'bg-gradient-to-br from-red-900/20 to-red-800/20'
    },
    {
      title: 'Prophecy Engine',
      description: 'Foresee upcoming deadlines and important events',
      icon: GlobeAltIcon,
      path: '/prophecy',
      color: 'from-indigo-500 to-purple-600',
      bgPattern: 'bg-gradient-to-br from-indigo-900/20 to-purple-900/20'
    },
    {
      title: 'Marauder\'s Map',
      description: 'Discover learning opportunities in your area',
      icon: MapIcon,
      path: '/map',
      color: 'from-amber-600 to-yellow-700',
      bgPattern: 'bg-gradient-to-br from-amber-900/20 to-yellow-900/20'
    },
    {
      title: 'Professor Pods',
      description: 'Receive guidance from Hogwarts\' finest professors',
      icon: AcademicCapIcon,
      path: '/professors',
      color: 'from-slate-500 to-slate-700',
      bgPattern: 'bg-gradient-to-br from-slate-800/20 to-slate-900/20'
    },
    {
      title: 'Quidditch Quest',
      description: 'Plan projects and find teammates for hackathons',
      icon: SparklesIcon,
      path: '/quidditch',
      color: 'from-orange-500 to-red-600',
      bgPattern: 'bg-gradient-to-br from-orange-900/20 to-red-900/20'
    },
    {
      title: 'Patronus Quiz',
      description: 'Discover your Hogwarts House and magical Patronus',
      icon: SparklesIcon,
      path: '/patronus-quiz',
      color: 'from-purple-600 to-indigo-700',
      bgPattern: 'bg-gradient-to-br from-purple-900/20 to-indigo-900/20'
    },
    {
      title: 'House Points',
      description: 'Track your progress and compete with fellow students',
      icon: TrophyIcon,
      path: '/house-points',
      color: 'from-gold to-yellow-600',
      bgPattern: 'bg-gradient-to-br from-yellow-900/20 to-amber-900/20'
    },
  ];

  // Generate floating candles
  const candles = Array.from({ length: 25 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: 100 + Math.random() * 20, // Start from bottom
    delay: Math.random() * 3,
    duration: 8 + Math.random() * 4 // Slower movement
  }));

  const getHouseGreeting = () => {
    if (!userHouse) return "Welcome to Hogwarts";
    
    const userName = userData?.name ? `, ${userData.name.split(' ')[0]}` : '';
    
    const houseGreetings = {
      gryffindor: `Welcome, brave Gryffindor${userName}!`,
      slytherin: `Welcome, cunning Slytherin${userName}!`,
      ravenclaw: `Welcome, wise Ravenclaw${userName}!`,
      hufflepuff: `Welcome, loyal Hufflepuff${userName}!`
    };
    
    return houseGreetings[userHouse as keyof typeof houseGreetings] || `Welcome to Hogwarts${userName}`;
  };

  const getHouseColors = () => {
    if (!userHouse) return "from-purple-600 to-indigo-700";
    
    const houseColors = {
      gryffindor: "from-red-600 to-yellow-600",
      slytherin: "from-green-600 to-gray-700",
      ravenclaw: "from-blue-600 to-indigo-700",
      hufflepuff: "from-yellow-600 to-amber-700"
    };
    
    return houseColors[userHouse as keyof typeof houseColors] || "from-purple-600 to-indigo-700";
  };

  const navigate=useNavigate()

  return (
    <div 
      className="min-h-screen"
      style={{
        backgroundImage: `url('/images/Greathall.jpeg')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
      <div className="min-h-screen p-8 relative">
        {/* Dark overlay for better readability */}
        <div className="absolute inset-0 bg-black/30" />
        
        {/* Floating candles */}
        {candles.map((candle) => (
          <motion.div
            key={candle.id}
            className="absolute w-3 h-8 bg-white rounded-full shadow-lg"
            style={{
              left: `${candle.x}%`,
              top: `${candle.y}%`,
            }}
            animate={{
              y: [0, -150],
              opacity: [0, 1, 1, 0],
              scale: [0.8, 1, 1, 0.8],
            }}
            transition={{
              duration: candle.duration,
              repeat: Infinity,
              delay: candle.delay,
              ease: "easeInOut"
            }}
          >
            {/* Candle flame */}
            <motion.div
              className="absolute -top-2 left-1/2 transform -translate-x-1/2 w-2 h-3 bg-gradient-to-b from-orange-400 to-orange-600 rounded-full"
              animate={{
                scale: [1, 1.2, 1],
                opacity: [0.8, 1, 0.8],
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            >
              {/* Inner flame glow */}
              <div className="absolute inset-0 bg-orange-300 rounded-full opacity-60" />
            </motion.div>
          </motion.div>
        ))}

        <div className="relative z-10 max-w-7xl mx-auto">
          <button
            onClick={() => navigate("/landing")}
            className="absolute top-6 right-6 bg-rose-600/60 hover:bg-rose-500 text-parchment px-4 py-2 rounded-md border border-slate-500/50 shadow-md transition"
          >
            Logout
          </button>
          
          {/* Header */}
          <motion.div
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-12"
          >
            <h1 className="text-5xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-gold via-amber-400 to-gold mb-4">
              Great Hall Dashboard
            </h1>
            <h2 className="text-2xl font-['Cormorant_Garamond'] text-white mb-6">
              {getHouseGreeting()}
            </h2>
          </motion.div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              
              return (
                <motion.div
                  key={feature.path}
                  initial={{ y: 50, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  whileHover={{ y: -5, scale: 1.02 }}
                  className="group"
                >
                  <Link
                    to={feature.path}
                    className={`block h-full p-6 rounded-xl border border-gold/20 ${feature.bgPattern} backdrop-blur-sm transition-all duration-300 hover:border-gold/40 hover:shadow-xl magical-border`}
                  >
                    <div className="flex flex-col items-center text-center space-y-4">
                      <div className={`p-4 rounded-full bg-gradient-to-br ${feature.color} shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                        <Icon className="w-8 h-8 text-white" />
                      </div>
                      
                      <h3 className="text-xl font-['Cormorant_Garamond'] font-semibold text-parchment">
                        {feature.title}
                      </h3>
                      
                      <p className="text-sm text-parchment/70 leading-relaxed">
                        {feature.description}
                      </p>
                    </div>
                    
                    {/* Hover effect overlay */}
                    <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-gold/0 via-gold/5 to-gold/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  </Link>
                </motion.div>
              );
            })}
          </div>

          {/* Quick Stats */}
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 1.2 }}
            className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            <div className="p-6 rounded-xl bg-gradient-to-br from-slate-800/40 to-slate-900/40 border border-gold/20 text-center backdrop-blur-sm">
              <div className="text-3xl font-bold text-gold mb-2">127</div>
              <div className="text-parchment/70">House Points Earned</div>
            </div>
            
            <div className="p-6 rounded-xl bg-gradient-to-br from-slate-800/40 to-slate-900/40 border border-gold/20 text-center backdrop-blur-sm">
              <div className="text-3xl font-bold text-silver mb-2">15</div>
              <div className="text-parchment/70">Spells Mastered</div>
            </div>
            
            <div className="p-6 rounded-xl bg-gradient-to-br from-slate-800/40 to-slate-900/40 border border-gold/20 text-center backdrop-blur-sm">
              <div className="text-3xl font-bold text-emerald-400 mb-2">8</div>
              <div className="text-parchment/70">Quests Completed</div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;