import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { CheckCircleIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

interface CompareResult {
  source_id: number;
  title: string;
  url: string;
  bias: {
    bias_score: number;
    indicators: string[];
    level: string;
    recommendations: string[];
  };
  credibility: {
    credibility_score: number;
    level: string;
    negative_indicators: string[];
    positive_indicators: string[];
    source_quality_assessment: {
      academic_language: boolean;
      balanced_perspective: boolean;
      has_citations: boolean;
      recent_information: boolean;
    };
  };
  summary: {
    success: boolean;
    summary_method: string;
    summary_text: string;
    word_count: number;
  };
  themes: {
    academic_disciplines: string[];
    complexity_level: string;
    content_categories: string[];
    primary_keywords: string[];
    secondary_keywords: string[];
  };
}

interface InputData {
  title: string;
  url: string;
  text: string;
}

const Source: React.FC = () => {
  const [inputs, setInputs] = useState<InputData[]>([
    { title: '', url: '', text: '' },
    { title: '', url: '', text: '' },
  ]);
  
  const [isChecking, setIsChecking] = useState(false);
  const [results, setResults] = useState<CompareResult[]>([]);

  const handleInputChange = (index: number, field: keyof InputData, value: string) => {
    const updated = [...inputs];
    updated[index][field] = value;
    setInputs(updated);
  };

  const allInputsFilled = inputs.every(input => input.title && input.url && input.text);

  const handleCheck = async () => {
    if (!allInputsFilled) return;

    setIsChecking(true);

    // Prepare the request payload
    const payload = {
      sources: inputs.map(input => ({
        title: input.title,
        url: input.url,
        text: input.text,
      })),
    };

    try {
      // Send POST request to backend
      const response = await fetch('http://localhost:5000/api/library/compare-sources', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();
      setResults(data);  // Update the results state with the response

      // Reset input fields
      setInputs([{ title: '', url: '', text: '' }, { title: '', url: '', text: '' }]);
    } catch (error) {
      console.error('Error fetching comparison results:', error);
    } finally {
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
              "Knowledge is power" – Compare your text with known sources
            </p>
          </motion.div>

          <motion.div
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-8 border border-red-400/20 backdrop-blur-sm mb-8"
          >
            <h2 className="text-2xl font-['Cormorant_Garamond'] text-red-300 mb-6 flex items-center space-x-2">
              <MagnifyingGlassIcon className="w-6 h-6" />
              <span>Source Comparison Spell</span>
            </h2>

            <div className="space-y-6">
              {inputs.map((input, index) => (
                <div key={index} className="space-y-4">
                  <h3 className="text-lg text-parchment/70 mb-2">Input {index + 1}</h3>

                  <div>
                    <label className="block text-parchment/70 mb-1">Title:</label>
                    <input
                      type="text"
                      value={input.title}
                      onChange={(e) => handleInputChange(index, 'title', e.target.value)}
                      placeholder="Enter title..."
                      className="w-full p-3 bg-slate-700/50 border border-red-400/20 rounded-lg text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-red-400/50 focus:border-red-400/50 transition-colors"
                    />
                  </div>

                  <div>
                    <label className="block text-parchment/70 mb-1">URL:</label>
                    <input
                      type="url"
                      value={input.url}
                      onChange={(e) => handleInputChange(index, 'url', e.target.value)}
                      placeholder="Enter URL..."
                      className="w-full p-3 bg-slate-700/50 border border-red-400/20 rounded-lg text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-red-400/50 focus:border-red-400/50 transition-colors"
                    />
                  </div>

                  <div>
                    <label className="block text-parchment/70 mb-1">Text:</label>
                    <textarea
                      value={input.text}
                      onChange={(e) => handleInputChange(index, 'text', e.target.value)}
                      placeholder="Paste your text here to compare with sources..."
                      rows={4}
                      className="w-full p-3 bg-slate-700/50 border border-red-400/20 rounded-lg text-parchment placeholder-parchment/50 resize-none focus:outline-none focus:ring-2 focus:ring-red-400/50 focus:border-red-400/50 transition-colors"
                    />
                  </div>
                </div>
              ))}

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleCheck}
                disabled={!allInputsFilled || isChecking}
                className={`w-full py-4 rounded-lg font-medium transition-all duration-300 ${allInputsFilled && !isChecking
                  ? 'bg-gradient-to-r from-red-600 to-red-700 text-white hover:from-red-500 hover:to-red-600 shadow-lg'
                  : 'bg-slate-700/50 text-parchment/50 cursor-not-allowed'
                  }`}
              >
                <span className="flex items-center justify-center space-x-2">
                  <MagnifyingGlassIcon className="w-5 h-5" />
                  <span>
                    {isChecking ? 'Consulting the Ancient Archives...' : 'Compare Sources'}
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
                    Searching through known sources for matches...
                  </p>
                </motion.div>
              )}
            </div>
          </motion.div>

          {results.map((result, index) => {
            const credibilityScore = result?.credibility?.credibility_score ?? 0;
            const credibilityLevel = credibilityScore > 90 ? 'High' : 'Moderate';

            const biasScore = result?.bias?.bias_score ?? 0;
            const biasLevel = biasScore < 40 ? 'Low' : biasScore < 60 ? 'Moderate' : 'High';

            const complexityLevels = ['Easy', 'Intermediate', 'Advanced'];
            const complexityLevel = complexityLevels[Math.floor(Math.random() * complexityLevels.length)];

            return (
              <motion.div
                key={result.source_id}
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
                        Source Comparison Complete
                      </h3>
                      <span className="px-3 py-1 rounded-full text-sm bg-purple-600/30 text-purple-300">
                        {credibilityScore}% confidence
                      </span>
                    </div>

                    <p className="text-parchment/80 mb-3">
                      "{result?.summary?.summary_text ?? 'Summary unavailable'}"
                    </p>

                    <div className="text-sm text-parchment/60 mb-2">
                      <span className="font-medium">Matched Sources:</span>
                      <ul className="list-disc list-inside mt-1">
                        {result?.themes?.primary_keywords?.map((source, i) => (
                          <li key={i}>{source}</li>
                        )) || 'No sources matched'}
                      </ul>
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-xs text-parchment/70 mt-4">
                      <div>
                        <span className="font-medium">Credibility Score:</span> {credibilityScore}
                      </div>
                      <div>
                        <span className="font-medium">Bias Level:</span> {biasLevel}
                      </div>
                    </div>

                    <div className="text-xs text-parchment/50 mt-3">
                      Compared on {new Date(result?.summary?.summary_method ?? 'N/A').toLocaleString()}
                    </div>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default Source;
