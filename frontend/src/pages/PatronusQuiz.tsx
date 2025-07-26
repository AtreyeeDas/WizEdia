import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { SparklesIcon, CheckIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

interface PatronusQuizProps {
  onComplete: (house: string, patronus: string) => void;
}

interface Question {
  id: number;
  text: string;
  options: {
    text: string;
    house: string;
    patronus: string;
  }[];
}

const PatronusQuiz: React.FC<PatronusQuizProps> = ({ onComplete }) => {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<string[]>([]);
  const [showResult, setShowResult] = useState(false);
  const [result, setResult] = useState<{ house: string; patronus: string } | null>(null);

  const questions: Question[] = [
    {
      id: 1,
      text: "You're faced with a difficult challenge. What's your first instinct?",
      options: [
        { text: "Face it head-on with courage", house: "gryffindor", patronus: "Lion" },
        { text: "Carefully analyze and plan your approach", house: "ravenclaw", patronus: "Eagle" },
        { text: "Find a clever way to turn it to your advantage", house: "slytherin", patronus: "Serpent" },
        { text: "Work steadily and persistently through it", house: "hufflepuff", patronus: "Badger" }
      ]
    },
    {
      id: 2,
      text: "What quality do you value most in others?",
      options: [
        { text: "Bravery and loyalty", house: "gryffindor", patronus: "Stag" },
        { text: "Intelligence and creativity", house: "ravenclaw", patronus: "Raven" },
        { text: "Ambition and cunning", house: "slytherin", patronus: "Dragon" },
        { text: "Kindness and hard work", house: "hufflepuff", patronus: "Bear" }
      ]
    },
    {
      id: 3,
      text: "Where would you prefer to spend your free time?",
      options: [
        { text: "Training for the next adventure", house: "gryffindor", patronus: "Wolf" },
        { text: "In a library, surrounded by books", house: "ravenclaw", patronus: "Owl" },
        { text: "Planning your next move", house: "slytherin", patronus: "Fox" },
        { text: "In nature, enjoying simple pleasures", house: "hufflepuff", patronus: "Rabbit" }
      ]
    },
    {
      id: 4,
      text: "What motivates you the most?",
      options: [
        { text: "Protecting those you love", house: "gryffindor", patronus: "Phoenix" },
        { text: "The pursuit of knowledge", house: "ravenclaw", patronus: "Dolphin" },
        { text: "Achieving your goals", house: "slytherin", patronus: "Panther" },
        { text: "Making the world a better place", house: "hufflepuff", patronus: "Deer" }
      ]
    },
    {
      id: 5,
      text: "How do you handle failure?",
      options: [
        { text: "Learn from it and try again immediately", house: "gryffindor", patronus: "Tiger" },
        { text: "Analyze what went wrong and adapt", house: "ravenclaw", patronus: "Swan" },
        { text: "Use it as motivation to succeed", house: "slytherin", patronus: "Falcon" },
        { text: "Accept it gracefully and keep working", house: "hufflepuff", patronus: "Elephant" }
      ]
    }
  ];

  const handleAnswer = (optionIndex: number) => {
    const newAnswers = [...answers, `${currentQuestion}-${optionIndex}`];
    setAnswers(newAnswers);

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      // Calculate result
      const houseCount: { [key: string]: number } = {};
      const patronusOptions: string[] = [];

      newAnswers.forEach((answer, index) => {
        const [questionIndex, optionIndex] = answer.split('-').map(Number);
        const option = questions[questionIndex].options[optionIndex];
        
        houseCount[option.house] = (houseCount[option.house] || 0) + 1;
        patronusOptions.push(option.patronus);
      });

      // Determine house
      const house = Object.keys(houseCount).reduce((a, b) => 
        houseCount[a] > houseCount[b] ? a : b
      );

      // Pick a random patronus from the user's selections
      const patronus = patronusOptions[Math.floor(Math.random() * patronusOptions.length)];

      setResult({ house, patronus });
      setShowResult(true);
    }
  };

  const handleComplete = () => {
    if (result) {
      onComplete(result.house, result.patronus);
    }
  };

  const getHouseColors = (house: string) => {
    const colors = {
      gryffindor: "from-red-600 to-yellow-600",
      slytherin: "from-green-600 to-gray-700",
      ravenclaw: "from-blue-600 to-indigo-700",
      hufflepuff: "from-yellow-600 to-amber-700"
    };
    return colors[house as keyof typeof colors] || "from-purple-600 to-indigo-700";
  };

  const getHouseDescription = (house: string) => {
    const descriptions = {
      gryffindor: "You belong in Gryffindor, where the brave at heart dwell. Your courage and determination set you apart.",
      slytherin: "You belong in Slytherin, where the cunning use any means to achieve their ends. Your ambition knows no bounds.",
      ravenclaw: "You belong in Ravenclaw, where wit and learning will always find their kind. Your wisdom guides your path.",
      hufflepuff: "You belong in Hufflepuff, where they are just and loyal. Your kindness and hard work are your greatest strengths."
    };
    return descriptions[house as keyof typeof descriptions] || "";
  };

  const navigate=useNavigate()

  return (
    <div 
      className="min-h-screen flex items-center justify-center"
      style={{
        backgroundImage: `url('/images/patronus.jpeg')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
      <Navbar />
      <div className="min-h-screen p-8 relative flex items-center justify-center">
        {/* Dark overlay for better readability */}
        <div className="absolute inset-0 bg-black/40" />
        
        <div className="relative z-10 max-w-2xl mx-auto">
          <button
            onClick={() => navigate(-1)}
            className="absolute top-6 right-6 bg-rose-600/60 hover:bg-rose-500 text-parchment px-4 py-2 rounded-md border border-slate-500/50 shadow-md transition"
          >
            Back
          </button>
          <AnimatePresence mode="wait">
            {!showResult ? (
              <motion.div
                key="quiz"
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -50 }}
                className="text-center"
              >
                {/* Header */}
                <div className="mb-8">
                  <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-silver via-gold to-silver mb-4">
                    The Patronus Quiz
                  </h1>
                  <p className="text-white/80 text-lg mb-6">
                    Discover your Hogwarts House and Patronus
                  </p>
                  
                  {/* Progress Bar */}
                  <div className="w-full bg-slate-700 rounded-full h-2 mb-8">
                    <motion.div
                      className="bg-gradient-to-r from-gold to-amber-400 h-2 rounded-full"
                      initial={{ width: 0 }}
                      animate={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
                      transition={{ duration: 0.5 }}
                    />
                  </div>
                </div>

                {/* Question */}
                <motion.div
                  key={currentQuestion}
                  initial={{ x: 100, opacity: 0 }}
                  animate={{ x: 0, opacity: 1 }}
                  exit={{ x: -100, opacity: 0 }}
                  className="bg-gradient-to-br from-blue-900/80 to-indigo-900/90 rounded-xl p-8 border border-blue-400/30 backdrop-blur-sm"
                  style={{
                    boxShadow: '0 0 30px rgba(59, 130, 246, 0.3), 0 0 60px rgba(59, 130, 246, 0.2), 0 0 90px rgba(59, 130, 246, 0.1)',
                    border: '2px solid rgba(59, 130, 246, 0.4)'
                  }}
                >
                  <h2 className="text-2xl font-['Cormorant_Garamond'] text-white mb-8">
                    {questions[currentQuestion].text}
                  </h2>

                  <div className="space-y-4">
                    {questions[currentQuestion].options.map((option, index) => (
                      <motion.button
                        key={index}
                        whileHover={{ scale: 1.02, x: 5 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => handleAnswer(index)}
                        className="w-full p-4 text-left bg-slate-700/70 hover:bg-slate-600/70 rounded-lg border border-blue-400/30 hover:border-blue-400/50 transition-all duration-300 text-white"
                      >
                        <span className="flex items-center justify-between">
                          <span>{option.text}</span>
                          <SparklesIcon className="w-5 h-5 opacity-0 group-hover:opacity-100 transition-opacity" />
                        </span>
                      </motion.button>
                    ))}
                  </div>

                  <div className="mt-6 text-sm text-white/60">
                    Question {currentQuestion + 1} of {questions.length}
                  </div>
                </motion.div>
              </motion.div>
            ) : (
              <motion.div
                key="result"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, type: "spring" }}
                className="text-center"
              >
                {/* Result Display */}
                <div className="bg-gradient-to-br from-blue-900/80 to-indigo-900/90 rounded-xl p-8 border border-blue-400/30 backdrop-blur-sm"
                     style={{
                       boxShadow: '0 0 30px rgba(59, 130, 246, 0.3), 0 0 60px rgba(59, 130, 246, 0.2), 0 0 90px rgba(59, 130, 246, 0.1)',
                       border: '2px solid rgba(59, 130, 246, 0.4)'
                     }}>
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.3, type: "spring" }}
                    className="mb-8"
                  >
                    <div className={`w-32 h-32 mx-auto rounded-full bg-gradient-to-br ${getHouseColors(result!.house)} flex items-center justify-center text-6xl mb-6 magical-glow`}>
                      <span className="text-white font-bold">
                        {result!.house === 'gryffindor' && '🦁'}
                        {result!.house === 'slytherin' && '🐍'}
                        {result!.house === 'ravenclaw' && '🦅'}
                        {result!.house === 'hufflepuff' && '🦡'}
                      </span>
                    </div>
                    
                    <h2 className="text-3xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-gold via-amber-400 to-gold mb-4 capitalize">
                      {result!.house}
                    </h2>
                  </motion.div>

                  <motion.div
                    initial={{ y: 30, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.6 }}
                    className="mb-8"
                  >
                    <p className="text-white/80 text-lg leading-relaxed mb-6">
                      {getHouseDescription(result!.house)}
                    </p>
                    
                    <div className="bg-slate-700/30 rounded-lg p-6 border border-silver/20">
                      <h3 className="text-xl font-['Cormorant_Garamond'] text-silver mb-3">
                        Your Patronus
                      </h3>
                      <div className="flex items-center justify-center space-x-3">
                        <SparklesIcon className="w-6 h-6 text-silver" />
                        <span className="text-2xl font-semibold text-white">{result!.patronus}</span>
                        <SparklesIcon className="w-6 h-6 text-silver" />
                      </div>
                    </div>
                  </motion.div>

                  <motion.button
                    initial={{ y: 30, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.9 }}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleComplete}
                    className={`px-8 py-3 bg-gradient-to-r ${getHouseColors(result!.house)} text-white font-['Cormorant_Garamond'] font-semibold text-lg rounded-lg shadow-xl hover:shadow-2xl transition-all duration-300 magical-glow`}
                  >
                    <span className="flex items-center space-x-2">
                      <CheckIcon className="w-5 h-5" />
                      <button onClick={()=>navigate("/")}>Enter Hogwarts</button>
                    </span>
                  </motion.button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default PatronusQuiz;