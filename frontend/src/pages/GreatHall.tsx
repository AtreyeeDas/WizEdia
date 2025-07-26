import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

const GreatHall: React.FC = () => {
  const navigate = useNavigate();

  // Generate floating candles
  const candles = Array.from({ length: 20 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    delay: Math.random() * 5,
    duration: 3 + Math.random() * 2
  }));

  return (
    <div 
      className="min-h-screen"
      style={{
        backgroundImage: `url('/images/Great Hall.jpeg')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
      <Navbar />
      <div className="min-h-screen p-8 relative">
        {/* Dark overlay for better readability */}
        <div className="absolute inset-0 bg-black/30" />
        
        {/* Floating candles */}
        {candles.map((candle) => (
          <motion.div
            key={candle.id}
            className="absolute w-2 h-6 bg-gradient-to-b from-yellow-400 to-orange-500 rounded-full"
            style={{
              left: `${candle.x}%`,
              top: `${candle.y}%`,
            }}
            animate={{
              y: [0, -100, 0],
              opacity: [0.3, 1, 0.3],
              scale: [0.8, 1.2, 0.8],
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
              className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-1 h-2 bg-yellow-300 rounded-full"
              animate={{
                scale: [1, 1.3, 1],
                opacity: [0.7, 1, 0.7],
              }}
              transition={{
                duration: 1,
                repeat: Infinity,
                ease: "easeInOut"
              }}
            />
          </motion.div>
        ))}
        
        <div className="relative z-10 max-w-4xl mx-auto">
          <button
            onClick={() => navigate(-1)}
            className="absolute top-6 right-6 bg-rose-600/60 hover:bg-rose-500 text-parchment px-4 py-2 rounded-md border border-slate-500/50 shadow-md transition"
          >
            Back
          </button>

          {/* Header */}
          <motion.div
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-12"
          >
            <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-gold via-amber-400 to-gold mb-4">
              The Great Hall
            </h1>
            <p className="text-white/80 text-lg mb-8">
              Welcome to the heart of Hogwarts - where magic and learning come together
            </p>
          </motion.div>

          {/* Content */}
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="bg-gradient-to-br from-slate-800/80 to-slate-900/90 rounded-xl p-8 border border-gold/20 backdrop-blur-sm"
          >
            <div className="text-center">
              <h2 className="text-2xl font-['Cormorant_Garamond'] text-gold mb-6">
                Feast Your Eyes on Knowledge
              </h2>
              <p className="text-white/80 text-lg leading-relaxed mb-8">
                The Great Hall stands as a testament to the magical education that has thrived here for centuries. 
                With its enchanted ceiling reflecting the sky above and the floating candles providing eternal light, 
                this hallowed space has witnessed countless students discovering their magical potential.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className="bg-gradient-to-br from-gold/10 to-amber/10 p-6 rounded-lg border border-gold/30"
                >
                  <h3 className="text-xl font-['Cormorant_Garamond'] text-gold mb-3">
                    Enchanted Ceiling
                  </h3>
                  <p className="text-white/80">
                    The ceiling of the Great Hall is bewitched to look like the sky outside. 
                    It reflects the weather and time of day, creating a magical atmosphere for all who enter.
                  </p>
                </motion.div>
                
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className="bg-gradient-to-br from-gold/10 to-amber/10 p-6 rounded-lg border border-gold/30"
                >
                  <h3 className="text-xl font-['Cormorant_Garamond'] text-gold mb-3">
                    Floating Candles
                  </h3>
                  <p className="text-white/80">
                    Hundreds of candles float above the tables, providing warm, flickering light 
                    that never goes out, symbolizing the eternal flame of knowledge.
                  </p>
                </motion.div>
                
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className="bg-gradient-to-br from-gold/10 to-amber/10 p-6 rounded-lg border border-gold/30"
                >
                  <h3 className="text-xl font-['Cormorant_Garamond'] text-gold mb-3">
                    House Tables
                  </h3>
                  <p className="text-white/80">
                    Four long tables represent the four houses of Hogwarts, where students gather 
                    to share meals, study, and forge lasting friendships.
                  </p>
                </motion.div>
                
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  className="bg-gradient-to-br from-gold/10 to-amber/10 p-6 rounded-lg border border-gold/30"
                >
                  <h3 className="text-xl font-['Cormorant_Garamond'] text-gold mb-3">
                    Magical Feasts
                  </h3>
                  <p className="text-white/80">
                    The tables are magically filled with delicious food during meal times, 
                    appearing and disappearing as needed to feed the entire school.
                  </p>
                </motion.div>
              </div>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/dashboard')}
                className="mt-8 px-8 py-3 bg-gradient-to-r from-gold to-amber-500 text-white font-['Cormorant_Garamond'] font-semibold text-lg rounded-lg shadow-xl hover:shadow-2xl transition-all duration-300"
              >
                Enter the Hall
              </motion.button>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default GreatHall; 