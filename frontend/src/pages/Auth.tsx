import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { EyeIcon, EyeSlashIcon, SparklesIcon } from '@heroicons/react/24/outline';

interface AuthProps {
  onAuth: (userData: { email: string; name: string }) => void;
}

const Auth: React.FC<AuthProps> = ({ onAuth }) => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Simulate authentication
    await new Promise(resolve => setTimeout(resolve, 2000));

    if (isSignUp && formData.password !== formData.confirmPassword) {
      alert('Passwords do not match!');
      setIsLoading(false);
      return;
    }

    // Simulate successful authentication
    onAuth({
      email: formData.email,
      name: formData.name || formData.email.split('@')[0]
    });

    setIsLoading(false);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div 
      className="min-h-screen text-parchment relative overflow-hidden flex items-center justify-center"
      style={{
        backgroundImage: `url('/images/hogwarts.jpeg')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
      {/* Dark overlay for better readability */}
      <div className="absolute inset-0 bg-black/50" />
      
      {/* Magical background effects */}
      <div className="fixed inset-0 opacity-20">
        <div className="absolute top-10 left-10 w-2 h-2 bg-gold rounded-full animate-pulse"></div>
        <div className="absolute top-32 right-20 w-1 h-1 bg-silver rounded-full animate-ping"></div>
        <div className="absolute bottom-20 left-1/4 w-1.5 h-1.5 bg-gold rounded-full animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 right-1/3 w-1 h-1 bg-silver rounded-full animate-ping delay-500"></div>
      </div>

      <div className="relative z-10 w-full max-w-md mx-auto px-6">
        {/* Header */}
        <motion.div
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-8"
        >
          <motion.div
            whileHover={{ scale: 1.1, rotate: 15 }}
            className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-purple-600 to-indigo-700 flex items-center justify-center shadow-lg magical-glow"
          >
            <SparklesIcon className="w-8 h-8 text-white" />
          </motion.div>
          
          <h1 className="text-3xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-gold via-amber-400 to-gold mb-2">
            {isSignUp ? 'Join Hogwarts' : 'Welcome Back'}
          </h1>
          <p className="text-white/80">
            {isSignUp ? 'Begin your magical learning journey' : 'Continue your magical studies'}
          </p>
        </motion.div>

        {/* Auth Form */}
        <motion.div
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="bg-gradient-to-br from-slate-800/80 to-slate-900/90 rounded-xl p-8 border border-gold/20 backdrop-blur-sm shadow-2xl"
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            <AnimatePresence mode="wait">
              {isSignUp && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <label className="block text-white/80 mb-2">Full Name</label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required={isSignUp}
                    className="w-full p-4 bg-slate-700/70 border border-gold/30 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold/50 transition-colors"
                    placeholder="Enter your full name"
                  />
                </motion.div>
              )}
            </AnimatePresence>

            <div>
              <label className="block text-white/80 mb-2">Email Address</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
                className="w-full p-4 bg-slate-700/70 border border-gold/30 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold/50 transition-colors"
                placeholder="Enter your email"
              />
            </div>

            <div>
              <label className="block text-white/80 mb-2">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  required
                  className="w-full p-4 pr-12 bg-slate-700/70 border border-gold/30 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold/50 transition-colors"
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-white/50 hover:text-white transition-colors"
                >
                  {showPassword ? (
                    <EyeSlashIcon className="w-5 h-5" />
                  ) : (
                    <EyeIcon className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>

            <AnimatePresence mode="wait">
              {isSignUp && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <label className="block text-white/80 mb-2">Confirm Password</label>
                  <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    required={isSignUp}
                    className="w-full p-4 bg-slate-700/70 border border-gold/30 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-gold/50 focus:border-gold/50 transition-colors"
                    placeholder="Confirm your password"
                  />
                </motion.div>
              )}
            </AnimatePresence>

            <motion.button
              type="submit"
              disabled={isLoading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className={`w-full py-4 rounded-lg font-['Cormorant_Garamond'] font-semibold text-lg transition-all duration-300 ${
                isLoading
                  ? 'bg-slate-600 text-white/50 cursor-not-allowed'
                  : 'bg-gradient-to-r from-emerald-600 to-emerald-700 text-white hover:from-emerald-500 hover:to-emerald-600 shadow-lg magical-glow'
              }`}
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>Casting spell...</span>
                </div>
              ) : (
                <span className="flex items-center justify-center space-x-2">
                  <SparklesIcon className="w-5 h-5" />
                  <span>{isSignUp ? 'Join the Academy' : 'Enter Hogwarts'}</span>
                </span>
              )}
            </motion.button>
          </form>

          {/* Toggle between Sign In/Sign Up */}
          <div className="mt-6 text-center">
            <p className="text-white/60 mb-3">
              {isSignUp ? 'Already have an account?' : "Don't have an account?"}
            </p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => {
                setIsSignUp(!isSignUp);
                setFormData({ name: '', email: '', password: '', confirmPassword: '' });
              }}
              className="text-gold hover:text-amber-400 font-medium transition-colors"
            >
              {isSignUp ? 'Sign In Instead' : 'Create Account'}
            </motion.button>
          </div>
        </motion.div>

        {/* Footer */}
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 1 }}
          className="text-center text-white/50 text-sm mt-8"
        >
          By continuing, you agree to the magical terms of Hogwarts Academy
        </motion.p>
      </div>

      {/* Magical transition particles */}
      {isLoading && (
        <div className="fixed inset-0 pointer-events-none">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ 
                opacity: [0, 1, 0],
                scale: [0, 1, 0],
                y: [0, -100],
                x: [0, Math.sin(i) * 50]
              }}
              transition={{ 
                duration: 2,
                repeat: Infinity,
                delay: i * 0.1
              }}
              className="absolute w-2 h-2 bg-gold rounded-full"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${80 + Math.random() * 20}%`,
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Auth;