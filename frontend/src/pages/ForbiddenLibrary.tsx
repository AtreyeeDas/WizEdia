import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

const ForbiddenLibrary: React.FC = () => {
  const [showLibrary, setShowLibrary] = useState(false);
  const navigate = useNavigate();

  const handleLibraryEntrance = () => {
    setShowLibrary(true);
    setTimeout(() => setShowLibrary(false), 3000);
  };

  return (
    <div 
      className="min-h-screen"
      style={{
        backgroundImage: `url('/images/library.jpeg')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
      <Navbar />

      <div className="min-h-screen p-8 relative">
        {/* Dark overlay for better readability */}
        <div className="absolute inset-0 bg-black/40" />
        
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
            <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-red-400 via-red-500 to-red-400 mb-4">
              The Forbidden Library
            </h1>
            <p className="text-white/80 text-lg mb-8">
              "Those who cannot remember the past are condemned to repeat it" - Explore your scholarly tools
            </p>
          </motion.div>

          {/* Library Entrance Animation */}
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 1, delay: 0.3 }}
            className="relative mb-12"
          >
            <motion.div
              whileHover={{ scale: 1.02 }}
              onClick={handleLibraryEntrance}
              className="relative cursor-pointer group"
            >
              <div className="relative mx-auto w-96 h-48 bg-gradient-to-b from-slate-800 to-slate-900 rounded-t-lg border-4 border-red-600/30 shadow-2xl">
                <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-4 w-16 h-8 bg-slate-700 rounded-t-full border-2 border-red-600/30" />
                <div className="absolute bottom-0 left-8 w-4 h-32 bg-slate-700 border-x border-red-600/30" />
                <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-4 h-32 bg-slate-700 border-x border-red-600/30" />
                <div className="absolute bottom-0 right-8 w-4 h-32 bg-slate-700 border-x border-red-600/30" />

                <motion.div
                  animate={showLibrary ? { rotateY: -60 } : { rotateY: 0 }}
                  transition={{ duration: 0.8 }}
                  className="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-20 h-28 bg-gradient-to-b from-red-900 to-red-800 border-2 border-red-600"
                  style={{ transformOrigin: 'left center' }}
                >
                  <div className="absolute top-1/2 right-2 w-2 h-2 bg-gold rounded-full" />
                  <div className="absolute inset-2 flex flex-col items-center justify-center space-y-2">
                    <ExclamationTriangleIcon className="w-6 h-6 text-red-400" />
                    <div className="text-xs text-red-400 font-bold text-center">
                      RESTRICTED
                    </div>
                  </div>
                </motion.div>

                <div className="absolute top-8 left-12 w-3 h-4 bg-red-400 rounded opacity-60 candlelight-flicker" />
                <div className="absolute top-8 right-12 w-3 h-4 bg-red-400 rounded opacity-60 candlelight-flicker" />
                <div className="absolute top-16 left-1/2 transform -translate-x-1/2 w-3 h-4 bg-red-400 rounded opacity-60 candlelight-flicker" />

                <motion.div
                  animate={{ opacity: [0.2, 0.5, 0.2], scale: [1, 1.05, 1] }}
                  transition={{ duration: 3, repeat: Infinity }}
                  className="absolute inset-0 bg-gradient-to-br from-red-600/10 via-red-500/20 to-red-600/10 rounded-t-lg"
                />
              </div>

              {showLibrary && (
                <>
                  {[...Array(5)].map((_, i) => (
                    <motion.div
                      key={i}
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{
                        scale: 1,
                        opacity: 1,
                        y: [0, -20, 0],
                        x: [0, Math.sin(i) * 30, 0]
                      }}
                      transition={{
                        duration: 2,
                        delay: i * 0.2,
                        y: { repeat: Infinity, duration: 3 }
                      }}
                      className={`absolute w-4 h-6 bg-gradient-to-b ${
                        ['from-red-600 to-red-800', 'from-purple-600 to-purple-800', 'from-gray-600 to-gray-800', 'from-blue-600 to-blue-800', 'from-green-600 to-green-800'][i]
                      } rounded-sm shadow-lg`}
                      style={{
                        left: `${20 + i * 15}%`,
                        top: `${20 + Math.sin(i) * 10}%`,
                      }}
                    />
                  ))}
                </>
              )}

              <div className="text-center mt-4 text-red-400 text-sm opacity-0 group-hover:opacity-100 transition-opacity">
                Click to enter the Forbidden Library
              </div>
            </motion.div>
          </motion.div>

          {/* Card Section with Different Routes */}
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8"
          >
            {/* Existing cards */}
            <motion.div className="bg-gradient-to-br from-slate-800/80 to-slate-900/90 rounded-xl p-6 border border-red-400/20 backdrop-blur-sm">
              <h3 className="text-xl font-['Cormorant_Garamond'] text-red-300 mb-2">Summarize Content</h3>
              <p className="text-white/80 mb-4">Generate concise summaries for long texts.</p>
              <button
                onClick={() => navigate('/summary')}
                className="w-full py-3 bg-gradient-to-r from-red-600 to-red-700 text-white rounded-lg hover:from-red-500 hover:to-red-600 transition shadow"
              >
                Summarize Now
              </button>
            </motion.div>

            <motion.div className="bg-gradient-to-br from-slate-800/80 to-slate-900/90 rounded-xl p-6 border border-red-400/20 backdrop-blur-sm">
              <h3 className="text-xl font-['Cormorant_Garamond'] text-red-300 mb-2">Fact Check</h3>
              <p className="text-white/80 mb-4">Verify factual accuracy of statements.</p>
              <button
                onClick={() => navigate('/fact')}
                className="w-full py-3 bg-gradient-to-r from-red-600 to-red-700 text-white rounded-lg hover:from-red-500 hover:to-red-600 transition shadow"
              >
                Fact Check Now
              </button>
            </motion.div>

            <motion.div className="bg-gradient-to-br from-slate-800/80 to-slate-900/90 rounded-xl p-6 border border-red-400/20 backdrop-blur-sm">
              <h3 className="text-xl font-['Cormorant_Garamond'] text-red-300 mb-2">Compare Sources</h3>
              <p className="text-white/80 mb-4">Analyse and compare multiple sources.</p>
              <button
                onClick={() => navigate('/source')}
                className="w-full py-3 bg-gradient-to-r from-red-600 to-red-700 text-white rounded-lg hover:from-red-500 hover:to-red-600 transition shadow"
              >
                Compare Sources
              </button>
            </motion.div>

            <motion.div className="bg-gradient-to-br from-slate-800/80 to-slate-900/90 rounded-xl p-6 border border-red-400/20 backdrop-blur-sm">
              <h3 className="text-xl font-['Cormorant_Garamond'] text-red-300 mb-2">Citation Helper</h3>
              <p className="text-white/80 mb-4">Generate accurate citations for your research.</p>
              <button
                onClick={() => navigate('/citation')}
                className="w-full py-3 bg-gradient-to-r from-red-600 to-red-700 text-white rounded-lg hover:from-red-500 hover:to-red-600 transition shadow"
              >
                Cite Now
              </button>
            </motion.div>
          </motion.div>

          {/* ✅ New Research Assistant Card (centered below) */}
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 1 }}
            className="flex justify-center"
          >
            <motion.div className="bg-gradient-to-br from-slate-800/80 to-slate-900/90 rounded-xl p-6 border border-red-400/20 backdrop-blur-sm w-full max-w-md text-center">
              <h3 className="text-xl font-['Cormorant_Garamond'] text-red-300 mb-2">Research Assistant</h3>
              <p className="text-white/80 mb-4">Get AI assistance for your academic research and projects.</p>
              <button
                onClick={() => navigate('/research')}
                className="w-full py-3 bg-gradient-to-r from-red-600 to-red-700 text-white rounded-lg hover:from-red-500 hover:to-red-600 transition shadow"
              >
                Launch Assistant
              </button>
            </motion.div>
          </motion.div>

        </div>
      </div>
    </div>
  );
};

export default ForbiddenLibrary;