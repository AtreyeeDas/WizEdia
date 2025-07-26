import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PlusIcon, EyeIcon, SparklesIcon, XCircleIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

type Mood = 'happy' | 'sad' | 'excited' | 'thoughtful' | 'grateful' | 'anger' | 'fear';

interface Memory {
  id: number;
  title: string;
  content: string;
  mood: Mood;
  date: Date;
  emotion: string;
  magicalInsight: string; // New field from API
}

const Pensieve: React.FC = () => {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [isWriting, setIsWriting] = useState(false);
  const [isSaving, setIsSaving] = useState(false); // For loading state
  const [error, setError] = useState<string | null>(null); // For error handling
  const [newMemory, setNewMemory] = useState({ title: '', content: '' });

  const navigate = useNavigate();

  // Maps API emotion to a valid Mood type for styling
  const mapEmotionToMood = (emotion: string): Mood => {
    const lowerEmotion = emotion.toLowerCase();
    switch (lowerEmotion) {
      case 'joy':
      case 'love':
        return 'happy';
      case 'sadness':
        return 'sad';
      case 'surprise':
        return 'excited';
      case 'anger':
        return 'anger';
      case 'fear':
        return 'fear';
      default:
        return 'thoughtful';
    }
  };

  const handleSaveMemory = async () => {
    if (!newMemory.title || !newMemory.content) return;

    setIsSaving(true);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/pensieve/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: newMemory.content }),
      });

      if (!response.ok) {
        throw new Error(`The Pensieve is cloudy... please try again. (HTTP ${response.status})`);
      }

      const data = await response.json();

      if (data.success) {
        const memory: Memory = {
          id: Date.now(),
          title: newMemory.title,
          content: newMemory.content,
          emotion: data.primary_emotion,
          mood: mapEmotionToMood(data.primary_emotion),
          magicalInsight: data.magical_insight,
          date: new Date(),
        };

        setMemories([memory, ...memories]);
        setNewMemory({ title: '', content: '' }); // Reset form
        setIsWriting(false); // Close modal
      } else {
        throw new Error(data.error || "An unknown magical interference occurred.");
      }

    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsSaving(false);
    }
  };

  const moodColors: Record<Mood, string> = {
    happy: 'from-yellow-400 to-orange-500',
    sad: 'from-blue-400 to-indigo-600',
    excited: 'from-pink-400 to-red-500',
    thoughtful: 'from-purple-400 to-indigo-600',
    grateful: 'from-green-400 to-emerald-600',
    anger: 'from-red-500 to-red-700',
    fear: 'from-gray-500 to-gray-700',
  };

  const moodEmojis: Record<Mood, string> = {
    happy: '😊',
    sad: '😢',
    excited: '🌟',
    thoughtful: '🤔',
    grateful: '🙏',
    anger: '😠',
    fear: '😨',
  };

  const isSaveDisabled = !newMemory.title || !newMemory.content || isSaving;

  return (
    <div className="min-h-screen p-8">
      <Navbar />
      <button
        onClick={() => navigate(-1)}
        className="absolute top-6 right-6 bg-rose-600/60 hover:bg-rose-500 text-parchment px-4 py-2 rounded-md border border-slate-500/50 shadow-md transition"
      >
        Back
      </button>

      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-silver via-gray-300 to-silver mb-4">
            Pensieve of Memories
          </h1>
          <p className="text-parchment/70 text-lg mb-8">
            Store your thoughts and reflections in this ancient pensieve
          </p>
        </motion.div>


        {/* Pensieve Bowl */}
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 1, delay: 0.3 }}
            className="relative mx-auto w-48 h-32 mb-8"
          >
            <div className="relative w-full h-full">
              <div className="absolute inset-0 bg-gradient-to-b from-silver/20 to-silver/40 rounded-full border-4 border-silver/30 shadow-2xl">
                <motion.div animate={{ rotate: 360 }} transition={{ duration: 20, repeat: Infinity, ease: "linear" }} className="absolute inset-4 bg-gradient-to-r from-blue-400/20 via-purple-400/20 to-silver/20 rounded-full blur-sm" />
                <motion.div animate={{ rotate: -360 }} transition={{ duration: 15, repeat: Infinity, ease: "linear" }} className="absolute inset-6 bg-gradient-to-r from-silver/30 via-blue-300/20 to-purple-300/20 rounded-full blur-sm" />
              </div>
              
              {memories.slice(0, 3).map((memory, index) => (
                <motion.div
                  key={memory.id}
                  animate={{ y: [0, -10, 0], opacity: [0.5, 1, 0.5] }}
                  transition={{ duration: 3, repeat: Infinity, delay: index * 1 }}
                  className="absolute w-2 h-2 bg-silver rounded-full"
                  style={{
                    left: `${30 + index * 20}%`,
                    top: `${40 + Math.sin(index) * 20}%`,
                  }}
                />
              ))}
            </div>
          </motion.div>

        {/* Add Memory Button */}
        <div className="text-center mb-8 z-50 relative">
          <button
            type="button"
            onClick={() => {
              setNewMemory({ title: '', content: '', mood: 'thoughtful' });
              setIsWriting(true);
            }}
            className="inline-flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-silver/20 to-gray-600/20 text-parchment border border-silver/30 rounded-lg hover:border-silver/50 transition-colors shadow-lg"
          >
            <PlusIcon className="w-5 h-5" />
            <span>Add New Memory</span>
          </button>
        </div>

        {/* Modal Popup */}
        <AnimatePresence>
          {isWriting && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
              onClick={() => setIsWriting(false)}
            >
              <motion.div
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0.8 }}
                className="bg-gradient-to-br from-slate-800/80 to-slate-900/90 rounded-xl p-6 border border-silver/20 backdrop-blur-sm w-full max-w-md"
                onClick={(e) => e.stopPropagation()} // Prevent closing modal when clicking inside
              >
                <h3 className="text-xl font-['Cormorant_Garamond'] text-silver mb-6 text-center">
                  Capture a New Memory
                </h3>

                <div className="space-y-4">
                  <input
                    type="text"
                    placeholder="Memory title..."
                    value={newMemory.title}
                    onChange={(e) => setNewMemory({ ...newMemory, title: e.target.value })}
                    className="w-full p-3 bg-slate-700/50 border border-silver/20 rounded-lg text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-silver/50"
                  />

                  <textarea
                    placeholder="Describe your memory in detail..."
                    value={newMemory.content}
                    onChange={(e) => setNewMemory({ ...newMemory, content: e.target.value })}
                    rows={5}
                    className="w-full p-3 bg-slate-700/50 border border-silver/20 rounded-lg text-parchment placeholder-parchment/50 resize-none focus:outline-none focus:ring-2 focus:ring-silver/50"
                  />
                  
                  {error && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="bg-red-900/50 border border-red-500 text-red-300 px-4 py-3 rounded-lg flex items-center space-x-3 text-sm"
                    >
                      <XCircleIcon className="w-5 h-5 flex-shrink-0" />
                      <span>{error}</span>
                    </motion.div>
                  )}

                  <div className="flex space-x-3 pt-4">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleSaveMemory}
                      disabled={isSaveDisabled}
                      className={`flex-1 px-6 py-2 text-parchment rounded-lg border transition-colors flex items-center justify-center ${
                        isSaveDisabled
                          ? 'bg-slate-700/50 text-parchment/50 border-slate-600/50 cursor-not-allowed'
                          : 'bg-gradient-to-r from-silver/20 to-gray-600/20 border-silver/30 hover:border-silver/50'
                      }`}
                    >
                      {isSaving ? 'Saving...' : 'Save Memory'}
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => setIsWriting(false)}
                      disabled={isSaving}
                      className="flex-1 px-6 py-2 bg-slate-700/50 text-parchment/70 rounded-lg border border-slate-600/50 hover:border-slate-500/50 transition-colors disabled:cursor-not-allowed"
                    >
                      Cancel
                    </motion.button>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Memories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {memories.map((memory, index) => (
            <motion.div
              key={memory.id}
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ y: -5, scale: 1.02 }}
              className="group relative"
            >
              <div className="bg-gradient-to-br from-slate-800/40 to-slate-900/60 rounded-xl p-6 border border-silver/20 backdrop-blur-sm hover:border-silver/40 transition-all duration-300 h-full flex flex-col">
                <div className="flex items-center justify-between mb-4">
                  <div className={`inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-gradient-to-r ${moodColors[memory.mood]} text-white text-sm`}>
                    <span>{moodEmojis[memory.mood]}</span>
                    <span className="capitalize">{memory.emotion}</span>
                  </div>
                  <span className="text-parchment/50 text-sm">
                    {memory.date.toLocaleDateString()}
                  </span>
                </div>

                <h3 className="text-xl font-['Cormorant_Garamond'] text-parchment mb-3">
                  {memory.title}
                </h3>

                <p className="text-parchment/70 leading-relaxed mb-4 line-clamp-3 flex-grow">
                  {memory.content}
                </p>
                
                {/* Magical Insight Section */}
                <div className="mt-auto pt-4 border-t border-silver/10">
                    <div className="flex items-start space-x-3 text-silver/80">
                        <SparklesIcon className="w-5 h-5 flex-shrink-0 text-silver/60 mt-1" />
                        <div className="flex-1">
                            <p className="font-semibold text-sm">Magical Insight</p>
                            <p className="text-parchment/70 italic">"{memory.magicalInsight}"</p>
                        </div>
                    </div>
                </div>

                <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-silver/0 via-silver/5 to-silver/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Pensieve;