import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { RocketLaunchIcon, UsersIcon, LightBulbIcon, TrophyIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

interface Project {
  id: number;
  title: string;
  description: string;
  category: 'web' | 'mobile' | 'ai' | 'blockchain' | 'game';
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  teamSize: string;
  duration: string;
  technologies: string[];
  prizes: string[];
}

interface TeamMember {
  id: number;
  name: string;
  role: string;
  skills: string[];
  experience: 'beginner' | 'intermediate' | 'expert';
  avatar: string;
}

const QuidditchQuest: React.FC = () => {
  const [selectedTab, setSelectedTab] = useState<'projects' | 'team' | 'ideas'>('projects');
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const projects: Project[] = [
    {
      id: 1,
      title: "Winter Hackathon 2024",
      description: "Build innovative solutions for climate change using cutting-edge technology",
      category: 'web',
      difficulty: 'intermediate',
      teamSize: '3-5 members',
      duration: '48 hours',
      technologies: ['React', 'Node.js', 'AI/ML', 'APIs'],
      prizes: ['$5,000 Grand Prize', 'Internship Opportunities', 'Mentorship Program']
    },
    {
      id: 2,
      title: "Mobile Innovation Challenge",
      description: "Create a mobile app that improves daily life for students",
      category: 'mobile',
      difficulty: 'beginner',
      teamSize: '2-4 members',
      duration: '72 hours',
      technologies: ['React Native', 'Flutter', 'Firebase', 'APIs'],
      prizes: ['$3,000 First Place', 'Developer Tools', 'App Store Publication']
    },
    {
      id: 3,
      title: "AI for Good Hackathon",
      description: "Leverage artificial intelligence to solve real-world problems",
      category: 'ai',
      difficulty: 'advanced',
      teamSize: '3-6 members',
      duration: '96 hours',
      technologies: ['Python', 'TensorFlow', 'PyTorch', 'Cloud APIs'],
      prizes: ['$10,000 Grand Prize', 'Research Collaboration', 'Conference Speaking']
    }
  ];

  const teammates: TeamMember[] = [
    {
      id: 1,
      name: "Alex Chen",
      role: "Full-Stack Developer",
      skills: ["React", "Node.js", "Python", "AWS"],
      experience: 'intermediate',
      avatar: '👨‍💻'
    },
    {
      id: 2,
      name: "Sarah Johnson",
      role: "UI/UX Designer",
      skills: ["Figma", "Adobe XD", "User Research", "Prototyping"],
      experience: 'expert',
      avatar: '👩‍🎨'
    },
    {
      id: 3,
      name: "Michael Rodriguez",
      role: "Data Scientist",
      skills: ["Python", "Machine Learning", "Statistics", "Visualization"],
      experience: 'intermediate',
      avatar: '👨‍🔬'
    },
    {
      id: 4,
      name: "Emily Zhang",
      role: "Mobile Developer",
      skills: ["React Native", "iOS", "Android", "Flutter"],
      experience: 'beginner',
      avatar: '👩‍💻'
    }
  ];

  const categoryColors = {
    web: 'from-blue-500 to-indigo-600',
    mobile: 'from-green-500 to-emerald-600',
    ai: 'from-purple-500 to-violet-600',
    blockchain: 'from-yellow-500 to-orange-600',
    game: 'from-red-500 to-pink-600'
  };

  const categoryIcons = {
    web: '🌐',
    mobile: '📱',
    ai: '🤖',
    blockchain: '⛓️',
    game: '🎮'
  };

  const difficultyColors = {
    beginner: 'bg-green-600/20 text-green-400 border-green-600/30',
    intermediate: 'bg-yellow-600/20 text-yellow-400 border-yellow-600/30',
    advanced: 'bg-red-600/20 text-red-400 border-red-600/30'
  };

  const experienceColors = {
    beginner: 'bg-blue-600/20 text-blue-400',
    intermediate: 'bg-yellow-600/20 text-yellow-400',
    expert: 'bg-red-600/20 text-red-400'
  };

  const projectIdeas = [
    "Smart Study Planner with AI recommendations",
    "AR Library Navigation System",
    "Peer Tutoring Marketplace",
    "Campus Sustainability Tracker",
    "Mental Health Support Chatbot",
    "Virtual Lab Simulator",
    "Student Collaboration Platform",
    "Interactive Learning Games"
  ];
  
  const navigate=useNavigate()

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
          <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-orange-400 via-red-400 to-orange-400 mb-4">
            Quidditch Quest Arena
          </h1>
          <p className="text-parchment/70 text-lg mb-8">
            Form your team, choose your quest, and build something magical
          </p>

          {/* Flying Broomstick Animation */}
          <motion.div
            initial={{ x: -100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 1, delay: 0.3 }}
            className="relative mx-auto w-32 h-16 mb-8"
          >
            <motion.div
              animate={{ 
                y: [0, -5, 0],
                rotate: [0, 2, 0]
              }}
              transition={{ duration: 2, repeat: Infinity }}
              className="text-4xl"
            >
              🧹
            </motion.div>
            
            {/* Trailing sparkles */}
            {[...Array(5)].map((_, i) => (
              <motion.div
                key={i}
                animate={{
                  opacity: [0, 1, 0],
                  scale: [0, 1, 0],
                  x: [0, -20, -40]
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: i * 0.2
                }}
                className="absolute top-2 left-8 w-1 h-1 bg-orange-400 rounded-full"
              />
            ))}
          </motion.div>
        </motion.div>

        {/* Tab Navigation */}
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="flex justify-center mb-8"
        >
          <div className="bg-slate-800/50 p-1 rounded-lg border border-orange-400/20">
            {[
              { id: 'projects', label: 'Hackathons', icon: RocketLaunchIcon },
              { id: 'team', label: 'Find Teammates', icon: UsersIcon },
              { id: 'ideas', label: 'Project Ideas', icon: LightBulbIcon }
            ].map((tab) => {
              const Icon = tab.icon;
              return (
                <motion.button
                  key={tab.id}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setSelectedTab(tab.id as any)}
                  className={`px-6 py-3 rounded-lg font-medium transition-all duration-300 flex items-center space-x-2 ${
                    selectedTab === tab.id
                      ? 'bg-gradient-to-r from-orange-600 to-red-600 text-white shadow-lg'
                      : 'text-parchment/70 hover:text-parchment hover:bg-slate-700/50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{tab.label}</span>
                </motion.button>
              );
            })}
          </div>
        </motion.div>

        {/* Content based on selected tab */}
        <motion.div
          key={selectedTab}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          {selectedTab === 'projects' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Projects List */}
              <div className="lg:col-span-2">
                <div className="space-y-6">
                  {projects.map((project, index) => (
                    <motion.div
                      key={project.id}
                      initial={{ x: -50, opacity: 0 }}
                      animate={{ x: 0, opacity: 1 }}
                      transition={{ duration: 0.6, delay: index * 0.1 }}
                      whileHover={{ scale: 1.02, y: -5 }}
                      onClick={() => setSelectedProject(project)}
                      className={`group cursor-pointer bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border backdrop-blur-sm transition-all duration-300 ${
                        selectedProject?.id === project.id
                          ? 'border-orange-400/50 shadow-xl'
                          : 'border-orange-400/20 hover:border-orange-400/40'
                      }`}
                    >
                      <div className="flex items-start space-x-4">
                        <div className={`w-16 h-16 rounded-lg bg-gradient-to-br ${categoryColors[project.category]} flex items-center justify-center text-2xl shadow-lg`}>
                          {categoryIcons[project.category]}
                        </div>

                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-3">
                            <h3 className="text-xl font-['Cormorant_Garamond'] text-parchment group-hover:text-orange-300 transition-colors">
                              {project.title}
                            </h3>
                            <span className={`px-3 py-1 rounded-full text-sm border ${difficultyColors[project.difficulty]}`}>
                              {project.difficulty}
                            </span>
                          </div>

                          <p className="text-parchment/70 leading-relaxed mb-4">
                            {project.description}
                          </p>

                          <div className="flex flex-wrap gap-2 mb-4">
                            {project.technologies.slice(0, 4).map((tech) => (
                              <span
                                key={tech}
                                className="px-2 py-1 bg-orange-600/20 text-orange-300 rounded text-sm border border-orange-600/30"
                              >
                                {tech}
                              </span>
                            ))}
                          </div>

                          <div className="flex items-center justify-between text-sm text-parchment/60">
                            <span>👥 {project.teamSize}</span>
                            <span>⏱️ {project.duration}</span>
                            <TrophyIcon className="w-4 h-4 text-gold" />
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>

              {/* Selected Project Details */}
              <div>
                <div className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border border-orange-400/20 backdrop-blur-sm sticky top-8">
                  <h2 className="text-xl font-['Cormorant_Garamond'] text-parchment mb-6 flex items-center space-x-2">
                    <RocketLaunchIcon className="w-6 h-6 text-orange-400" />
                    <span>Quest Details</span>
                  </h2>

                  {selectedProject ? (
                    <div className="space-y-4">
                      <div className={`w-16 h-16 rounded-lg bg-gradient-to-br ${categoryColors[selectedProject.category]} flex items-center justify-center text-2xl mx-auto mb-4`}>
                        {categoryIcons[selectedProject.category]}
                      </div>

                      <h3 className="text-lg font-medium text-parchment text-center">
                        {selectedProject.title}
                      </h3>

                      <div className="space-y-3">
                        <div>
                          <h4 className="text-parchment/70 font-medium mb-2">Technologies:</h4>
                          <div className="flex flex-wrap gap-2">
                            {selectedProject.technologies.map((tech) => (
                              <span
                                key={tech}
                                className="px-2 py-1 bg-orange-600/20 text-orange-300 rounded text-sm"
                              >
                                {tech}
                              </span>
                            ))}
                          </div>
                        </div>

                        <div>
                          <h4 className="text-parchment/70 font-medium mb-2">Prizes:</h4>
                          <ul className="space-y-1">
                            {selectedProject.prizes.map((prize, i) => (
                              <li key={i} className="text-parchment/80 text-sm flex items-center space-x-2">
                                <TrophyIcon className="w-4 h-4 text-gold" />
                                <span>{prize}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>

                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="w-full mt-6 py-3 bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-lg hover:from-orange-500 hover:to-red-500 transition-colors shadow-lg"
                      >
                        Join Quest
                      </motion.button>
                    </div>
                  ) : (
                    <div className="text-center text-parchment/50 py-12">
                      <RocketLaunchIcon className="w-12 h-12 mx-auto mb-4 opacity-50" />
                      <p>Select a hackathon to view details</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {selectedTab === 'team' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {teammates.map((member, index) => (
                <motion.div
                  key={member.id}
                  initial={{ y: 50, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  whileHover={{ scale: 1.05, y: -5 }}
                  className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border border-orange-400/20 backdrop-blur-sm hover:border-orange-400/40 transition-all duration-300 text-center"
                >
                  <div className="text-4xl mb-4">{member.avatar}</div>
                  
                  <h3 className="text-lg font-medium text-parchment mb-2">
                    {member.name}
                  </h3>
                  
                  <p className="text-parchment/70 mb-3">{member.role}</p>
                  
                  <div className={`inline-block px-3 py-1 rounded-full text-xs border mb-4 ${experienceColors[member.experience]}`}>
                    {member.experience}
                  </div>
                  
                  <div className="space-y-2 mb-4">
                    {member.skills.slice(0, 3).map((skill) => (
                      <span
                        key={skill}
                        className="inline-block px-2 py-1 bg-slate-700/50 text-parchment/80 rounded text-xs mr-1"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                  
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="w-full py-2 bg-gradient-to-r from-orange-600/20 to-red-600/20 text-orange-300 border border-orange-400/30 rounded-lg hover:border-orange-400/50 transition-colors"
                  >
                    Invite to Team
                  </motion.button>
                </motion.div>
              ))}
            </div>
          )}

          {selectedTab === 'ideas' && (
            <div className="max-w-4xl mx-auto">
              <div className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-8 border border-orange-400/20 backdrop-blur-sm">
                <h2 className="text-2xl font-['Cormorant_Garamond'] text-parchment mb-8 text-center flex items-center justify-center space-x-2">
                  <LightBulbIcon className="w-6 h-6 text-orange-400" />
                  <span>Magical Project Ideas</span>
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {projectIdeas.map((idea, index) => (
                    <motion.div
                      key={index}
                      initial={{ scale: 0, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.5, delay: index * 0.1 }}
                      whileHover={{ scale: 1.05 }}
                      className="group p-4 bg-slate-700/30 rounded-lg border border-orange-400/20 hover:border-orange-400/40 transition-all duration-300 cursor-pointer"
                    >
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-gradient-to-br from-orange-500 to-red-600 rounded-full flex items-center justify-center text-white">
                          💡
                        </div>
                        <span className="text-parchment group-hover:text-orange-300 transition-colors">
                          {idea}
                        </span>
                      </div>
                    </motion.div>
                  ))}
                </div>

                <motion.div
                  initial={{ y: 30, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 1 }}
                  className="mt-8 text-center"
                >
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="px-8 py-3 bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-lg hover:from-orange-500 hover:to-red-500 transition-colors shadow-lg"
                  >
                    Generate More Ideas
                  </motion.button>
                </motion.div>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default QuidditchQuest;