import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  HomeIcon,
  ChatBubbleLeftIcon,
  BookOpenIcon,
  ClockIcon,
  EyeIcon,
  BeakerIcon,
  BuildingLibraryIcon,
  GlobeAltIcon,
  MapIcon,
  AcademicCapIcon,
  TrophyIcon,
  SparklesIcon,
  StarIcon,
} from '@heroicons/react/24/outline';

interface NavbarProps {
  userHouse: string | null;
  onReturnToLanding?: () => void;
}

const Navbar=()=> {
  const location = useLocation();
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);

  const navItems = [
    { path: '/', icon: BuildingLibraryIcon, label: 'Great Hall', color: 'from-amber-500 to-orange-600' },
    { path: '/hermione', icon: ChatBubbleLeftIcon, label: 'Ask Hermione', color: 'from-blue-500 to-indigo-600' },
    { path: '/pensieve', icon: BookOpenIcon, label: 'Pensieve', color: 'from-gray-400 to-gray-600' },
    { path: '/time-turner', icon: ClockIcon, label: 'Time Turner', color: 'from-yellow-500 to-amber-600' },
    { path: '/mirror', icon: EyeIcon, label: 'Mirror of Erised', color: 'from-purple-500 to-violet-600' },
    { path: '/potions', icon: BeakerIcon, label: 'Potions Lab', color: 'from-green-500 to-emerald-600' },
    { path: '/library', icon: BuildingLibraryIcon, label: 'Forbidden Library', color: 'from-red-600 to-red-800' },
    { path: '/prophecy', icon: GlobeAltIcon, label: 'Prophecy Engine', color: 'from-indigo-500 to-purple-600' },
    { path: '/map', icon: MapIcon, label: 'Marauder\'s Map', color: 'from-amber-600 to-yellow-700' },
    { path: '/professors', icon: AcademicCapIcon, label: 'Professor Pods', color: 'from-slate-500 to-slate-700' },
    { path: '/quidditch', icon: SparklesIcon, label: 'Quidditch Quest', color: 'from-orange-500 to-red-600' },
    { path: '/house-points', icon: TrophyIcon, label: 'House Points', color: 'from-gold to-yellow-600' },
    { path: '/patronus-quiz', icon: StarIcon, label: 'Patronus Quiz', color: 'from-purple-600 to-indigo-700' },
  ];

  const getHouseColors = (house: string | null) => {
    switch (house) {
      case 'gryffindor': return 'from-red-600 to-yellow-600';
      case 'slytherin': return 'from-green-600 to-gray-700';
      case 'ravenclaw': return 'from-blue-600 to-indigo-700';
      case 'hufflepuff': return 'from-yellow-600 to-amber-700';
      default: return 'from-purple-600 to-indigo-700';
    }
  };

  return (
    <motion.nav
      initial={{ x: -100, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className="fixed left-0 top-0 h-full w-16 bg-gradient-to-b from-slate-900/90 to-slate-800/90 backdrop-blur-md border-r border-gold/20 z-40"
    >
      <div className="flex flex-col items-center py-4 space-y-2">
        {/* Return to Landing Button */}
        {(
          <motion.div
            onHoverStart={() => setHoveredItem('Home')}
            onHoverEnd={() => setHoveredItem(null)}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            
            className="relative w-8 h-8 rounded-full bg-gradient-to-br from-gold to-amber-600 flex items-center justify-center shadow-lg cursor-pointer hover:shadow-xl transition-shadow"
          >
            <HomeIcon className="w-4 h-4 text-white" />
            
            {/* Tooltip */}
            {hoveredItem === 'Home' && (
              <motion.div
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="absolute left-12 top-1/2 transform -translate-y-1/2 bg-slate-800 text-parchment px-3 py-2 rounded-lg shadow-lg border border-gold/20 whitespace-nowrap z-50"
              >
                <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-1 w-2 h-2 bg-slate-800 rotate-45 border-l border-b border-gold/20"></div>
                Home
              </motion.div>
            )}
          </motion.div>
        )}

        {/* Navigation Items */}
        <div className="flex flex-col space-y-2 mt-4">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;

            return (
              <motion.div
                key={item.path}
                onHoverStart={() => setHoveredItem(item.label)}
                onHoverEnd={() => setHoveredItem(null)}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
              >
                <Link
                  to={item.path}
                  className={`relative block p-2 rounded-lg transition-all duration-300 ${
                    isActive
                      ? `bg-gradient-to-br ${item.color} shadow-lg magical-glow`
                      : 'bg-slate-800/50 hover:bg-slate-700/50'
                  }`}
                >
                  <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-parchment'}`} />
                  
                  {/* Tooltip */}
                  {hoveredItem === item.label && (
                    <motion.div
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      className="absolute left-12 top-1/2 transform -translate-y-1/2 bg-slate-800 text-parchment px-3 py-2 rounded-lg shadow-lg border border-gold/20 whitespace-nowrap z-50"
                    >
                      <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-1 w-2 h-2 bg-slate-800 rotate-45 border-l border-b border-gold/20"></div>
                      {item.label}
                    </motion.div>
                  )}
                </Link>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Floating magical orbs */}
      <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
        <motion.div
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
          className="w-2 h-2 bg-gold rounded-full opacity-60 blur-sm"
        />
      </div>
    </motion.nav>
  );
};

export default Navbar;