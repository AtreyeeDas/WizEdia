import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { SparklesIcon, ArrowRightIcon } from '@heroicons/react/24/outline';

interface LandingProps {
  onGetStarted: () => void;
}

const Landing: React.FC<LandingProps> = ({ onGetStarted }) => {
  const [isAnimating, setIsAnimating] = useState(false);

  const handleGetStarted = () => {
    setIsAnimating(true);
    setTimeout(() => {
      onGetStarted();
    }, 1500);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen flex items-center justify-center relative overflow-hidden glitter-cursor"
      style={{
        backgroundImage: `url('/images/hogwarts.jpeg')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
      {/* Dark overlay for better text readability */}
      <div className="absolute inset-0 bg-black/40" />
      
      {/* Animated background */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900/60 via-purple-900/40 to-slate-800/60" />
        
        {/* Floating magical particles */}
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-gold rounded-full"
            animate={{
              y: [0, -100, 0],
              x: [0, Math.random() * 100 - 50, 0],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: 4 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 4,
            }}
            style={{
              left: `${Math.random() * 100}%`,
              top: `${100 + Math.random() * 20}%`,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 text-center max-w-4xl mx-auto px-6">
        {/* Hogwarts Castle Silhouette replaced with 3 large candles */}
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 1.5, ease: "easeOut" }}
          className="mb-12"
        >
          <div className="relative mx-auto w-96 h-64 mb-8 flex items-end justify-between">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="flex flex-col items-center"
                initial={{ y: 40, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2 * i, duration: 1 }}
                style={{ width: i === 1 ? '90px' : '60px', height: '180px' }}
              >
                {/* Candle flame */}
                <motion.div
                  className="w-10 h-16 bg-gradient-to-b from-orange-400 to-orange-600 rounded-full mb-[-12px] relative z-10"
                  animate={{
                    scale: [1, 1.15, 1],
                    opacity: [0.85, 1, 0.85],
                  }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                >
                  <div className="absolute inset-0 bg-orange-300 rounded-full opacity-60" />
                </motion.div>
                {/* Candle body */}
                <div className="w-full h-full bg-white rounded-b-3xl shadow-lg border border-slate-200" />
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Title */}
        <motion.h1
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
          className="text-6xl md:text-8xl font-['Cochin'] font-bold text-black mb-6"
          style={{
            textShadow: '0 0 20px rgba(255, 255, 255, 0.8), 0 0 40px rgba(255, 255, 255, 0.6), 0 0 60px rgba(255, 255, 255, 0.4)',
            filter: 'drop-shadow(0 0 10px rgba(255, 255, 255, 0.5))'
          }}
        >
          Hogwarts Study
        </motion.h1>

        <motion.h2
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1, delay: 0.8 }}
          className="text-2xl md:text-3xl font-['Cochin'] text-white mb-4"
        >
          Chamber of Academic Secrets
        </motion.h2>

        <motion.p
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 1, delay: 1.1 }}
          className="text-lg text-white mb-12 max-w-2xl mx-auto leading-relaxed font-['Cochin']"
        >
          Welcome to a magical learning experience where ancient wisdom meets modern education. 
          Discover your Patronus, join your House, and embark on an enchanted journey of knowledge.
        </motion.p>

        {/* Enter Button */}
        <motion.button
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.8, delay: 1.4, type: "spring", bounce: 0.4 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleGetStarted}
          disabled={isAnimating}
          className={`group relative px-8 py-4 bg-gradient-to-r from-emerald-600 to-emerald-700 text-white font-['Cormorant_Garamond'] font-semibold text-xl rounded-lg shadow-xl transition-all duration-300 hover:shadow-2xl magical-glow ${
            isAnimating ? 'opacity-50 cursor-not-allowed' : 'hover:from-emerald-500 hover:to-emerald-600'
          }`}
        >
          <span className="flex items-center space-x-3">
            <SparklesIcon className="w-6 h-6" />
            <span>{isAnimating ? 'Opening the Chamber...' : 'Get Started'}</span>
            <ArrowRightIcon className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
          </span>
          
          {/* Magical sparkle effect */}
          <div className="absolute inset-0 rounded-lg overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
          </div>
        </motion.button>

        {/* Floating instruction */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 2 }}
          className="text-sm text-white/80 mt-8 font-['Cochin']"
        >
          Create an account or sign in to begin your magical journey
        </motion.p>
      </div>

      {/* Magical transition overlay */}
      {isAnimating && (
        <motion.div
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 3, opacity: 1 }}
          className="fixed inset-0 bg-gradient-to-r from-emerald-600 to-emerald-700 rounded-full z-50"
          style={{ transformOrigin: 'center' }}
        />
      )}
    </motion.div>
  );
};

export default Landing;