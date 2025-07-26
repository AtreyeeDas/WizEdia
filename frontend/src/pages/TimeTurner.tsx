import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ClockIcon, PlusIcon, CalendarIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

interface Event {
  id: number;
  title: string;
  description: string;
  date: Date;
  time: string;
  type: 'class' | 'assignment' | 'exam' | 'project' | 'personal';
}

const TimeTurner: React.FC = () => {
  const [events, setEvents] = useState<Event[]>([
    {
      id: 1,
      title: "Defense Against the Dark Arts",
      description: "Professor Lupin's lesson on Boggarts",
      date: new Date('2024-01-20'),
      time: '09:00',
      type: 'class'
    },
    {
      id: 2,
      title: "Potions Essay Due",
      description: "Write about the properties of Veritaserum",
      date: new Date('2024-01-22'),
      time: '23:59',
      type: 'assignment'
    },
    {
      id: 3,
      title: "Transfiguration Exam",
      description: "Professor McGonagall's midterm examination",
      date: new Date('2024-01-25'),
      time: '14:00',
      type: 'exam'
    }
  ]);

  const [selectedDate, setSelectedDate] = useState(new Date());
  const [showAddEvent, setShowAddEvent] = useState(false);
  const [newEvent, setNewEvent] = useState<Partial<Event>>({
    title: '',
    description: '',
    time: '09:00',
    type: 'class'
  });

  const typeColors = {
    class: 'from-blue-500 to-indigo-600',
    assignment: 'from-yellow-500 to-orange-600',
    exam: 'from-red-500 to-pink-600',
    project: 'from-green-500 to-emerald-600',
    personal: 'from-purple-500 to-violet-600'
  };

  const typeIcons = {
    class: '📚',
    assignment: '📝',
    exam: '📋',
    project: '🚀',
    personal: '⭐'
  };

  const currentTime = new Date();

  const handleAddEvent = () => {
    if (newEvent.title && newEvent.description) {
      const event: Event = {
        id: Date.now(),
        title: newEvent.title,
        description: newEvent.description!,
        date: selectedDate,
        time: newEvent.time!,
        type: newEvent.type!
      };
      setEvents([...events, event]);
      setNewEvent({ title: '', description: '', time: '09:00', type: 'class' });
      setShowAddEvent(false);
    }
  };

  const getUpcomingEvents = () => {
    return events
      .filter(event => event.date >= currentTime)
      .sort((a, b) => a.date.getTime() - b.date.getTime())
      .slice(0, 5);
  };

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
          <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-yellow-400 to-amber-400 mb-4">
            Time Turner Scheduler
          </h1>
          <p className="text-parchment/70 text-lg mb-8">
            Master time itself and never miss an important moment
          </p>

          {/* Time Turner Animation */}
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 1, delay: 0.3 }}
            className="relative mx-auto w-32 h-32 mb-8"
          >
            {/* Outer Ring */}
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="absolute inset-0 border-4 border-gold/30 rounded-full"
            >
              <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-2 w-2 h-4 bg-gold rounded-full" />
              <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 translate-y-2 w-2 h-4 bg-gold rounded-full" />
              <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -translate-x-2 w-4 h-2 bg-gold rounded-full" />
              <div className="absolute right-0 top-1/2 transform -translate-y-1/2 translate-x-2 w-4 h-2 bg-gold rounded-full" />
            </motion.div>

            {/* Inner Clock */}
            <motion.div
              animate={{ rotate: -360 }}
              transition={{ duration: 12, repeat: Infinity, ease: "linear" }}
              className="absolute inset-4 bg-gradient-to-br from-amber-400/20 to-gold/40 rounded-full border-2 border-gold/50 flex items-center justify-center"
            >
              <ClockIcon className="w-8 h-8 text-gold" />
            </motion.div>

            {/* Time particles */}
            {[...Array(6)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute w-1 h-1 bg-amber-400 rounded-full"
                animate={{
                  scale: [0, 1, 0],
                  opacity: [0, 1, 0],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  delay: i * 0.3,
                }}
                style={{
                  left: `${50 + Math.cos(i * 60 * Math.PI / 180) * 40}%`,
                  top: `${50 + Math.sin(i * 60 * Math.PI / 180) * 40}%`,
                }}
              />
            ))}
          </motion.div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Calendar Section */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ x: -50, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border border-gold/20 backdrop-blur-sm mb-6"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-['Cormorant_Garamond'] text-parchment">
                  Magical Calendar
                </h2>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setShowAddEvent(true)}
                  className="inline-flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-amber-600 to-yellow-600 text-white rounded-lg hover:from-amber-500 hover:to-yellow-500 transition-colors shadow-lg"
                >
                  <PlusIcon className="w-5 h-5" />
                  <span>Add Event</span>
                </motion.button>
              </div>

              {/* Simple Calendar Grid */}
              <div className="grid grid-cols-7 gap-2 mb-4">
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
                  <div key={day} className="text-center p-2 text-parchment/70 font-medium">
                    {day}
                  </div>
                ))}
                
                {Array.from({ length: 35 }, (_, i) => {
                  const date = new Date();
                  date.setDate(date.getDate() - date.getDay() + i);
                  const hasEvent = events.some(event => 
                    event.date.toDateString() === date.toDateString()
                  );
                  const isToday = date.toDateString() === new Date().toDateString();
                  
                  return (
                    <motion.div
                      key={i}
                      whileHover={{ scale: 1.1 }}
                      onClick={() => setSelectedDate(date)}
                      className={`relative p-2 text-center cursor-pointer rounded-lg transition-colors ${
                        isToday 
                          ? 'bg-amber-600 text-white' 
                          : selectedDate.toDateString() === date.toDateString()
                          ? 'bg-amber-600/50 text-white'
                          : 'hover:bg-slate-700/50 text-parchment'
                      }`}
                    >
                      {date.getDate()}
                      {hasEvent && (
                        <div className="absolute bottom-1 right-1 w-2 h-2 bg-gold rounded-full" />
                      )}
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>

            {/* Add Event Form */}
            {showAddEvent && (
              <motion.div
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border border-gold/20 backdrop-blur-sm mb-6"
              >
                <h3 className="text-xl font-['Cormorant_Garamond'] text-parchment mb-4">
                  Schedule New Event
                </h3>
                
                <div className="space-y-4">
                  <input
                    type="text"
                    placeholder="Event title..."
                    value={newEvent.title}
                    onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
                    className="w-full p-3 bg-slate-700/50 border border-gold/20 rounded-lg text-parchment placeholder-parchment/50 focus:outline-none focus:ring-2 focus:ring-amber-400/50"
                  />
                  
                  <textarea
                    placeholder="Event description..."
                    value={newEvent.description}
                    onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })}
                    rows={3}
                    className="w-full p-3 bg-slate-700/50 border border-gold/20 rounded-lg text-parchment placeholder-parchment/50 resize-none focus:outline-none focus:ring-2 focus:ring-amber-400/50"
                  />
                  
                  <div className="grid grid-cols-2 gap-4">
                    <input
                      type="time"
                      value={newEvent.time}
                      onChange={(e) => setNewEvent({ ...newEvent, time: e.target.value })}
                      className="p-3 bg-slate-700/50 border border-gold/20 rounded-lg text-parchment focus:outline-none focus:ring-2 focus:ring-amber-400/50"
                    />
                    
                    <select
                      value={newEvent.type}
                      onChange={(e) => setNewEvent({ ...newEvent, type: e.target.value as Event['type'] })}
                      className="p-3 bg-slate-700/50 border border-gold/20 rounded-lg text-parchment focus:outline-none focus:ring-2 focus:ring-amber-400/50"
                    >
                      <option value="class">Class</option>
                      <option value="assignment">Assignment</option>
                      <option value="exam">Exam</option>
                      <option value="project">Project</option>
                      <option value="personal">Personal</option>
                    </select>
                  </div>
                  
                  <div className="flex space-x-3">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleAddEvent}
                      className="px-6 py-2 bg-gradient-to-r from-amber-600 to-yellow-600 text-white rounded-lg hover:from-amber-500 hover:to-yellow-500 transition-colors"
                    >
                      Save Event
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => setShowAddEvent(false)}
                      className="px-6 py-2 bg-slate-700/50 text-parchment/70 rounded-lg border border-slate-600/50 hover:border-slate-500/50 transition-colors"
                    >
                      Cancel
                    </motion.button>
                  </div>
                </div>
              </motion.div>
            )}
          </div>

          {/* Upcoming Events */}
          <div>
            <motion.div
              initial={{ x: 50, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="bg-gradient-to-br from-slate-800/60 to-slate-900/80 rounded-xl p-6 border border-gold/20 backdrop-blur-sm"
            >
              <h2 className="text-xl font-['Cormorant_Garamond'] text-parchment mb-6 flex items-center space-x-2">
                <CalendarIcon className="w-6 h-6 text-amber-400" />
                <span>Upcoming Events</span>
              </h2>
              
              <div className="space-y-4">
                {getUpcomingEvents().map((event, index) => (
                  <motion.div
                    key={event.id}
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                    className="bg-slate-700/30 rounded-lg p-4 border border-gold/10 hover:border-gold/20 transition-colors"
                  >
                    <div className="flex items-start space-x-3">
                      <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${typeColors[event.type]} flex items-center justify-center text-xl`}>
                        {typeIcons[event.type]}
                      </div>
                      
                      <div className="flex-1">
                        <h3 className="font-medium text-parchment mb-1">
                          {event.title}
                        </h3>
                        <p className="text-sm text-parchment/70 mb-2">
                          {event.description}
                        </p>
                        <div className="flex items-center space-x-2 text-xs text-amber-400">
                          <span>{event.date.toLocaleDateString()}</span>
                          <span>•</span>
                          <span>{event.time}</span>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
                
                {getUpcomingEvents().length === 0 && (
                  <div className="text-center text-parchment/50 py-8">
                    <ClockIcon className="w-12 h-12 mx-auto mb-3 opacity-50" />
                    <p>No upcoming events</p>
                  </div>
                )}
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TimeTurner;