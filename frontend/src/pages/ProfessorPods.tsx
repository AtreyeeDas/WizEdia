import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { AcademicCapIcon, XCircleIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

// --- Interfaces for State and API Responses ---

interface Professor {
  id: 'mcgonagall' | 'snape' | 'lupin' | 'hagrid';
  name: string;
  subject: string;
  personality: string;
  avatar: string;
  description: string;
  specialties: string[];
  color: string;
  task: string;
  image: string;
}

// Interfaces for API results, closely matching the backend response
interface McgResults {
  personalized_recommendations: { recommendations: string };
  professor_insights?: { study_strategies: string[] }; // Optional since it's nested
}

interface SnapeResults {
  learning_path: {
    learning_modules: { order: number; topic: string; estimated_duration: string }[];
    total_duration: string;
    weekly_commitment: string;
  };
}

interface LupinResults {
  online_platforms: { name: string; best_for: string }[];
  preparation_tips: string[];
  self_directed_alternatives: { study_techniques: string[] };
}

interface HagridResults {
  tutoring_response: {
    explanation: string;
  };
}

// --- Main Component ---

const ProfessorPods: React.FC = () => {
  const [selectedProfessor, setSelectedProfessor] = useState<Professor | null>(null);
  const [activeProfessor, setActiveProfessor] = useState<string | null>(null);
  const [loadingStates, setLoadingStates] = useState({ mcgonagall: false, snape: false, lupin: false, hagrid: false });
  const [errorStates, setErrorStates] = useState<Record<Professor['id'], string | null>>({ mcgonagall: null, snape: null, lupin: null, hagrid: null });

  // State for each professor's form and results
  const [mcgSubject, setMcgSubject] = useState('');
  const [mcgLevel, setMcgLevel] = useState('intermediate');
  const [mcgLearningStyle, setMcgLearningStyle] = useState('mixed');
  const [mcgResults, setMcgResults] = useState<McgResults | null>(null);

  const [snapeSubject, setSnapeSubject] = useState('');
  const [snapeCurrentLevel, setSnapeCurrentLevel] = useState('beginner');
  const [snapeTargetLevel, setSnapeTargetLevel] = useState('intermediate');
  const [snapeTimeline, setSnapeTimeline] = useState('12 weeks');
  const [snapeResults, setSnapeResults] = useState<SnapeResults | null>(null);

  const [lupinSubject, setLupinSubject] = useState('');
  const [lupinBudget, setLupinBudget] = useState('low');
  const [lupinFormat, setLupinFormat] = useState('online');
  const [lupinResults, setLupinResults] = useState<LupinResults | null>(null);

  const [hagridQuestion, setHagridQuestion] = useState('');
  const [hagridSubject, setHagridSubject] = useState('');
  const [hagridDifficulty, setHagridDifficulty] = useState('intermediate');
  const [hagridLearningStyle, setHagridLearningStyle] = useState('mixed');
  const [hagridResults, setHagridResults] = useState<HagridResults | null>(null);
  
  const navigate = useNavigate();

  const professors: Professor[] = [
    { 
      id: 'mcgonagall', 
      name: 'Professor McGonagall', 
      subject: 'Recommendation Engine', 
      personality: 'Stern but fair, logical thinker', 
      avatar: '🧙‍♀️', 
      description: 'Master of personalized learning recommendations. Analyzes your subject, level, and learning style to provide tailored platform and course suggestions.', 
      specialties: ['Course Recommendations', 'Platform Selection', 'Learning Style Analysis', 'Personalized Guidance'], 
      color: 'from-green-600 to-emerald-700', 
      task: 'Recommendation Engine',
      image: '/images/mcgonagell.jpeg'
    },
    { 
      id: 'snape', 
      name: 'Professor Snape', 
      subject: 'Career Path Guide', 
      personality: 'Exacting perfectionist', 
      avatar: '🧪', 
      description: 'Master of structured career progression. Designs comprehensive learning paths with clear subtopics, duration estimates, and skill progression routes.', 
      specialties: ['Career Planning', 'Skill Progression', 'Learning Paths', 'Professional Development'], 
      color: 'from-slate-700 to-gray-800', 
      task: 'Career Path Guide',
      image: '/images/snape.jpg'
    },
    { 
      id: 'lupin', 
      name: 'Professor Lupin', 
      subject: 'The Tutor', 
      personality: 'Gentle, encouraging mentor', 
      avatar: '🛡️', 
      description: 'Expert in personalized tutoring and study guidance. Provides budget-conscious resources, effective study techniques, and knows when additional help is needed.', 
      specialties: ['Tutoring', 'Study Techniques', 'Resource Management', 'Learning Support'], 
      color: 'from-blue-600 to-indigo-700', 
      task: 'The Tutor',
      image: '/images/Lupin.jpeg'
    },
    { 
      id: 'hagrid', 
      name: 'Professor Hagrid', 
      subject: 'Doubt Solver', 
      personality: 'Enthusiastic, hands-on teacher', 
      avatar: '🐉', 
      description: 'Master of breaking down complex problems into understandable explanations. Tackles your doubts with patience and clarity, regardless of difficulty level.', 
      specialties: ['Problem Solving', 'Concept Clarification', 'Doubt Resolution', 'Simplified Explanations'], 
      color: 'from-amber-600 to-orange-700', 
      task: 'Doubt Solver',
      image: '/images/hagrid.jpg'
    },
  ];
  
  const setApiState = (profId: Professor['id'], isLoading: boolean, error: string | null) => {
    setLoadingStates(prev => ({ ...prev, [profId]: isLoading }));
    setErrorStates(prev => ({ ...prev, [profId]: error }));
  };

  const speakToProfessor = (professor: Professor) => {
    setActiveProfessor(professor.id);
    setSelectedProfessor(professor);
    setMcgResults(null); setSnapeResults(null); setLupinResults(null); setHagridResults(null);
    setErrorStates({ mcgonagall: null, snape: null, lupin: null, hagrid: null });
    setTimeout(() => setActiveProfessor(null), 3000);
  };
  
  // --- API Handlers ---

  const handleMcGonagallSubmit = async () => {
    if (!mcgSubject) return;
    setApiState('mcgonagall', true, null);
    try {
      const params = new URLSearchParams({ subject: mcgSubject, level: mcgLevel, learning_style: mcgLearningStyle });
      const response = await fetch(`http://localhost:5000/api/pods/recommend?${params}`);
      if (!response.ok) throw new Error('Failed to get recommendations from the Headmistress.');
      const data = await response.json();
      if (data.success) setMcgResults(data);
      else throw new Error(data.error || 'An unknown error occurred.');
    } catch (err: any) {
      setApiState('mcgonagall', false, err.message);
    } finally {
      setLoadingStates(prev => ({ ...prev, mcgonagall: false }));
    }
  };

  const handleSnapeSubmit = async () => {
    if (!snapeSubject) return;
    setApiState('snape', true, null);
    try {
      const response = await fetch('http://localhost:5000/api/pods/learning-path', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          subject: snapeSubject,
          current_level: snapeCurrentLevel,
          target_level: snapeTargetLevel,
          timeline: snapeTimeline
        }),
      });
      if (!response.ok) throw new Error('The Potions Master is displeased with your request.');
      const data = await response.json();
      if (data.success) setSnapeResults(data);
      else throw new Error(data.error || 'An unknown error occurred.');
    } catch (err: any) {
      setApiState('snape', false, err.message);
    } finally {
      setLoadingStates(prev => ({ ...prev, snape: false }));
    }
  };

  const handleLupinSubmit = async () => {
    if (!lupinSubject) return;
    setApiState('lupin', true, null);
    try {
      const params = new URLSearchParams({ subject: lupinSubject, budget: lupinBudget, format: lupinFormat });
      const response = await fetch(`http://localhost:5000/api/pods/tutoring?${params}`);
      if (!response.ok) throw new Error('Could not get tutoring guidance. The moon must be full.');
      const data = await response.json();
      if (data.success) setLupinResults(data);
      else throw new Error(data.error || 'An unknown error occurred.');
    } catch (err: any) {
      setApiState('lupin', false, err.message);
    } finally {
      setLoadingStates(prev => ({ ...prev, lupin: false }));
    }
  };
  
  const handleHagridSubmit = async () => {
    if (!hagridQuestion || !hagridSubject) return;
    setApiState('hagrid', true, null);
    try {
      const response = await fetch('http://localhost:5000/api/pods/ai-tutor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: hagridQuestion,
          subject: hagridSubject,
          difficulty: hagridDifficulty,
          learning_style: hagridLearningStyle,
        }),
      });
      if (!response.ok) throw new Error("Blast-Ended Skrewt got into the server room!");
      const data = await response.json();
      if (data.success) setHagridResults(data);
      else throw new Error(data.error || 'An unknown error occurred.');
    } catch (err: any) {
      setApiState('hagrid', false, err.message);
    } finally {
      setLoadingStates(prev => ({ ...prev, hagrid: false }));
    }
  };

  // --- Render Functions ---
  
  const ResultCard = ({ title, children }: { title: string; children: React.ReactNode }) => (
    <div className="p-4 bg-slate-700/30 rounded-lg border border-slate-600/30">
      <h5 className="text-parchment font-medium mb-2">{title}</h5>
      <div className="text-slate-300 text-sm space-y-1">{children}</div>
    </div>
  );

  const renderProfessorInterface = () => {
    if (!selectedProfessor) return null;

    const isLoading = loadingStates[selectedProfessor.id];
    const error = errorStates[selectedProfessor.id];

    const renderError = (err: string | null) => err && (
        <div className="p-3 my-2 text-sm text-red-300 bg-red-800/30 border border-red-500/50 rounded-md flex items-center gap-2">
            <XCircleIcon className="w-5 h-5" /> {err}
        </div>
    );

    switch (selectedProfessor.id) {
      case 'mcgonagall':
        return (
          <div className="space-y-4">
            <h4 className="text-parchment font-medium mb-3">Recommendation Engine</h4>
            <div><label className="block text-parchment/70 text-sm mb-2">Subject</label><input type="text" value={mcgSubject} onChange={(e) => setMcgSubject(e.target.value)} placeholder="e.g., Python, Physics" className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-slate-400/50"/></div>
            <div><label className="block text-parchment/70 text-sm mb-2">Level</label><select value={mcgLevel} onChange={(e) => setMcgLevel(e.target.value)} className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment focus:outline-none focus:ring-2 focus:ring-slate-400/50"><option value="beginner">Beginner</option><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option></select></div>
            <div><label className="block text-parchment/70 text-sm mb-2">Learning Style</label><select value={mcgLearningStyle} onChange={(e) => setMcgLearningStyle(e.target.value)} className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment focus:outline-none focus:ring-2 focus:ring-slate-400/50"><option value="visual">Visual</option><option value="auditory">Auditory</option><option value="kinesthetic">Kinesthetic (Hands-on)</option><option value="mixed">Mixed</option></select></div>
            {renderError(error)}
            <button onClick={handleMcGonagallSubmit} disabled={isLoading} className="w-full py-3 bg-gradient-to-r from-green-600 to-emerald-700 text-white rounded-lg hover:opacity-90 transition-opacity shadow-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed">{isLoading ? 'Consulting...' : 'Get Recommendations'}</button>
            {/* FIX: Use optional chaining (?.) for safe access */}
            {mcgResults?.personalized_recommendations && <div className="mt-6 space-y-4">
              <ResultCard title="Professor's Recommendation"><p className='whitespace-pre-wrap'>{mcgResults.personalized_recommendations.recommendations}</p></ResultCard>
            </div>}
          </div>
        );

      case 'snape':
        return (
          <div className="space-y-4">
            <h4 className="text-parchment font-medium mb-3">Career Path Guide</h4>
            <div><label className="block text-parchment/70 text-sm mb-2">Subject Area</label><input type="text" value={snapeSubject} onChange={(e) => setSnapeSubject(e.target.value)} placeholder="e.g., Web Development" className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-slate-400/50"/></div>
            <div><label className="block text-parchment/70 text-sm mb-2">Current Level</label><select value={snapeCurrentLevel} onChange={(e) => setSnapeCurrentLevel(e.target.value)} className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment focus:outline-none focus:ring-2 focus:ring-slate-400/50"><option value="beginner">Beginner</option><option value="intermediate">Intermediate</option></select></div>
            <div><label className="block text-parchment/70 text-sm mb-2">Target Level</label><select value={snapeTargetLevel} onChange={(e) => setSnapeTargetLevel(e.target.value)} className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment focus:outline-none focus:ring-2 focus:ring-slate-400/50"><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option></select></div>
            <div><label className="block text-parchment/70 text-sm mb-2">Timeline</label><input type="text" value={snapeTimeline} onChange={(e) => setSnapeTimeline(e.target.value)} placeholder="e.g., 6 months" className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-slate-400/50"/></div>
            {renderError(error)}
            <button onClick={handleSnapeSubmit} disabled={isLoading} className="w-full py-3 bg-gradient-to-r from-slate-700 to-gray-800 text-white rounded-lg hover:opacity-90 transition-opacity shadow-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed">{isLoading ? 'Brewing Path...' : 'Generate Career Path'}</button>
            {/* FIX: Use optional chaining (?.) for safe access */}
            {snapeResults?.learning_path && <div className="mt-6 space-y-4">
              <ResultCard title={`Learning Path (${snapeResults.learning_path.total_duration})`}>
                <p className="mb-2"><strong>Weekly Commitment:</strong> {snapeResults.learning_path.weekly_commitment}</p>
                {snapeResults.learning_path.learning_modules?.map(mod => <p key={mod.order}>{mod.order}. {mod.topic} ({mod.estimated_duration})</p>)}
              </ResultCard>
            </div>}
          </div>
        );

      case 'lupin':
        return (
          <div className="space-y-4">
            <h4 className="text-parchment font-medium mb-3">The Tutor</h4>
            <div><label className="block text-parchment/70 text-sm mb-2">Subject</label><input type="text" value={lupinSubject} onChange={(e) => setLupinSubject(e.target.value)} placeholder="e.g., Data Structures" className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-slate-400/50"/></div>
            <div><label className="block text-parchment/70 text-sm mb-2">Budget</label><select value={lupinBudget} onChange={(e) => setLupinBudget(e.target.value)} className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment focus:outline-none focus:ring-2 focus:ring-slate-400/50"><option value="free">Free</option><option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option></select></div>
            <div><label className="block text-parchment/70 text-sm mb-2">Format</label><select value={lupinFormat} onChange={(e) => setLupinFormat(e.target.value)} className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment focus:outline-none focus:ring-2 focus:ring-slate-400/50"><option value="online">Online</option><option value="in_person">In-Person</option><option value="hybrid">Hybrid</option></select></div>
            {renderError(error)}
            <button onClick={handleLupinSubmit} disabled={isLoading} className="w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-700 text-white rounded-lg hover:opacity-90 transition-opacity shadow-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed">{isLoading ? 'Searching...' : 'Get Tutoring Guidance'}</button>
            {/* FIX: Use optional chaining (?.) and check for array length */}
            {lupinResults && <div className="mt-6 space-y-4">
                {lupinResults.online_platforms?.length > 0 && <ResultCard title="Recommended Platforms">{lupinResults.online_platforms.map(p => <div key={p.name}><strong>{p.name}</strong>: {p.best_for}</div>)}</ResultCard>}
                {lupinResults.preparation_tips?.length > 0 && <ResultCard title="Preparation Tips"><ul>{lupinResults.preparation_tips.map((tip, i) => <li key={i}>- {tip}</li>)}</ul></ResultCard>}
                {lupinResults.self_directed_alternatives?.study_techniques?.length > 0 && <ResultCard title="Effective Study Techniques"><ul>{lupinResults.self_directed_alternatives.study_techniques.map((tech, i) => <li key={i}>- {tech}</li>)}</ul></ResultCard>}
            </div>}
          </div>
        );

      case 'hagrid':
        return (
          <div className="space-y-4">
            <h4 className="text-parchment font-medium mb-3">Doubt Solver</h4>
            <div><label className="block text-parchment/70 text-sm mb-2">Question</label><textarea value={hagridQuestion} onChange={(e) => setHagridQuestion(e.target.value)} placeholder="What is a closure in JavaScript?" rows={3} className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-slate-400/50 resize-none"/></div>
            <div><label className="block text-parchment/70 text-sm mb-2">Subject</label><input type="text" value={hagridSubject} onChange={(e) => setHagridSubject(e.target.value)} placeholder="e.g., JavaScript" className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-slate-400/50"/></div>
            <div><label className="block text-parchment/70 text-sm mb-2">Difficulty</label><select value={hagridDifficulty} onChange={(e) => setHagridDifficulty(e.target.value)} className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment focus:outline-none focus:ring-2 focus:ring-slate-400/50"><option value="beginner">Beginner</option><option value="intermediate">Intermediate</option><option value="advanced">Advanced</option></select></div>
            <div><label className="block text-parchment/70 text-sm mb-2">Learning Style</label><select value={hagridLearningStyle} onChange={(e) => setHagridLearningStyle(e.target.value)} className="w-full p-3 bg-slate-700/50 border border-slate-600/30 rounded-md text-parchment focus:outline-none focus:ring-2 focus:ring-slate-400/50"><option value="visual">Visual</option><option value="auditory">Auditory</option><option value="kinesthetic">Kinesthetic</option><option value="mixed">Mixed</option></select></div>
            {renderError(error)}
            <button onClick={handleHagridSubmit} disabled={isLoading} className="w-full py-3 bg-gradient-to-r from-amber-600 to-orange-700 text-white rounded-lg hover:opacity-90 transition-opacity shadow-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed">{isLoading ? 'Thinkin\'...' : 'Get Explanation'}</button>
            {/* FIX: Use optional chaining (?.) for safe access */}
            {hagridResults?.tutoring_response && <div className="mt-6"><ResultCard title="Here's What I Reckon"><p className="whitespace-pre-wrap">{hagridResults.tutoring_response.explanation}</p></ResultCard></div>}
          </div>
        );

      default:
        return null;
    }
  };
  
  // --- Main Render ---

  return (
    <div className="min-h-screen p-8">
      <Navbar />
      <button onClick={() => navigate(-1)} className="absolute top-6 right-6 bg-rose-600/60 hover:bg-rose-500 text-parchment px-4 py-2 rounded-md border border-slate-500/50 shadow-md transition">Back</button>
      <div className="max-w-6xl mx-auto">
        <motion.div initial={{ y: -50, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.8 }} className="text-center mb-12">
          <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-slate-400 via-gray-300 to-slate-400 mb-4">Professor Portrait Gallery</h1>
          <p className="text-parchment/70 text-lg mb-8">Seek wisdom from the finest educators</p>
        </motion.div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <motion.div initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 0.8, delay: 0.2 }} className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-8 border border-slate-400/20 backdrop-blur-sm">
              <h2 className="text-2xl font-['Cormorant_Garamond'] text-parchment mb-8 text-center">Choose Your Mentor</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {professors.map((professor, index) => (
                  <motion.div key={professor.id} initial={{ y: 50, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ duration: 0.6, delay: index * 0.1 }} whileHover={{ scale: 1.02, y: -5 }} onClick={() => speakToProfessor(professor)} className="group relative cursor-pointer">
                    <div className={`relative p-6 rounded-xl border-2 bg-gradient-to-br ${professor.color} border-gold/30 shadow-xl transition-all duration-300 group-hover:border-gold/50 group-hover:shadow-2xl`}>
                      <motion.div animate={activeProfessor === professor.id ? { scale: [1, 1.1, 1], rotate: [0, 5, -5, 0] } : {}} transition={{ duration: 0.5 }} className="text-center mb-4">
                        <img 
                          src={professor.image} 
                          alt={professor.name}
                          className="w-16 h-16 mx-auto rounded-full object-cover border-2 border-white/50 shadow-lg"
                        />
                      </motion.div>
                      <div className="text-center text-white"><h3 className="text-xl font-['Cormorant_Garamond'] font-bold mb-2">{professor.name}</h3><p className="text-sm opacity-90 mb-3">{professor.task}</p><p className="text-xs opacity-80 italic">"{professor.personality}"</p></div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          </div>
          <div>
            <motion.div initial={{ x: 50, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ duration: 0.8, delay: 0.4 }} className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border border-slate-400/20 backdrop-blur-sm sticky top-8">
              <h2 className="text-xl font-['Cormorant_Garamond'] text-parchment mb-6 flex items-center space-x-2"><AcademicCapIcon className="w-6 h-6 text-slate-400" /><span>Professor's Guidance</span></h2>
              {selectedProfessor ? (
                <motion.div key={selectedProfessor.id} initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="space-y-6">
                  <div className="text-center">
                    <img 
                      src={selectedProfessor.image} 
                      alt={selectedProfessor.name}
                      className="w-20 h-20 mx-auto mb-3 rounded-full object-cover border-2 border-white/50 shadow-lg"
                    />
                    <h3 className="text-lg font-medium text-parchment">{selectedProfessor.name}</h3>
                    <p className="text-slate-400 text-sm">{selectedProfessor.task}</p>
                  </div>
                  <p className="text-parchment/70 text-sm leading-relaxed">{selectedProfessor.description}</p>
                  <div><h4 className="text-parchment font-medium mb-3">Specialties:</h4><div className="flex flex-wrap gap-2">{selectedProfessor.specialties.map((specialty) => (<span key={specialty} className="px-3 py-1 bg-slate-700/50 text-slate-300 rounded-full text-xs border border-slate-600/50">{specialty}</span>))}</div></div>
                  {renderProfessorInterface()}
                </motion.div>
              ) : (
                <div className="text-center text-parchment/50 py-12"><AcademicCapIcon className="w-12 h-12 mx-auto mb-4 opacity-50" /><p>Click on a professor's portrait to seek their wisdom</p></div>
              )}
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfessorPods;