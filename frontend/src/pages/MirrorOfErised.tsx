import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { HeartIcon, StarIcon, XCircleIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

// --- Interfaces for State and API Responses ---

interface QuoteState {
  quote: string;
  author: string;
  theme?: string;
  application?: string;
  house_wisdom?: string;
  reflection_prompt?: string;
}

interface CustomQuote {
  id: number;
  goal: string;
  quote: string;
  insight: string;
}

type QuoteMode = 'daily' | 'themed' | 'personalized';

const MirrorOfErised: React.FC = () => {
  const [quoteState, setQuoteState] = useState<QuoteState>({ quote: "The mirror is waking...", author: "Whispers in the frame" });
  const [isLoadingQuote, setIsLoadingQuote] = useState(true);
  const [quoteError, setQuoteError] = useState<string | null>(null);
  const [quoteMode, setQuoteMode] = useState<QuoteMode>('daily');
  
  // State for themed quotes
  const [availableThemes, setAvailableThemes] = useState<string[]>([]);
  const [selectedTheme, setSelectedTheme] = useState('courage');

  // State for personalized quotes
  const [selectedMood, setSelectedMood] = useState('anxious');
  const [selectedHouse, setSelectedHouse] = useState('ravenclaw');
  
  // State for custom quotes (Heart's Desires)
  const [customQuotes, setCustomQuotes] = useState<CustomQuote[]>([]);
  const [newGoal, setNewGoal] = useState('');
  const [showAddGoal, setShowAddGoal] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  const navigate = useNavigate();

  // --- API Fetching Functions ---

  const fetchQuote = async (url: string) => {
    setIsLoadingQuote(true);
    setQuoteError(null);
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error("The mirror's reflection is clouded right now.");
      const data = await response.json();
      if (!data.success) throw new Error(data.error || "A mysterious interference occurred.");
      return data;
    } catch (err: any) {
      setQuoteError(err.message);
    } finally {
      setIsLoadingQuote(false);
    }
  };

  const fetchDailyQuote = async () => {
    const data = await fetchQuote('http://localhost:5000/api/erised/daily');
    if (data) {
      setQuoteState({
        quote: data.quote,
        author: data.author,
        theme: data.theme,
        reflection_prompt: data.reflection_prompt,
      });
    }
  };

  const fetchThemedQuote = async (theme: string) => {
    const data = await fetchQuote(`http://localhost:5000/api/erised/themed?theme=${theme}&limit=1`);
    if (data && data.quotes.length > 0) {
      setQuoteState({
        quote: data.quotes[0].text,
        author: data.quotes[0].author,
        theme: data.theme,
      });
    }
  };

  const fetchPersonalizedQuote = async () => {
    const params = new URLSearchParams({ mood: selectedMood, context: 'personal growth', house: selectedHouse });
    const data = await fetchQuote(`http://localhost:5000/api/erised/quote?${params}`);
    if (data) {
        // The personalized quote is often a long string with explanation, so we just use that.
        setQuoteState({ quote: data.quote, author: `Wisdom for a ${data.house}` });
    }
  };
  
  // Fetch initial data on load
  useEffect(() => {
    fetchDailyQuote();
    // Fetch available themes for the dropdown
    const getThemes = async () => {
        const data = await fetchQuote('http://localhost:5000/api/erised/themed?theme=courage');
        if (data?.available_themes) setAvailableThemes(data.available_themes);
    };
    getThemes();
  }, []);

  // Handler for custom quote generation
  const handleGenerateCustomQuote = async () => {
    if (!newGoal.trim()) return;
    setIsGenerating(true);
    setQuoteError(null);
    try {
        const response = await fetch('http://localhost:5000/api/erised/custom', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ situation: newGoal, goal: newGoal, challenge: 'overcoming self-doubt', style: 'inspiring' })
        });
        if (!response.ok) throw new Error("The mirror couldn't quite grasp that desire.");
        const data = await response.json();
        if (data.success) {
            setCustomQuotes(prev => [...prev, { id: Date.now(), goal: newGoal, quote: data.quote, insight: data.mirror_insight }]);
            setNewGoal('');
            setShowAddGoal(false);
        } else {
            throw new Error(data.error || 'An unknown error occurred.');
        }
    } catch(err: any) {
        setQuoteError(err.message);
    } finally {
        setIsGenerating(false);
    }
  };

  const removeGoal = (id: number) => {
    setCustomQuotes(customQuotes.filter((cq) => cq.id !== id));
  };
  
  return (
    <div 
      className="min-h-screen"
      style={{
        backgroundImage: `url('/images/mirror.jpeg')`,
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
          <button onClick={() => navigate(-1)} className="absolute top-6 right-6 bg-rose-600/60 hover:bg-rose-500 text-parchment px-4 py-2 rounded-md border border-slate-500/50 shadow-md transition">Back</button>
          {/* Header */}
          <motion.div initial={{ y: -50, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.8 }} className="text-center mb-12">
            <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-violet-400 to-purple-400 mb-4">Mirror of Erised</h1>
            <p className="text-white/80 text-lg mb-8">"I show not your face but your heart's desire"</p>
          </motion.div>

          {/* Mirror */}
          <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 1, delay: 0.3 }} className="relative mx-auto mb-12">
            <div className="relative max-w-2xl mx-auto">
              <div className="relative bg-gradient-to-br from-amber-600 via-yellow-600 to-amber-700 p-8 rounded-t-full rounded-b-lg shadow-2xl">
                <div className="absolute top-4 left-1/2 transform -translate-x-1/2 w-16 h-4 bg-gradient-to-r from-gold to-amber-500 rounded-full opacity-80" />
                <div className="absolute top-8 left-8 w-6 h-6 bg-gold rounded-full opacity-60" />
                <div className="absolute top-8 right-8 w-6 h-6 bg-gold rounded-full opacity-60" />
                
                <div className="relative bg-gradient-to-br from-slate-800/60 via-purple-900/40 to-slate-800/60 rounded-t-full rounded-b-lg p-8 border-4 border-silver/30 backdrop-blur-sm min-h-96 flex flex-col items-center justify-center overflow-hidden">
                  <motion.div animate={{ opacity: [0.3, 0.7, 0.3], scale: [1, 1.1, 1] }} transition={{ duration: 4, repeat: Infinity }} className="absolute inset-0 bg-gradient-to-br from-purple-400/10 via-violet-400/20 to-purple-400/10 rounded-t-full rounded-b-lg"/>
                  <AnimatePresence mode="wait">
                    <motion.div key={quoteState.quote} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }} transition={{ duration: 0.7 }} className="text-center z-10 relative">
                      {isLoadingQuote ? (
                        <div className="w-12 h-12 mx-auto border-4 border-purple-400/30 border-t-purple-400 rounded-full animate-spin" />
                      ) : quoteError ? (
                          <div className="p-4 text-red-300 bg-red-800/30 border border-red-500/50 rounded-md flex items-center gap-2 max-w-sm mx-auto">
                              <XCircleIcon className="w-6 h-6" /> {quoteError}
                          </div>
                      ) : (
                        <>
                          <blockquote className="text-xl md:text-2xl font-['Cormorant_Garamond'] text-white leading-relaxed italic text-center max-w-lg">"{quoteState.quote}"</blockquote>
                          <div className="mt-6 text-purple-300 text-sm">— {quoteState.author}</div>
                        </>
                      )}
                    </motion.div>
                  </AnimatePresence>
                  {[...Array(12)].map((_, i) => (<motion.div key={i} className="absolute w-1 h-1 bg-purple-400 rounded-full" animate={{ y: [0, -20, 0], x: [0, Math.sin(i) * 20, 0], opacity: [0, 1, 0], scale: [0, 1, 0] }} transition={{ duration: 3 + Math.random() * 2, repeat: Infinity, delay: i * 0.3 }} style={{ left: `${20 + (i * 7)}%`, top: `${30 + Math.sin(i) * 30}%` }}/>))}
                </div>
                <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 bg-amber-700 px-6 py-2 rounded-lg border-2 border-gold"><div className="text-xs text-gold font-['Cormorant_Garamond'] text-center">Erised stra ehru oyt ube cafru oyt on wohsi</div></div>
              </div>
            </div>
          </motion.div>

          {/* --- Quote Controls --- */}
          <motion.div initial={{ y: 50, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.8, delay: 0.4 }} className="bg-gradient-to-br from-slate-800/80 to-slate-900/90 rounded-xl p-6 border border-purple-400/20 backdrop-blur-sm mb-12">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Mode Selection */}
                  <div className="md:col-span-3 flex justify-center gap-2 mb-4">
                      {(['daily', 'themed', 'personalized'] as QuoteMode[]).map(mode => (
                          <button key={mode} onClick={() => setQuoteMode(mode)} className={`px-4 py-2 text-sm rounded-lg transition-colors capitalize ${quoteMode === mode ? 'bg-purple-600 text-white shadow-lg' : 'bg-slate-700/50 text-white/80 hover:bg-slate-700'}`}>{mode === 'daily' ? 'Daily Wisdom' : mode === 'themed' ? 'Themed Reflection' : 'Personalized Guidance'}</button>
                      ))}
                  </div>
                  {/* Dynamic Controls based on Mode */}
                  {quoteMode === 'themed' && (<>
                      <select value={selectedTheme} onChange={e => setSelectedTheme(e.target.value)} className="w-full p-3 bg-slate-700/70 border border-purple-400/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-400/50 capitalize"><option value="">Select Theme</option>{availableThemes.map(t => <option key={t} value={t}>{t}</option>)}</select>
                      <button onClick={() => fetchThemedQuote(selectedTheme)} disabled={isLoadingQuote} className="md:col-span-2 w-full py-3 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-lg hover:opacity-90 transition-opacity font-medium disabled:opacity-50">Show Themed Quote</button>
                  </>)}
                  {quoteMode === 'personalized' && (<>
                      <select value={selectedMood} onChange={e => setSelectedMood(e.target.value)} className="w-full p-3 bg-slate-700/70 border border-purple-400/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-400/50 capitalize"><option value="anxious">Anxious</option><option value="sad">Sad</option><option value="unmotivated">Unmotivated</option><option value="stressed">Stressed</option></select>
                      <select value={selectedHouse} onChange={e => setSelectedHouse(e.target.value)} className="w-full p-3 bg-slate-700/70 border border-purple-400/20 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-purple-400/50 capitalize"><option value="ravenclaw">Ravenclaw</option><option value="gryffindor">Gryffindor</option><option value="hufflepuff">Hufflepuff</option><option value="slytherin">Slytherin</option></select>
                      <button onClick={fetchPersonalizedQuote} disabled={isLoadingQuote} className="w-full py-3 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-lg hover:opacity-90 transition-opacity font-medium disabled:opacity-50">Get Personal Quote</button>
                  </>)}
                   {quoteMode === 'daily' && (<div className="md:col-span-3 text-center"><button onClick={fetchDailyQuote} disabled={isLoadingQuote} className="py-3 px-6 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-lg hover:opacity-90 transition-opacity font-medium disabled:opacity-50">Refresh Daily Quote</button></div>)}
              </div>
          </motion.div>

          {/* Your Heart's Desires Section */}
          <motion.div initial={{ y: 50, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.8, delay: 0.6 }} className="bg-gradient-to-br from-slate-800/80 to-slate-900/90 rounded-xl p-8 border border-purple-400/20 backdrop-blur-sm">
            <div className="text-center mb-8"><h2 className="text-2xl font-['Cormorant_Garamond'] text-purple-300 mb-4 flex items-center justify-center space-x-2"><HeartIcon className="w-6 h-6" /><span>Generate Personal Insight</span></h2><p className="text-white/80">What does your heart truly desire? The mirror will offer its wisdom.</p></div>
            {customQuotes.length > 0 && (
              <div className="space-y-4 mb-6">
                {customQuotes.map((cq) => (
                  <motion.div key={cq.id} initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 0.5 }} className="group relative bg-gradient-to-br from-purple-900/30 to-violet-900/30 p-4 rounded-lg border border-purple-400/20">
                      <p className="text-white font-semibold leading-relaxed pr-8">Your Desire: <span className="font-normal italic">"{cq.goal}"</span></p>
                      <hr className="my-3 border-purple-400/20" />
                      <p className="text-purple-200 text-sm leading-relaxed"><strong>Mirror's Insight:</strong> {cq.insight}</p>
                      <p className="text-white/80 text-sm mt-2 italic">"{cq.quote}"</p>
                    <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }} onClick={() => removeGoal(cq.id)} className="absolute top-2 right-2 w-6 h-6 bg-red-600/20 hover:bg-red-600/40 rounded-full flex items-center justify-center text-red-400 opacity-0 group-hover:opacity-100 transition-opacity">×</motion.button>
                  </motion.div>
                ))}
              </div>
            )}
            {showAddGoal ? (
              <motion.div initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="space-y-4">
                <textarea value={newGoal} onChange={(e) => setNewGoal(e.target.value)} placeholder="Describe your goal, dream, or challenge..." rows={3} className="w-full p-4 bg-slate-700/70 border border-purple-400/20 rounded-lg text-white placeholder-white/50 resize-none focus:outline-none focus:ring-2 focus:ring-purple-400/50" autoFocus />
                {quoteError && <div className="p-3 text-sm text-red-300 bg-red-800/30 border border-red-500/50 rounded-md flex items-center gap-2"><XCircleIcon className="w-5 h-5" />{quoteError}</div>}
                <div className="flex space-x-3">
                  <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={handleGenerateCustomQuote} disabled={isGenerating} className="px-6 py-2 bg-gradient-to-r from-purple-600 to-violet-600 text-white rounded-lg hover:from-purple-500 hover:to-violet-500 transition-colors shadow-lg disabled:opacity-50">{isGenerating ? 'Generating...' : 'Reveal Insight'}</motion.button>
                  <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={() => setShowAddGoal(false)} className="px-6 py-2 bg-slate-700/50 text-white/70 rounded-lg border border-slate-600/50 hover:border-slate-500/50 transition-colors">Cancel</motion.button>
                </div>
              </motion.div>
            ) : (
              <div className="text-center">
                <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={() => setShowAddGoal(true)} className="inline-flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-purple-600/20 to-violet-600/20 text-purple-300 border border-purple-400/30 rounded-lg hover:border-purple-400/50 transition-colors shadow-lg"><HeartIcon className="w-5 h-5" /><span>Reveal a New Desire</span></motion.button>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default MirrorOfErised;