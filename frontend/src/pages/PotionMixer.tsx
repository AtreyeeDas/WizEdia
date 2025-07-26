import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { BeakerIcon, PlusIcon, SparklesIcon, XCircleIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

interface Ingredient {
  id: string;
  name: string;
  type: 'concept' | 'question' | 'confusion';
  color: string;
}

interface Potion {
  id: number;
  ingredients: Ingredient[];
  result: string; // This will hold the 'description' from the API
  color: string;
  timestamp: Date;
  brewing_difficulty: string;
}

const PotionMixer: React.FC = () => {
  const [availableIngredients, setAvailableIngredients] = useState<Ingredient[]>([
    { id: '1', name: 'Complex Algorithms', type: 'concept', color: 'bg-blue-500' },
    { id: '2', name: 'Database Relationships', type: 'concept', color: 'bg-green-500' },
    { id: '3', name: 'Recursion', type: 'question', color: 'bg-yellow-500' },
    { id: '4', name: 'Asynchronous JavaScript', type: 'confusion', color: 'bg-red-500' },
    { id: '5', name: 'React Hooks Logic', type: 'concept', color: 'bg-purple-500' },
  ]);

  const [cauldronIngredients, setCauldronIngredients] = useState<Ingredient[]>([]);
  const [potions, setPotions] = useState<Potion[]>([]);
  const [isBrewingPotion, setIsBrewingPotion] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [newIngredient, setNewIngredient] = useState({ name: '', type: 'concept' as Ingredient['type'] });
  const [showAddIngredient, setShowAddIngredient] = useState(false);
  const navigate = useNavigate();

  const getIngredientColor = (type: Ingredient['type']) => {
    switch (type) {
      case 'concept': return 'bg-blue-500';
      case 'question': return 'bg-yellow-500';
      case 'confusion': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  // Helper to determine potion color based on difficulty from API
  const getPotionColor = (difficulty: string) => {
    const difficultyClean = difficulty.toLowerCase();
    if (difficultyClean.includes('easy') || difficultyClean.includes('low')) {
        return 'from-green-400 to-emerald-600';
    }
    if (difficultyClean.includes('intermediate') || difficultyClean.includes('medium')) {
        return 'from-blue-400 to-indigo-600';
    }
    if (difficultyClean.includes('hard') || difficultyClean.includes('high') || difficultyClean.includes('difficult')) {
        return 'from-red-600 to-red-800';
    }
    return 'from-purple-400 to-violet-600'; // Default
  };


  const addIngredient = () => {
    if (newIngredient.name.trim()) {
      const ingredient: Ingredient = {
        id: Date.now().toString(),
        name: newIngredient.name,
        type: newIngredient.type,
        color: getIngredientColor(newIngredient.type)
      };
      setAvailableIngredients([...availableIngredients, ingredient]);
      setNewIngredient({ name: '', type: 'concept' });
      setShowAddIngredient(false);
    }
  };

  const addToCauldron = (ingredient: Ingredient) => {
    setCauldronIngredients([...cauldronIngredients, ingredient]);
    setAvailableIngredients(availableIngredients.filter(i => i.id !== ingredient.id));
  };

  const removeFromCauldron = (ingredient: Ingredient) => {
    setCauldronIngredients(cauldronIngredients.filter(i => i.id !== ingredient.id));
    setAvailableIngredients([...availableIngredients, ingredient]);
  };

  const brewPotion = async () => {
    if (cauldronIngredients.length === 0) return;

    setIsBrewingPotion(true);
    setError(null);

    const conceptNames = cauldronIngredients.map(ing => ing.name);

    try {
        const response = await fetch('http://localhost:5000/api/potion/analyze-batch', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ concepts: conceptNames }),
        });

        if (!response.ok) {
            throw new Error(`The potion fizzled unexpectedly... (HTTP ${response.status})`);
        }

        const data = await response.json();

        if (data.success && data.batch_analysis) {
            const newPotion: Potion = {
                id: Date.now(),
                ingredients: [...cauldronIngredients],
                result: data.batch_analysis.description,
                brewing_difficulty: data.batch_analysis.brewing_difficulty,
                color: getPotionColor(data.batch_analysis.brewing_difficulty),
                timestamp: new Date(),
            };
            setPotions([newPotion, ...potions]);
            setCauldronIngredients([]); // Clear the cauldron
        } else {
            throw new Error(data.error || "The potion's ingredients failed to combine properly.");
        }

    } catch (err: any) {
        setError(err.message || 'A mysterious force prevented the brewing.');
    } finally {
        setIsBrewingPotion(false);
    }
  };
  
  return (
    <div className="min-h-screen p-8">
      <Navbar />
      <button
        onClick={() => navigate(-1)}
        className="absolute top-6 right-6 bg-rose-600/60 hover:bg-rose-500 text-parchment px-4 py-2 rounded-md border border-slate-500/50 shadow-md transition"
      >
        Back
      </button>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-green-400 via-emerald-400 to-green-400 mb-4">
            Professor's Potion Lab
          </h1>
          <p className="text-parchment/70 text-lg mb-8">
            Mix your confusing concepts into a potion of clear understanding
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Ingredient Shelves & Results */}
          <div className="lg:col-span-2 space-y-8">
            <motion.div
              initial={{ x: -50, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border border-green-400/20 backdrop-blur-sm"
            >
              {/* Shelves Header & Add Button */}
              <div className="flex items-center justify-between mb-6">
                 <h2 className="text-xl font-['Cormorant_Garamond'] text-parchment">
                     Ingredient Shelves
                 </h2>
                 <motion.button
                     whileHover={{ scale: 1.05 }}
                     whileTap={{ scale: 0.95 }}
                     onClick={() => setShowAddIngredient(true)}
                     className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-500 hover:to-emerald-500 transition-colors shadow-lg"
                 >
                     <PlusIcon className="w-5 h-5" />
                     <span>Add Ingredient</span>
                 </motion.button>
              </div>

              {/* Add Ingredient Form */}
              {showAddIngredient && (
                <motion.div
                  initial={{ y: -20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  className="bg-slate-700/30 rounded-lg p-4 mb-6 border border-green-400/20"
                >
                  <div className="space-y-3">
                    <input
                      type="text"
                      placeholder="What concept confuses you?"
                      value={newIngredient.name}
                      onChange={(e) => setNewIngredient({ ...newIngredient, name: e.target.value })}
                      className="w-full p-3 bg-slate-700/50 border border-green-400/20 rounded-lg text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-green-400/50"
                    />
                    <div className="flex space-x-3">
                      <select
                        value={newIngredient.type}
                        onChange={(e) => setNewIngredient({ ...newIngredient, type: e.target.value as Ingredient['type'] })}
                        className="flex-1 p-3 bg-slate-700/50 border border-green-400/20 rounded-lg text-parchment focus:outline-none focus:ring-2 focus:ring-green-400/50"
                      >
                        <option value="concept">Concept</option>
                        <option value="question">Question</option>
                        <option value="confusion">Confusion</option>
                      </select>
                      <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={addIngredient} className="px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-500 transition-colors">Add</motion.button>
                      <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} onClick={() => setShowAddIngredient(false)} className="px-4 py-3 bg-slate-600 text-white rounded-lg hover:bg-slate-500 transition-colors">Cancel</motion.button>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Available Ingredients Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                 {availableIngredients.map((ingredient, index) => (
                     <motion.div
                         key={ingredient.id}
                         initial={{ y: 20, opacity: 0 }}
                         animate={{ y: 0, opacity: 1 }}
                         transition={{ duration: 0.5, delay: index * 0.1 }}
                         whileHover={{ scale: 1.02, y: -2 }}
                         onClick={() => addToCauldron(ingredient)}
                         className={`p-4 ${ingredient.color} rounded-lg cursor-pointer shadow-lg hover:shadow-xl transition-all duration-300 text-white`}
                     >
                         <div className="flex items-center space-x-3">
                             <div className="w-3 h-3 bg-white rounded-full opacity-80" />
                             <div>
                                 <div className="font-medium">{ingredient.name}</div>
                                 <div className="text-xs opacity-80 capitalize">{ingredient.type}</div>
                             </div>
                         </div>
                     </motion.div>
                 ))}
              </div>
            </motion.div>

            {/* Brewing Results */}
            {potions.length > 0 && (
              <motion.div
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.8, delay: 0.4 }}
                className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border border-green-400/20 backdrop-blur-sm"
              >
                 <h2 className="text-xl font-['Cormorant_Garamond'] text-parchment mb-6">Recent Brews</h2>
                 <div className="space-y-4 max-h-[40rem] overflow-y-auto pr-2">
                     {potions.map((potion, index) => (
                         <motion.div
                             key={potion.id}
                             initial={{ x: -20, opacity: 0 }}
                             animate={{ x: 0, opacity: 1 }}
                             transition={{ duration: 0.5, delay: index * 0.1 }}
                             className={`p-4 bg-gradient-to-r ${potion.color} rounded-lg border border-white/20 text-white`}
                         >
                            <div className="text-sm opacity-80 mb-3">{potion.timestamp.toLocaleString()}</div>
                            <div className="font-semibold mb-3">Potion Analysis:</div>
                            {/* Render the detailed description, preserving whitespace */}
                            <div className="text-sm mb-4 whitespace-pre-wrap font-light opacity-90">{potion.result}</div>
                            <div className="text-xs opacity-80 border-t border-white/20 pt-2">
                                <p><strong>Ingredients:</strong> {potion.ingredients.map(i => i.name).join(', ')}</p>
                                <p><strong>Brewing Difficulty:</strong> {potion.brewing_difficulty}</p>
                            </div>
                         </motion.div>
                     ))}
                 </div>
              </motion.div>
            )}
          </div>

          {/* Cauldron */}
          <motion.div
            initial={{ x: 50, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border border-green-400/20 backdrop-blur-sm sticky top-8"
          >
             <h2 className="text-xl font-['Cormorant_Garamond'] text-parchment mb-6 flex items-center space-x-2">
                 <BeakerIcon className="w-6 h-6 text-green-400" />
                 <span>Brewing Cauldron</span>
             </h2>

             {/* Cauldron Visual & Ingredients */}
             <div className="relative mb-6">
                {/* Visuals here - code unchanged */}
                <motion.div
                  className="w-48 h-48 mx-auto bg-gradient-to-br from-slate-700 to-slate-900 rounded-full border-4 border-slate-600 shadow-2xl overflow-hidden"
                  animate={isBrewingPotion ? { scale: [1, 1.05, 1] } : {}}
                  transition={{ duration: 0.5, repeat: isBrewingPotion ? Infinity : 0 }}
                >
                    {cauldronIngredients.length > 0 && (
                        <>
                        <motion.div animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.7, 0.3] }} transition={{ duration: 2, repeat: Infinity }} className="absolute inset-8 bg-gradient-to-br from-green-400/30 to-emerald-600/50 rounded-full" />
                        {[...Array(6)].map((_, i) => ( <motion.div key={i} animate={{ y: [0, -20, 0], opacity: [0, 1, 0], scale: [0.5, 1, 0.5]}} transition={{ duration: 1.5, repeat: Infinity, delay: i * 0.3}} className="absolute w-2 h-2 bg-green-400 rounded-full" style={{ left: `${30 + i * 8}%`, top: '70%'}} /> ))}
                        </>
                    )}
                    {cauldronIngredients.length === 0 && (<div className="absolute inset-0 flex items-center justify-center text-parchment/50 text-sm text-center">Drop ingredients here</div>)}
                </motion.div>
                {/* Sparks */}
                {isBrewingPotion && ( <> {[...Array(8)].map((_, i) => ( <motion.div key={i} className="absolute w-1 h-1 bg-green-400 rounded-full" animate={{ scale: [0, 1, 0], y: [0, -40, -80], x: [0, Math.random() * 40 - 20, Math.random() * 80 - 40], opacity: [0, 1, 0]}} transition={{ duration: 2, repeat: Infinity, delay: i * 0.2}} style={{ left: `${45 + Math.random() * 10}%`, top: '20%'}}/> ))} </>)}
             </div>

             {/* Ingredients in Cauldron */}
             {cauldronIngredients.length > 0 && (
                <div className="space-y-2 mb-6 min-h-[50px]">
                  <h3 className="text-sm text-parchment/70">In the cauldron:</h3>
                  {cauldronIngredients.map((ingredient) => (
                    <motion.div key={ingredient.id} initial={{ scale: 0 }} animate={{ scale: 1 }} onClick={() => removeFromCauldron(ingredient)} className={`p-2 ${ingredient.color} rounded text-white text-sm cursor-pointer hover:opacity-80 transition-opacity`}>
                      {ingredient.name}
                    </motion.div>
                  ))}
                </div>
             )}

             {/* Brew Button */}
             <motion.button
                whileHover={{ scale: cauldronIngredients.length > 0 ? 1.05 : 1 }}
                whileTap={{ scale: cauldronIngredients.length > 0 ? 0.95 : 1 }}
                onClick={brewPotion}
                disabled={cauldronIngredients.length === 0 || isBrewingPotion}
                className={`w-full py-3 rounded-lg font-medium transition-all duration-300 ${cauldronIngredients.length > 0 && !isBrewingPotion ? 'bg-gradient-to-r from-green-600 to-emerald-600 text-white hover:from-green-500 hover:to-emerald-500 shadow-lg' : 'bg-slate-700/50 text-parchment/50 cursor-not-allowed'}`}
             >
                <span className="flex items-center justify-center space-x-2">
                    <SparklesIcon className="w-5 h-5" />
                    <span>{isBrewingPotion ? 'Brewing...' : 'Brew Potion'}</span>
                </span>
             </motion.button>

             {/* Error Message */}
             {error && (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-4 bg-red-900/50 border border-red-500 text-red-300 px-4 py-3 rounded-lg flex items-center space-x-3 text-sm">
                    <XCircleIcon className="w-5 h-5" />
                    <span>{error}</span>
                </motion.div>
             )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default PotionMixer;