import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { XMarkIcon } from '@heroicons/react/24/outline';

interface MagicModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

const MagicModal: React.FC<MagicModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md'
}) => {
  const sizes = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl'
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
          />

          {/* Modal */}
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div
              initial={{ scale: 0.8, opacity: 0, y: 50 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.8, opacity: 0, y: 50 }}
              transition={{ type: "spring", damping: 20, stiffness: 300 }}
              className={`
                relative w-full ${sizes[size]} bg-gradient-to-br from-slate-800/95 to-slate-900/95 
                rounded-xl border border-gold/20 backdrop-blur-md shadow-2xl magical-glow
              `}
            >
              {/* Header */}
              {title && (
                <div className="flex items-center justify-between p-6 border-b border-gold/20">
                  <h2 className="text-2xl font-['Cormorant_Garamond'] font-bold text-parchment">
                    {title}
                  </h2>
                  <motion.button
                    whileHover={{ scale: 1.1, rotate: 90 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={onClose}
                    className="p-2 rounded-full bg-slate-700/50 hover:bg-slate-600/50 text-parchment/70 hover:text-parchment transition-colors"
                  >
                    <XMarkIcon className="w-5 h-5" />
                  </motion.button>
                </div>
              )}

              {/* Content */}
              <div className="p-6">
                {children}
              </div>

              {/* Magical border effect */}
              <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-gold/0 via-gold/10 to-gold/0 opacity-0 hover:opacity-100 transition-opacity duration-500 pointer-events-none" />

              {/* Floating particles */}
              {[...Array(6)].map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute w-1 h-1 bg-gold rounded-full opacity-60"
                  animate={{
                    y: [0, -20, 0],
                    opacity: [0.6, 1, 0.6],
                    scale: [0.8, 1.2, 0.8]
                  }}
                  transition={{
                    duration: 3 + Math.random() * 2,
                    repeat: Infinity,
                    delay: i * 0.5
                  }}
                  style={{
                    left: `${10 + i * 15}%`,
                    top: `${10 + Math.sin(i) * 10}%`,
                  }}
                />
              ))}
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
};

export default MagicModal;