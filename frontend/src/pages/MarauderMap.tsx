import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MapIcon, CalendarIcon, MapPinIcon, UsersIcon } from '@heroicons/react/24/outline';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';

interface Event {
  id: number;
  title: string;
  description: string;
  location: string;
  date: Date;
  type: 'workshop' | 'hackathon' | 'conference' | 'meetup' | 'webinar';
  attendees: number;
  isOnline: boolean;
  coordinates: { x: number; y: number };
}

const MarauderMap: React.FC = () => {
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(null);
  const [mapRevealed, setMapRevealed] = useState(false);

  const events: Event[] = [
    {
      id: 1,
      title: "React Advanced Patterns Workshop",
      description: "Deep dive into advanced React patterns and best practices",
      location: "Tech Hub Downtown",
      date: new Date('2025-08-15'),
      type: 'workshop',
      attendees: 45,
      isOnline: false,
      coordinates: { x: 25, y: 35 }
    },
    {
      id: 2,
      title: "Summer Hackathon 2025",
      description: "48-hour coding marathon with amazing prizes",
      location: "University Campus",
      date: new Date('2025-08-28'),
      type: 'hackathon',
      attendees: 120,
      isOnline: false,
      coordinates: { x: 60, y: 20 }
    },
    {
      id: 3,
      title: "AI & Machine Learning Conference",
      description: "Latest trends in artificial intelligence",
      location: "Convention Center",
      date: new Date('2025-09-05'),
      type: 'conference',
      attendees: 300,
      isOnline: true,
      coordinates: { x: 80, y: 60 }
    },
     {
      id: 4,
      title: "JavaScript Community Meetup",
      description: "Monthly gathering of JS developers",
      location: "Coffee & Code Cafe",
      date: new Date('2025-09-10'),
      type: 'meetup',
      attendees: 25,
      isOnline: false,
      coordinates: { x: 15, y: 70 }
    },
    {
      id: 5,
      title: "Web Performance Optimization",
      description: "Learn to make your websites lightning fast",
      location: "Online Platform",
      date: new Date('2025-09-15'),
      type: 'webinar',
      attendees: 80,
      isOnline: true,
      coordinates: { x: 45, y: 80 }
    }
  ];

  const typeColors = {
    workshop: 'from-blue-500 to-indigo-600',
    hackathon: 'from-purple-500 to-violet-600',
    conference: 'from-green-500 to-emerald-600',
    meetup: 'from-yellow-500 to-orange-600',
    webinar: 'from-red-500 to-pink-600'
  };

  const typeIcons = {
    workshop: '🛠️',
    hackathon: '💻',
    conference: '🎤',
    meetup: '☕',
    webinar: '📹'
  };

  // Generate animated footsteps
  const footsteps = Array.from({ length: 8 }, (_, i) => ({
    id: i,
    startX: Math.random() * 100,
    startY: Math.random() * 100,
    delay: Math.random() * 10,
    duration: 4 + Math.random() * 3
  }));

  // FIX: The most simple and reliable state toggle.
  const revealMap = () => {
    setMapRevealed(prev => !prev);
  };

  const selectEvent = (event: Event) => {
    setSelectedEvent(event);
  };
  
  const navigate=useNavigate()

  return (
    <div 
      className="min-h-screen"
      style={{
        backgroundImage: `url('/images/marauders.jpg')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
      }}
    >
       <Navbar />
       <div className="min-h-screen p-8 relative">
         {/* Dark overlay for better readability */}
         <div className="absolute inset-0 bg-black/40" />
         
         {/* Animated footsteps */}
         {footsteps.map((footstep) => (
           <motion.div
             key={footstep.id}
             className="absolute w-4 h-2 bg-black/60 rounded-full shadow-lg"
             style={{
               left: `${footstep.startX}%`,
               top: `${footstep.startY}%`,
             }}
             animate={{
               x: [0, 100],
               y: [0, 100],
               opacity: [0, 1, 0],
               scale: [0.5, 1, 0.5],
             }}
             transition={{
               duration: footstep.duration,
               repeat: Infinity,
               delay: footstep.delay,
               ease: "easeInOut"
             }}
           >
             {/* Additional shadow effect */}
             <div className="absolute inset-0 bg-black/40 rounded-full blur-sm" />
           </motion.div>
         ))}
         
         <div className="relative z-10 max-w-6xl mx-auto">
           <button
            onClick={() => navigate(-1)}
            className="absolute top-6 right-6 bg-rose-600/60 hover:bg-rose-500 text-parchment px-4 py-2 rounded-md border border-slate-500/50 shadow-md transition"
          >
            Back
          </button>
          {/* Header */}
          <motion.div
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-12"
          >
            <h1 className="text-4xl font-['Cormorant_Garamond'] font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-yellow-400 to-amber-400 mb-4">
              The Marauder's Map
            </h1>
            <p className="text-white/80 text-lg mb-8">
              "I solemnly swear I am up to no good" - Discover learning events near you
            </p>

            <button
              onClick={revealMap}
              className={`inline-flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-amber-600 to-yellow-600 text-white font-medium rounded-lg hover:from-amber-500 hover:to-yellow-500 transition-colors shadow-lg cursor-pointer`}
            >
              <MapIcon className="w-5 h-5" />
              <span>
                {mapRevealed ? 'Hide the Map' : 'Reveal the Map'}
              </span>
            </button>
          </motion.div>

          {/* FIX: Removed AnimatePresence and motion props from this div for stability */}
          {mapRevealed && (
            <div>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Map */}
                <div className="lg:col-span-2">
                  <div
                    className="bg-gradient-to-br from-amber-100/10 to-yellow-100/10 rounded-xl p-8 border-2 border-amber-400/30 backdrop-blur-sm relative overflow-hidden"
                    style={{
                      backgroundImage: `
                        radial-gradient(circle at 1px 1px, rgba(251, 191, 36, 0.1) 1px, transparent 0),
                        linear-gradient(45deg, rgba(251, 191, 36, 0.05) 25%, transparent 25%, transparent 75%, rgba(251, 191, 36, 0.05) 75%),
                        linear-gradient(-45deg, rgba(251, 191, 36, 0.05) 25%, transparent 25%, transparent 75%, rgba(251, 191, 36, 0.05) 75%)
                      `,
                      backgroundSize: '20px 20px, 40px 40px, 40px 40px'
                    }}
                  >
                     <div className="relative h-96 bg-gradient-to-br from-amber-50/5 to-yellow-50/5 rounded-lg border border-amber-400/20 overflow-hidden">
                       {events.map((event, index) => (
                         <motion.div // motion can stay on internal elements
                          key={event.id}
                          initial={{ scale: 0.5, opacity: 0 }}
                          animate={{ scale: 1, opacity: 1 }}
                          transition={{ duration: 0.4, delay: 0.2 + index * 0.1, ease: "backOut" }}
                          whileHover={{ scale: 1.2, zIndex: 10 }}
                          onClick={() => selectEvent(event)}
                          className="absolute cursor-pointer group"
                          style={{
                            left: `${event.coordinates.x}%`,
                            top: `${event.coordinates.y}%`,
                            transform: 'translate(-50%, -50%)'
                          }}
                        >
                          <div className={`w-8 h-8 rounded-full bg-gradient-to-br ${typeColors[event.type]} flex items-center justify-center text-white shadow-lg border-2 border-white/50`}>
                            <span className="text-sm">{typeIcons[event.type]}</span>
                          </div>
                          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 opacity-0 group-hover:opacity-100 transition-opacity bg-slate-800 text-white px-3 py-2 rounded-lg text-sm whitespace-nowrap border border-amber-400/20 z-10">
                            <div className="font-medium">{event.title}</div>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Event Details */}
                <div>
                  <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/90 rounded-xl p-6 border border-amber-400/20 backdrop-blur-sm sticky top-8">
                    <h2 className="text-xl font-['Cormorant_Garamond'] text-white mb-6 flex items-center space-x-2">
                      <CalendarIcon className="w-6 h-6 text-amber-400" />
                      <span>Event Details</span>
                    </h2>
                     {selectedEvent ? (
                        <div className="space-y-4">
                            <h3 className="text-lg font-medium text-white text-center">{selectedEvent.title}</h3>
                            <p className="text-white/80 text-sm leading-relaxed">{selectedEvent.description}</p>
                            <div className="space-y-3 pt-4 border-t border-amber-400/20">
                               <div className="flex items-center space-x-3 text-sm"><MapPinIcon className="w-4 h-4 text-amber-400" /> <span className="text-white/80">{selectedEvent.location}</span> {selectedEvent.isOnline && (<span className="px-2 py-1 bg-green-600/20 text-green-400 rounded text-xs">Online</span>)}</div>
                               <div className="flex items-center space-x-3 text-sm"><CalendarIcon className="w-4 h-4 text-amber-400" /><span className="text-white/80">{selectedEvent.date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</span></div>
                               <div className="flex items-center space-x-3 text-sm"><UsersIcon className="w-4 h-4 text-amber-400" /><span className="text-white/80">{selectedEvent.attendees} attendees</span></div>
                            </div>
                        </div>
                      ) : (
                        <div className="text-center text-white/50 py-12">
                          <MapIcon className="w-12 h-12 mx-auto mb-4 opacity-50" />
                          <p>Click on a map marker to view event details</p>
                        </div>
                      )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MarauderMap;