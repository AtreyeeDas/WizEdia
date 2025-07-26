"""
Emotion Analysis Model
Preprocessing and analysis logic for emotional content
"""

import re
from typing import Dict, List, Any

class EmotionAnalyzer:
    def __init__(self):
        self.emotion_keywords = {
            'joy': [
                'happy', 'excited', 'thrilled', 'delighted', 'cheerful', 'elated',
                'joyful', 'pleased', 'content', 'satisfied', 'glad', 'euphoric'
            ],
            'sadness': [
                'sad', 'depressed', 'melancholy', 'gloomy', 'dejected', 'downhearted',
                'sorrowful', 'mournful', 'blue', 'unhappy', 'miserable', 'despondent'
            ],
            'anger': [
                'angry', 'furious', 'enraged', 'livid', 'irate', 'incensed',
                'irritated', 'annoyed', 'frustrated', 'mad', 'outraged', 'hostile'
            ],
            'fear': [
                'afraid', 'scared', 'terrified', 'frightened', 'anxious', 'worried',
                'nervous', 'panicked', 'alarmed', 'apprehensive', 'fearful', 'uneasy'
            ],
            'surprise': [
                'surprised', 'amazed', 'astonished', 'shocked', 'stunned', 'bewildered',
                'startled', 'astounded', 'flabbergasted', 'dumbfounded', 'speechless'
            ],
            'disgust': [
                'disgusted', 'revolted', 'repulsed', 'sickened', 'nauseated', 'appalled',
                'horrified', 'repelled', 'offended', 'disturbed', 'grossed out'
            ],
            'trust': [
                'trust', 'confident', 'secure', 'assured', 'certain', 'believing',
                'faithful', 'loyal', 'dependable', 'reliable', 'convinced'
            ],
            'anticipation': [
                'excited', 'eager', 'hopeful', 'expectant', 'optimistic', 'looking forward',
                'anticipating', 'awaiting', 'prepared', 'ready', 'enthusiastic'
            ]
        }
        
        self.intensity_modifiers = {
            'very': 1.5,
            'extremely': 2.0,
            'incredibly': 2.0,
            'really': 1.3,
            'quite': 1.2,
            'somewhat': 0.8,
            'slightly': 0.6,
            'a bit': 0.7,
            'kind of': 0.7,
            'sort of': 0.7
        }
        
        self.negation_words = [
            'not', 'no', 'never', 'nothing', 'nobody', 'nowhere',
            'neither', 'nor', 'none', 'hardly', 'scarcely', 'barely'
        ]
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for emotion analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation for context
        text = re.sub(r'[^\w\s.,!?;:]', '', text)
        
        return text.strip()
    
    def extract_emotion_features(self, text: str) -> Dict[str, Any]:
        """Extract emotion-related features from text"""
        preprocessed_text = self.preprocess_text(text)
        words = preprocessed_text.split()
        
        features = {
            'emotion_scores': {},
            'intensity_indicators': [],
            'negation_context': [],
            'emotional_phrases': [],
            'overall_sentiment': 'neutral'
        }
        
        # Calculate emotion scores
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            matches = []
            
            for keyword in keywords:
                if keyword in preprocessed_text:
                    # Check for intensity modifiers
                    intensity = self._get_intensity_modifier(preprocessed_text, keyword)
                    
                    # Check for negation
                    is_negated = self._is_negated(preprocessed_text, keyword)
                    
                    keyword_score = intensity
                    if is_negated:
                        keyword_score *= -0.5  # Reduce but don't completely negate
                    
                    score += keyword_score
                    matches.append({
                        'keyword': keyword,
                        'intensity': intensity,
                        'negated': is_negated,
                        'score': keyword_score
                    })
            
            features['emotion_scores'][emotion] = {
                'score': round(score, 2),
                'matches': matches
            }
        
        # Determine overall sentiment
        features['overall_sentiment'] = self._determine_overall_sentiment(features['emotion_scores'])
        
        # Extract emotional phrases
        features['emotional_phrases'] = self._extract_emotional_phrases(preprocessed_text)
        
        return features
    
    def _get_intensity_modifier(self, text: str, keyword: str) -> float:
        """Get intensity modifier for a keyword"""
        words = text.split()
        
        try:
            keyword_index = words.index(keyword)
            
            # Check words before the keyword
            for i in range(max(0, keyword_index - 3), keyword_index):
                word = words[i]
                if word in self.intensity_modifiers:
                    return self.intensity_modifiers[word]
            
            # Check words after the keyword
            for i in range(keyword_index + 1, min(len(words), keyword_index + 3)):
                word = words[i]
                if word in self.intensity_modifiers:
                    return self.intensity_modifiers[word]
        
        except ValueError:
            pass
        
        return 1.0  # Default intensity
    
    def _is_negated(self, text: str, keyword: str) -> bool:
        """Check if a keyword is negated"""
        words = text.split()
        
        try:
            keyword_index = words.index(keyword)
            
            # Check for negation words before the keyword
            for i in range(max(0, keyword_index - 4), keyword_index):
                if words[i] in self.negation_words:
                    return True
        
        except ValueError:
            pass
        
        return False
    
    def _determine_overall_sentiment(self, emotion_scores: Dict[str, Dict]) -> str:
        """Determine overall sentiment from emotion scores"""
        positive_emotions = ['joy', 'trust', 'anticipation']
        negative_emotions = ['sadness', 'anger', 'fear', 'disgust']
        
        positive_score = sum(
            emotion_scores.get(emotion, {}).get('score', 0)
            for emotion in positive_emotions
        )
        
        negative_score = sum(
            emotion_scores.get(emotion, {}).get('score', 0)
            for emotion in negative_emotions
        )
        
        if positive_score > negative_score + 0.5:
            return 'positive'
        elif negative_score > positive_score + 0.5:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_emotional_phrases(self, text: str) -> List[str]:
        """Extract emotionally significant phrases"""
        phrases = []
        
        # Simple phrase extraction based on punctuation and conjunctions
        sentences = re.split(r'[.!?;]', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Minimum length for meaningful phrases
                # Check if sentence contains emotional keywords
                contains_emotion = any(
                    keyword in sentence
                    for keywords in self.emotion_keywords.values()
                    for keyword in keywords
                )
                
                if contains_emotion:
                    phrases.append(sentence)
        
        return phrases[:5]  # Limit to 5 most relevant phrases
    
    def analyze_emotional_progression(self, text: str) -> Dict[str, Any]:
        """Analyze how emotions progress through the text"""
        sentences = re.split(r'[.!?]', text)
        progression = []
        
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                sentence_features = self.extract_emotion_features(sentence)
                
                # Get dominant emotion for this sentence
                dominant_emotion = self._get_dominant_emotion(sentence_features['emotion_scores'])
                
                progression.append({
                    'sentence_number': i + 1,
                    'text': sentence.strip(),
                    'dominant_emotion': dominant_emotion,
                    'sentiment': sentence_features['overall_sentiment']
                })
        
        return {
            'progression': progression,
            'emotional_arc': self._analyze_emotional_arc(progression),
            'stability': self._calculate_emotional_stability(progression)
        }
    
    def _get_dominant_emotion(self, emotion_scores: Dict[str, Dict]) -> str:
        """Get the dominant emotion from scores"""
        max_score = 0
        dominant_emotion = 'neutral'
        
        for emotion, data in emotion_scores.items():
            score = data.get('score', 0)
            if score > max_score:
                max_score = score
                dominant_emotion = emotion
        
        return dominant_emotion if max_score > 0.5 else 'neutral'
    
    def _analyze_emotional_arc(self, progression: List[Dict]) -> str:
        """Analyze the overall emotional arc"""
        if len(progression) < 2:
            return 'insufficient_data'
        
        sentiments = [p['sentiment'] for p in progression]
        
        # Simple arc analysis
        positive_count = sentiments.count('positive')
        negative_count = sentiments.count('negative')
        neutral_count = sentiments.count('neutral')
        
        if positive_count > negative_count:
            if sentiments[0] == 'negative' and sentiments[-1] == 'positive':
                return 'recovery'
            else:
                return 'generally_positive'
        elif negative_count > positive_count:
            if sentiments[0] == 'positive' and sentiments[-1] == 'negative':
                return 'decline'
            else:
                return 'generally_negative'
        else:
            return 'stable'
    
    def _calculate_emotional_stability(self, progression: List[Dict]) -> float:
        """Calculate emotional stability score"""
        if len(progression) < 2:
            return 1.0
        
        # Count sentiment changes
        changes = 0
        for i in range(1, len(progression)):
            if progression[i]['sentiment'] != progression[i-1]['sentiment']:
                changes += 1
        
        # Stability is inverse of change frequency
        stability = 1.0 - (changes / (len(progression) - 1))
        return round(stability, 2)
    
    def get_emotion_recommendations(self, emotion_features: Dict[str, Any]) -> List[str]:
        """Get recommendations based on emotional analysis"""
        recommendations = []
        
        dominant_emotions = []
        for emotion, data in emotion_features['emotion_scores'].items():
            if data['score'] > 1.0:
                dominant_emotions.append(emotion)
        
        if 'sadness' in dominant_emotions or 'fear' in dominant_emotions:
            recommendations.extend([
                'Consider reaching out to friends, family, or a counselor for support',
                'Practice self-care activities that bring you comfort',
                'Remember that difficult emotions are temporary and will pass',
                'Try mindfulness or breathing exercises to help manage stress'
            ])
        
        if 'anger' in dominant_emotions:
            recommendations.extend([
                'Take some time to cool down before making important decisions',
                'Consider physical exercise to help release tension',
                'Practice expressing your feelings in a constructive way',
                'Identify the root cause of your anger to address it effectively'
            ])
        
        if 'joy' in dominant_emotions:
            recommendations.extend([
                'Savor this positive moment and reflect on what brought it about',
                'Consider sharing your joy with others who matter to you',
                'Think about how you can create more moments like this',
                'Use this positive energy to tackle challenges or help others'
            ])
        
        if not dominant_emotions:
            recommendations.extend([
                'Your emotional state seems balanced right now',
                'This might be a good time for reflection or planning',
                'Consider what activities or goals would bring you fulfillment',
                'Maintain this stability through consistent self-care practices'
            ])
        
        return recommendations[:4]  # Limit to 4 recommendations

# Global instance
emotion_analyzer = EmotionAnalyzer()