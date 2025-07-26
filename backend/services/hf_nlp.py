"""
Hugging Face NLP Services
Handles emotion analysis and other NLP tasks using Hugging Face API
"""

import os
import requests
from typing import Dict, List, Any

class HuggingFaceNLP:
    def __init__(self):
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def analyze_emotion(self, text: str) -> Dict[str, Any]:
        """Analyze emotions in text using Hugging Face emotion model"""
        try:
            url = f"{self.base_url}/j-hartmann/emotion-english-distilroberta-base"
            
            payload = {
                "inputs": text,
                "options": {
                    "wait_for_model": True
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                emotions = response.json()
                
                # Format emotions for better readability
                if isinstance(emotions, list) and len(emotions) > 0:
                    emotion_list = emotions[0] if isinstance(emotions[0], list) else emotions
                    
                    # Sort by score and take top emotions
                    sorted_emotions = sorted(emotion_list, key=lambda x: x['score'], reverse=True)
                    
                    return {
                        'success': True,
                        'emotions': sorted_emotions[:3],  # Top 3 emotions
                        'primary_emotion': sorted_emotions[0]['label'] if sorted_emotions else 'neutral',
                        'confidence': sorted_emotions[0]['score'] if sorted_emotions else 0.0
                    }
            
            return {
                'success': False,
                'error': f'API request failed: {response.status_code}',
                'emotions': []
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Emotion analysis failed: {str(e)}',
                'emotions': []
            }
    
    def generate_text(self, prompt: str, model: str = "gpt2") -> Dict[str, Any]:
        """Generate text using Hugging Face language models"""
        try:
            url = f"{self.base_url}/{model}"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 150,
                    "temperature": 0.7,
                    "return_full_text": False
                },
                "options": {
                    "wait_for_model": True
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    
                    return {
                        'success': True,
                        'generated_text': generated_text,
                        'model_used': model
                    }
            
            return {
                'success': False,
                'error': f'Text generation failed: {response.status_code}',
                'generated_text': ''
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Text generation error: {str(e)}',
                'generated_text': ''
            }
    
    def classify_text(self, text: str, labels: List[str]) -> Dict[str, Any]:
        """Classify text into given categories"""
        try:
            url = f"{self.base_url}/facebook/bart-large-mnli"
            
            payload = {
                "inputs": text,
                "parameters": {
                    "candidate_labels": labels
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                return {
                    'success': True,
                    'classification': result,
                    'top_label': result.get('labels', [''])[0] if result.get('labels') else '',
                    'confidence': result.get('scores', [0])[0] if result.get('scores') else 0
                }
            
            return {
                'success': False,
                'error': f'Classification failed: {response.status_code}',
                'classification': {}
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Classification error: {str(e)}',
                'classification': {}
            }

# Global instance
hf_nlp = HuggingFaceNLP()