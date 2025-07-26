"""
Gemini AI Chat Service
Handles LLM conversations using Google Gemini API
"""

import os
import requests
from typing import Dict, Any

class GeminiChat:
    def __init__(self):
        self.api_key = "AIzaSyAt3bEvKqm3sqMt-YtbyREh-slufqpcJfs"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def chat(self, prompt: str, context: str = "", personality: str = "helpful") -> Dict[str, Any]:
        #Send a chat request to Gemini
        try:
            if not self.api_key:
                return self._fallback_response(prompt, personality)
            
            # Format the prompt with personality
            system_prompt = self._get_personality_prompt(personality)
            full_prompt = f"{system_prompt}\n\nContext: {context}\n\nUser: {prompt}\n\nAssistant:"
            
            url = f"{self.base_url}/gemini-2.0-flash:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": full_prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }
            headers = {
                    "Content-Type": "application/json"
                }
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    
                    return {
                        'success': True,
                        'response': content,
                        'model': 'gemini-2.0-flash',
                        'personality': personality
                    }
            print(f"[DEBUG] Gemini API status: {response.status_code}")
            print(f"[DEBUG] Gemini response: {response.text}")
            return self._fallback_response(prompt, personality)
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._fallback_response(prompt, personality)


    def _get_personality_prompt(self, personality: str) -> str:
        """Get system prompt based on personality"""
        personalities = {
            'hermione': "You are Hermione Granger from Harry Potter, brilliant and studious. Answer with detailed explanations and encourage learning. Be enthusiastic about knowledge and slightly perfectionist.",
            'riddlenet': "You are Tom Riddle from Harry Potter, an evolving AI diary companion. Respond with empathy and wisdom, adapting your tone to match the user's emotional state. Be supportive but honest.",
            'professor': "You are a wise Hogwarts professor. Provide educational guidance with patience and depth. Use analogies and encourage critical thinking.",
            'motivational': "You are an inspiring mentor. Provide encouragement and motivation while being realistic. Help users see their potential.",
            'helpful': "You are a knowledgeable and friendly assistant. Provide clear, helpful responses with a warm tone."
        }
        
        return personalities.get(personality, personalities['helpful'])
    
    def _fallback_response(self, prompt: str, personality: str) -> Dict[str, Any]:
        """Provide fallback responses when API is unavailable"""
        fallback_responses = {
            'hermione': "I'd love to help you learn more about this topic! While I can't access my full knowledge right now, I encourage you to explore this question further through research and practice.",
            'riddlenet': "Thank you for sharing with the Dark Lord. Your thoughts and feelings are valid, and I'm here to listen. Sometimes the best insights come from reflecting on our experiences.",
            'professor': "An excellent question! This is exactly the kind of inquiry that leads to deeper understanding. I encourage you to explore different perspectives on this topic.",
            'motivational': "You're asking great questions, and that shows your commitment to growth! Keep pushing forward - every challenge is an opportunity to learn something new.",
            'helpful': "I appreciate your question! While I'm experiencing some technical difficulties right now, I encourage you to keep exploring this topic."
        }
        
        return {
            'success': True,
            'response': fallback_responses.get(personality, fallback_responses['helpful']),
            'model': 'fallback',
            'personality': personality
        }

# Global instance
gemini_chat = GeminiChat()