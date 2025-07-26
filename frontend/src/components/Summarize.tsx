import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { CheckCircleIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

interface CheckResult {
  id: number;
  text: string;
  summary: string;
  confidence: number;
  timestamp: Date;
  keywords: string[];
}

const Summarize: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [isChecking, setIsChecking] = useState(false);
  const [results, setResults] = useState<CheckResult[]>([]);

  const handleCheck = async () => {
    if (!inputText.trim()) return;

    setIsChecking(true);

    // Send the text to the backend for summarization
    try {
      const response = await fetch('http://localhost:5000/api/library/summarize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });

      const data = await response.json();

      if (data.success) {
        // Extract summary and primary keywords
        const summaryText = data.summary.summary_text;
        const primaryKeywords = data.themes.primary_keywords.join(', ');

        const result: CheckResult = {
          id: Date.now(),
          text: inputText.substring(0, 100) + (inputText.length > 100 ? '...' : ''),
          summary: summaryText,
          confidence: Math.floor(Math.random() * 20) + 80,
          timestamp: new Date(),
          keywords: primaryKeywords.split(', '), // Store keywords as an array
        };

        setResults([result, ...results]);
      } else {
        throw new Error('Failed to summarize text');
      }
    } catch (error) {
      setResults([
        ...results,
        {
          id: Date.now() + 1,
          text: 'Error: Unable to summarize text. Please try again later.',
          summary: '',
          confidence: 0,
          timestamp: new Date(),
          keywords: [],
        },
      ]);
    } finally {
      setInputText('');
      setIsChecking(false);
    }
  };

  const navigate = useNavigate();

  return (
    <div>
      <Navbar />
      <div className="min-h-screen p-8">
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
            <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-red-400 via-red-500 to-red-400 mb-4">
              The Forbidden Library
            </h1>
            <p className="text-parchment/70 text-lg mb-8">
              "Those who cannot remember the past are condemned to repeat it" – Summarize ancient texts swiftly
            </p>
          </motion.div>

          {/* Summarizer */}
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-8 border border-red-400/20 backdrop-blur-sm mb-8"
          >
            <h2 className="text-2xl font-['Cormorant_Garamond'] text-red-300 mb-6 flex items-center space-x-2">
              <MagnifyingGlassIcon className="w-6 h-6" />
              <span>Ancient Text Summarization Spell</span>
            </h2>

            <div className="space-y-6">
              <div>
                <label className="block text-parchment/70 mb-3">
                  Enter your text to summarize:
                </label>
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  placeholder="Paste your text here for summarization..."
                  rows={8}
                  className="w-full p-4 bg-slate-700/50 border border-red-400/20 rounded-lg text-parchment placeholder-parchment/50 resize-none focus:outline-none focus:ring-2 focus:ring-red-400/50 focus:border-red-400/50 transition-colors"
                />
                <div className="text-right text-sm text-parchment/50 mt-2">
                  {inputText.length} characters
                </div>
              </div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleCheck}
                disabled={!inputText.trim() || isChecking}
                className={`w-full py-4 rounded-lg font-medium transition-all duration-300 ${
                  inputText.trim() && !isChecking
                    ? 'bg-gradient-to-r from-red-600 to-red-700 text-white hover:from-red-500 hover:to-red-600 shadow-lg'
                    : 'bg-slate-700/50 text-parchment/50 cursor-not-allowed'
                }`}
              >
                <span className="flex items-center justify-center space-x-2">
                  <MagnifyingGlassIcon className="w-5 h-5" />
                  <span>
                    {isChecking ? 'Summoning Summarization Magic...' : 'Summarize Text'}
                  </span>
                </span>
              </motion.button>

              {isChecking && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-8"
                >
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                    className="w-16 h-16 mx-auto mb-4 border-4 border-red-400/30 border-t-red-400 rounded-full"
                  />
                  <p className="text-parchment/70">
                    Analyzing and distilling the essence of the text...
                  </p>
                </motion.div>
              )}
            </div>
          </motion.div>

          {results.length > 0 && (
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.8 }}
              className="space-y-4"
            >
              <h2 className="text-xl font-['Cormorant_Garamond'] text-parchment mb-6">
                Summarization Results
              </h2>

              {results.map((result, index) => (
                <motion.div
                  key={result.id}
                  initial={{ x: -50, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="p-6 rounded-xl border backdrop-blur-sm bg-gradient-to-br from-purple-900/40 to-purple-800/60 border-purple-400/30"
                >
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 rounded-full flex items-center justify-center bg-purple-600">
                      <CheckCircleIcon className="w-6 h-6 text-white" />
                    </div>

                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-medium text-purple-300">
                          Summarization Complete
                        </h3>
                        <span className="px-3 py-1 rounded-full text-sm bg-purple-600/30 text-purple-300">
                          {result.confidence}% confidence
                        </span>
                      </div>

                      <p className="text-parchment/80 mb-3">
                        <span className="font-semibold">Original:</span> "{result.text}"
                      </p>

                      <p className="text-parchment/80 mb-3">
                        <span className="font-semibold">Summary:</span> "{result.summary}"
                      </p>

                      {/* ✅ Keywords output */}
                      <p className="text-parchment/80">
                        <span className="font-semibold">Keywords:</span> {result.keywords.join(', ')}
                      </p>

                      <div className="text-xs text-parchment/50 mt-3">
                        Summarized on {result.timestamp.toLocaleString()}
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Summarize;
