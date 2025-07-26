import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ExclamationTriangleIcon, CheckCircleIcon, MagnifyingGlassIcon, XCircleIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

// Updated interface to match the backend API response
interface ResearchResult {
  id: number;
  topic: string;
  level: string;
  type: string;
  ethical_considerations: string[];
  methodology_guidance: string;
  recommended_sources: string;
  research_timeline: string;
  suggested_research_questions: string;
  timestamp: Date;
}

const Research: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [level, setLevel] = useState('undergraduate'); // Default to undergraduate
  const [type, setType] = useState('general'); // Default to general
  const [isChecking, setIsChecking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<ResearchResult[]>([]);
  const navigate = useNavigate();

  const handleCheck = async () => {
    if (!topic.trim() || !type.trim()) return;

    setIsChecking(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/api/library/research-assistant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic, level, type }),
      });

      if (!response.ok) {
        throw new Error(`The ancient texts are unreadable. Please try again later. (HTTP ${response.status})`);
      }

      const data = await response.json();

      if (data.success) {
        const newResult: ResearchResult = {
          id: Date.now(),
          topic: data.topic,
          level: data.research_level,
          type: data.research_type,
          ethical_considerations: data.ethical_considerations || [],
          methodology_guidance: data.methodology_guidance,
          recommended_sources: data.recommended_sources,
          research_timeline: data.research_timeline,
          suggested_research_questions: data.suggested_research_questions,
          timestamp: new Date(),
        };

        setResults([newResult, ...results]);
        // Reset form
        setTopic('');
        setType('general');
        setLevel('undergraduate');
      } else {
        throw new Error(data.error || "An unknown error occurred while consulting the archives.");
      }

    } catch (err: any) {
      setError(err.message || 'A network error occurred. Please check your connection.');
    } finally {
      setIsChecking(false);
    }
  };


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
              "Those who cannot remember the past are condemned to repeat it" - Research Assistant
            </p>
          </motion.div>

          {/* Research Assistant Input */}
          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-8 border border-red-400/20 backdrop-blur-sm mb-8"
          >
            <h2 className="text-2xl font-['Cormorant_Garamond'] text-red-300 mb-6 flex items-center space-x-2">
              <MagnifyingGlassIcon className="w-6 h-6" />
              <span>Research Assistance Spell</span>
            </h2>

            <div className="space-y-6">
              <div>
                <label className="block text-parchment/70 mb-3">Topic:</label>
                <input
                  type="text"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  placeholder="Enter research topic..."
                  className="w-full p-4 bg-slate-700/50 border border-red-400/20 rounded-lg text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-red-400/50 transition-colors"
                />
              </div>

              <div>
                <label className="block text-parchment/70 mb-3">Level:</label>
                <select
                  value={level}
                  onChange={(e) => setLevel(e.target.value)}
                  className="w-full p-4 bg-slate-700/50 border border-red-400/20 rounded-lg text-parchment focus:outline-none focus:ring-2 focus:ring-red-400/50 transition-colors"
                >
                  <option value="undergraduate">Undergraduate</option>
                  <option value="graduate">Graduate</option>
                  <option value="professional">Professional</option>
                </select>
              </div>

              <div>
                <label className="block text-parchment/70 mb-3">Type:</label>
                <select
                  value={type}
                  onChange={(e) => setType(e.target.value)}
                  className="w-full p-4 bg-slate-700/50 border border-red-400/20 rounded-lg text-parchment focus:outline-none focus:ring-2 focus:ring-red-400/50 transition-colors"
                >
                  <option value="general">General</option>
                  <option value="literature_review">Literature Review</option>
                  <option value="empirical">Empirical</option>
                  <option value="theoretical">Theoretical</option>
                </select>
              </div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleCheck}
                disabled={!topic.trim() || !type.trim() || isChecking}
                className={`w-full py-4 rounded-lg font-medium transition-all duration-300 ${
                  topic.trim() && type.trim() && !isChecking
                    ? 'bg-gradient-to-r from-red-600 to-red-700 text-white hover:from-red-500 hover:to-red-600 shadow-lg'
                    : 'bg-slate-700/50 text-parchment/50 cursor-not-allowed'
                }`}
              >
                <span className="flex items-center justify-center space-x-2">
                  <ExclamationTriangleIcon className="w-5 h-5" />
                  <span>{isChecking ? 'Consulting the Ancient Texts...' : 'Generate Research Plan'}</span>
                </span>
              </motion.button>
              
              {/* --- Loading Spinner --- */}
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
                    Consulting archives and scholars for your research...
                  </p>
                </motion.div>
              )}
              {/* --- Error Message --- */}
              {error && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-red-900/50 border border-red-500 text-red-300 px-4 py-3 rounded-lg flex items-center space-x-3"
                >
                  <XCircleIcon className="w-6 h-6" />
                  <span>{error}</span>
                </motion.div>
              )}
            </div>
          </motion.div>

          {/* --- Results Display --- */}
          {results.length > 0 && (
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ duration: 0.8 }}
              className="space-y-4"
            >
              <h2 className="text-xl font-['Cormorant_Garamond'] text-parchment mb-6">
                Research Plan Results
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
                    <div className="w-12 h-12 rounded-full flex-shrink-0 flex items-center justify-center bg-purple-600">
                      <CheckCircleIcon className="w-6 h-6 text-white" />
                    </div>

                    <div className="flex-1 space-y-6">
                      <h3 className="font-medium text-purple-300">
                        Research Plan for "{result.topic}" (Level: {result.level}, Type: {result.type})
                      </h3>

                      {/* Render each section from the API response */}
                      <ResultSection title="Suggested Research Questions">
                        <div className="text-parchment/70 whitespace-pre-wrap">{result.suggested_research_questions}</div>
                      </ResultSection>
                      
                      <ResultSection title="Methodology Guidance">
                        <div className="text-parchment/70 whitespace-pre-wrap">{result.methodology_guidance}</div>
                      </ResultSection>

                      <ResultSection title="Recommended Sources">
                         <div className="text-parchment/70 whitespace-pre-wrap">{result.recommended_sources}</div>
                      </ResultSection>
                      
                      <ResultSection title="Research Timeline">
                        <div className="text-parchment/70 whitespace-pre-wrap">{result.research_timeline}</div>
                      </ResultSection>

                      <ResultSection title="Ethical Considerations">
                        <ul className="list-disc list-inside text-parchment/70">
                          {result.ethical_considerations.map((item, i) => (
                            <li key={i}>{item}</li>
                          ))}
                        </ul>
                      </ResultSection>

                      <div className="text-xs text-parchment/50 mt-3 pt-4 border-t border-purple-400/20">
                        Generated on {result.timestamp.toLocaleString()}
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

// Helper component for consistent section styling
const ResultSection: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
  <div>
    <p className="text-parchment/80 mb-2 font-semibold">{title}:</p>
    {children}
  </div>
);


export default Research;