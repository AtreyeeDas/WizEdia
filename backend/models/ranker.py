"""
Gamified Ranking and House Points System
Manages user progress, achievements, and house-based competition
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta
import json

class HousePointsSystem:
    def __init__(self):
        self.houses = {
            'gryffindor': {
                'name': 'Gryffindor',
                'traits': ['courage', 'bravery', 'nerve', 'chivalry'],
                'colors': ['#740001', '#D3A625'],
                'mascot': 'Lion',
                'element': 'Fire'
            },
            'hufflepuff': {
                'name': 'Hufflepuff', 
                'traits': ['hard work', 'patience', 'loyalty', 'fair play'],
                'colors': ['#FFDB00', '#000000'],
                'mascot': 'Badger',
                'element': 'Earth'
            },
            'ravenclaw': {
                'name': 'Ravenclaw',
                'traits': ['intelligence', 'wit', 'learning', 'wisdom'],
                'colors': ['#0E1A40', '#946B2D'],
                'mascot': 'Eagle',
                'element': 'Air'
            },
            'slytherin': {
                'name': 'Slytherin',
                'traits': ['ambition', 'cunning', 'leadership', 'resourcefulness'],
                'colors': ['#1A472A', '#AAAAAA'],
                'mascot': 'Serpent',
                'element': 'Water'
            }
        }
        
        self.point_activities = {
            'study_session': {
                'base_points': 10,
                'description': 'Completing a focused study session',
                'multipliers': {'duration': 0.5}  # 0.5 points per minute over 30 min
            },
            'quiz_completion': {
                'base_points': 15,
                'description': 'Completing a practice quiz',
                'multipliers': {'score': 1.0}  # 1 point per percentage point
            },
            'helping_peer': {
                'base_points': 25,
                'description': 'Helping a fellow student',
                'multipliers': {}
            },
            'assignment_submission': {
                'base_points': 20,
                'description': 'Submitting an assignment on time',
                'multipliers': {'quality': 0.5}  # Based on quality score
            },
            'research_contribution': {
                'base_points': 30,
                'description': 'Contributing to research or knowledge base',
                'multipliers': {}
            },
            'consistency_bonus': {
                'base_points': 50,
                'description': 'Maintaining study streak',
                'multipliers': {'streak_days': 2}  # 2 points per day in streak
            },
            'innovation_bonus': {
                'base_points': 40,
                'description': 'Creative problem solving or innovation',
                'multipliers': {}
            },
            'leadership_activity': {
                'base_points': 35,
                'description': 'Leading study groups or mentoring',
                'multipliers': {}
            }
        }
        
        self.achievements = {
            'first_steps': {
                'name': 'First Steps',
                'description': 'Complete your first study session',
                'points': 50,
                'icon': '👶',
                'rarity': 'common'
            },
            'knowledge_seeker': {
                'name': 'Knowledge Seeker',
                'description': 'Complete 10 study sessions',
                'points': 100,
                'icon': '📚',
                'rarity': 'common'
            },
            'scholar': {
                'name': 'Scholar',
                'description': 'Complete 50 study sessions',
                'points': 250,
                'icon': '🎓',
                'rarity': 'uncommon'
            },
            'master_learner': {
                'name': 'Master Learner',
                'description': 'Complete 100 study sessions',
                'points': 500,
                'icon': '🧙‍♂️',
                'rarity': 'rare'
            },
            'quiz_master': {
                'name': 'Quiz Master',
                'description': 'Score 90%+ on 5 consecutive quizzes',
                'points': 200,
                'icon': '🏆',
                'rarity': 'uncommon'
            },
            'helping_hand': {
                'name': 'Helping Hand',
                'description': 'Help 10 fellow students',
                'points': 300,
                'icon': '🤝',
                'rarity': 'uncommon'
            },
            'streak_warrior': {
                'name': 'Streak Warrior',
                'description': 'Maintain a 30-day study streak',
                'points': 400,
                'icon': '🔥',
                'rarity': 'rare'
            },
            'house_champion': {
                'name': 'House Champion',
                'description': 'Be the top contributor to your house this month',
                'points': 1000,
                'icon': '👑',
                'rarity': 'legendary'
            },
            'innovator': {
                'name': 'Innovator',
                'description': 'Contribute a creative solution or insight',
                'points': 350,
                'icon': '💡',
                'rarity': 'rare'
            },
            'mentor': {
                'name': 'Mentor',
                'description': 'Successfully mentor 5 students',
                'points': 600,
                'icon': '🧑‍🏫',
                'rarity': 'epic'
            }
        }
        
        self.leaderboard_categories = [
            'total_points',
            'weekly_points', 
            'monthly_points',
            'study_streak',
            'quiz_average',
            'helping_others',
            'consistency_score'
        ]
    
    def calculate_points(self, activity: str, **kwargs) -> Dict[str, Any]:
        """Calculate points for an activity"""
        if activity not in self.point_activities:
            return {'points': 0, 'error': 'Unknown activity'}
        
        activity_config = self.point_activities[activity]
        base_points = activity_config['base_points']
        multipliers = activity_config['multipliers']
        
        total_points = base_points
        calculation_details = {
            'base_points': base_points,
            'multipliers_applied': {},
            'total_points': base_points
        }
        
        # Apply multipliers
        for multiplier_key, multiplier_value in multipliers.items():
            if multiplier_key in kwargs:
                bonus = kwargs[multiplier_key] * multiplier_value
                total_points += bonus
                calculation_details['multipliers_applied'][multiplier_key] = {
                    'value': kwargs[multiplier_key],
                    'multiplier': multiplier_value,
                    'bonus_points': bonus
                }
        
        calculation_details['total_points'] = round(total_points)
        
        return {
            'points': round(total_points),
            'activity': activity,
            'description': activity_config['description'],
            'calculation': calculation_details
        }
    
    def assign_house(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Assign user to a house based on preferences and personality"""
        # Simple house assignment based on preferences
        # In a real implementation, this could use a more sophisticated algorithm
        
        preference_scores = {house: 0 for house in self.houses.keys()}
        
        # Analyze learning style preferences
        learning_style = user_preferences.get('learning_style', 'mixed')
        if learning_style == 'hands_on':
            preference_scores['gryffindor'] += 2
            preference_scores['hufflepuff'] += 1
        elif learning_style == 'analytical':
            preference_scores['ravenclaw'] += 2
            preference_scores['slytherin'] += 1
        elif learning_style == 'collaborative':
            preference_scores['hufflepuff'] += 2
            preference_scores['gryffindor'] += 1
        elif learning_style == 'independent':
            preference_scores['slytherin'] += 2
            preference_scores['ravenclaw'] += 1
        
        # Analyze goal preferences
        goals = user_preferences.get('goals', [])
        for goal in goals:
            goal_lower = goal.lower()
            if any(word in goal_lower for word in ['lead', 'manage', 'organize']):
                preference_scores['slytherin'] += 1
                preference_scores['gryffindor'] += 1
            elif any(word in goal_lower for word in ['help', 'support', 'collaborate']):
                preference_scores['hufflepuff'] += 2
            elif any(word in goal_lower for word in ['learn', 'understand', 'research']):
                preference_scores['ravenclaw'] += 2
            elif any(word in goal_lower for word in ['challenge', 'compete', 'achieve']):
                preference_scores['gryffindor'] += 1
                preference_scores['slytherin'] += 1
        
        # Analyze personality traits
        personality = user_preferences.get('personality_traits', [])
        for trait in personality:
            trait_lower = trait.lower()
            for house, house_data in self.houses.items():
                if any(house_trait in trait_lower for house_trait in house_data['traits']):
                    preference_scores[house] += 3
        
        # Find the house with highest score
        assigned_house = max(preference_scores, key=preference_scores.get)
        
        # If scores are tied, use a tiebreaker
        max_score = preference_scores[assigned_house]
        tied_houses = [house for house, score in preference_scores.items() if score == max_score]
        
        if len(tied_houses) > 1:
            # Use a simple tiebreaker (could be more sophisticated)
            assigned_house = tied_houses[0]
        
        return {
            'assigned_house': assigned_house,
            'house_data': self.houses[assigned_house],
            'preference_scores': preference_scores,
            'reasoning': self._generate_house_assignment_reasoning(assigned_house, user_preferences)
        }
    
    def _generate_house_assignment_reasoning(self, house: str, preferences: Dict[str, Any]) -> str:
        """Generate reasoning for house assignment"""
        house_data = self.houses[house]
        traits = ', '.join(house_data['traits'])
        
        reasoning = f"You've been sorted into {house_data['name']}! "
        reasoning += f"This house values {traits}, which aligns well with your preferences for "
        
        learning_style = preferences.get('learning_style', 'mixed')
        reasoning += f"{learning_style} learning"
        
        if preferences.get('goals'):
            reasoning += f" and your goals around {', '.join(preferences['goals'][:2])}"
        
        reasoning += f". As a {house_data['name']} student, you'll thrive in an environment that celebrates "
        reasoning += f"{house_data['traits'][0]} and {house_data['traits'][1]}."
        
        return reasoning
    
    def check_achievements(self, user_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check which achievements a user has earned"""
        earned_achievements = []
        
        for achievement_id, achievement in self.achievements.items():
            if self._is_achievement_earned(achievement_id, user_stats):
                earned_achievements.append({
                    'id': achievement_id,
                    **achievement,
                    'earned_date': datetime.now().isoformat()
                })
        
        return earned_achievements
    
    def _is_achievement_earned(self, achievement_id: str, user_stats: Dict[str, Any]) -> bool:
        """Check if a specific achievement is earned"""
        study_sessions = user_stats.get('study_sessions_completed', 0)
        quiz_scores = user_stats.get('quiz_scores', [])
        peers_helped = user_stats.get('peers_helped', 0)
        study_streak = user_stats.get('current_study_streak', 0)
        
        achievement_conditions = {
            'first_steps': study_sessions >= 1,
            'knowledge_seeker': study_sessions >= 10,
            'scholar': study_sessions >= 50,
            'master_learner': study_sessions >= 100,
            'quiz_master': self._check_quiz_master(quiz_scores),
            'helping_hand': peers_helped >= 10,
            'streak_warrior': study_streak >= 30,
            'house_champion': user_stats.get('monthly_house_rank', 10) == 1,
            'innovator': user_stats.get('innovations_contributed', 0) >= 1,
            'mentor': user_stats.get('students_mentored', 0) >= 5
        }
        
        return achievement_conditions.get(achievement_id, False)
    
    def _check_quiz_master(self, quiz_scores: List[float]) -> bool:
        """Check if user qualifies for Quiz Master achievement"""
        if len(quiz_scores) < 5:
            return False
        
        # Check last 5 scores for 90%+ consecutive
        recent_scores = quiz_scores[-5:]
        return all(score >= 90 for score in recent_scores)
    
    def generate_leaderboard(self, users_data: List[Dict[str, Any]], category: str = 'total_points') -> Dict[str, Any]:
        """Generate leaderboard for specified category"""
        if category not in self.leaderboard_categories:
            category = 'total_points'
        
        # Sort users by the specified category
        sorted_users = sorted(
            users_data,
            key=lambda x: x.get(category, 0),
            reverse=True
        )
        
        # Add rankings
        leaderboard = []
        for i, user in enumerate(sorted_users[:50]):  # Top 50
            leaderboard.append({
                'rank': i + 1,
                'user_id': user.get('user_id', 'unknown'),
                'username': user.get('username', 'Anonymous'),
                'house': user.get('house', 'unassigned'),
                'score': user.get(category, 0),
                'avatar': user.get('avatar', '🧙‍♂️'),
                'title': self._get_user_title(user)
            })
        
        # Calculate house standings
        house_standings = self._calculate_house_standings(users_data)
        
        return {
            'category': category,
            'leaderboard': leaderboard,
            'house_standings': house_standings,
            'total_participants': len(users_data),
            'last_updated': datetime.now().isoformat()
        }
    
    def _get_user_title(self, user: Dict[str, Any]) -> str:
        """Get user title based on achievements and stats"""
        total_points = user.get('total_points', 0)
        achievements_count = len(user.get('achievements', []))
        
        if total_points >= 10000:
            return 'Archmage'
        elif total_points >= 5000:
            return 'Master Wizard'
        elif total_points >= 2000:
            return 'Senior Scholar'
        elif total_points >= 1000:
            return 'Scholar'
        elif total_points >= 500:
            return 'Apprentice'
        elif achievements_count >= 5:
            return 'Achiever'
        else:
            return 'Student'
    
    def _calculate_house_standings(self, users_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate house standings based on total points"""
        house_totals = {house: 0 for house in self.houses.keys()}
        house_member_counts = {house: 0 for house in self.houses.keys()}
        
        for user in users_data:
            user_house = user.get('house', 'unassigned')
            if user_house in house_totals:
                house_totals[user_house] += user.get('total_points', 0)
                house_member_counts[user_house] += 1
        
        # Calculate average points per member
        house_standings = []
        for house, total_points in house_totals.items():
            member_count = house_member_counts[house]
            average_points = total_points / member_count if member_count > 0 else 0
            
            house_standings.append({
                'house': house,
                'house_name': self.houses[house]['name'],
                'total_points': total_points,
                'member_count': member_count,
                'average_points': round(average_points, 1),
                'colors': self.houses[house]['colors'],
                'mascot': self.houses[house]['mascot']
            })
        
        # Sort by total points
        house_standings.sort(key=lambda x: x['total_points'], reverse=True)
        
        # Add rankings
        for i, house in enumerate(house_standings):
            house['rank'] = i + 1
        
        return house_standings
    
    def calculate_consistency_score(self, user_activity: List[Dict[str, Any]]) -> float:
        """Calculate user's consistency score based on activity patterns"""
        if not user_activity:
            return 0.0
        
        # Analyze activity over the last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_activity = [
            activity for activity in user_activity
            if datetime.fromisoformat(activity.get('date', '2024-01-01')) >= thirty_days_ago
        ]
        
        if not recent_activity:
            return 0.0
        
        # Calculate daily activity
        daily_activity = {}
        for activity in recent_activity:
            date = activity.get('date', '2024-01-01')[:10]  # Get date part only
            if date not in daily_activity:
                daily_activity[date] = 0
            daily_activity[date] += 1
        
        # Calculate consistency metrics
        active_days = len(daily_activity)
        total_days = 30
        activity_rate = active_days / total_days
        
        # Calculate activity distribution (how evenly spread)
        if active_days > 1:
            activity_values = list(daily_activity.values())
            avg_activity = sum(activity_values) / len(activity_values)
            variance = sum((x - avg_activity) ** 2 for x in activity_values) / len(activity_values)
            distribution_score = 1 / (1 + variance)  # Lower variance = higher score
        else:
            distribution_score = 0.5
        
        # Combine metrics
        consistency_score = (activity_rate * 0.7) + (distribution_score * 0.3)
        
        return round(min(1.0, consistency_score), 2)
    
    def generate_progress_insights(self, user_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights about user's progress and suggestions"""
        insights = {
            'strengths': [],
            'areas_for_improvement': [],
            'recommendations': [],
            'next_achievements': [],
            'progress_summary': {}
        }
        
        # Analyze strengths
        total_points = user_stats.get('total_points', 0)
        study_streak = user_stats.get('current_study_streak', 0)
        quiz_average = user_stats.get('quiz_average', 0)
        consistency_score = user_stats.get('consistency_score', 0)
        
        if total_points > 1000:
            insights['strengths'].append('High overall achievement with significant point accumulation')
        
        if study_streak > 7:
            insights['strengths'].append(f'Excellent consistency with {study_streak}-day study streak')
        
        if quiz_average > 85:
            insights['strengths'].append(f'Strong academic performance with {quiz_average}% quiz average')
        
        if consistency_score > 0.7:
            insights['strengths'].append('Highly consistent learning pattern')
        
        # Identify areas for improvement
        if study_streak < 3:
            insights['areas_for_improvement'].append('Building consistent daily study habits')
        
        if quiz_average < 70:
            insights['areas_for_improvement'].append('Improving quiz performance and comprehension')
        
        if user_stats.get('peers_helped', 0) < 3:
            insights['areas_for_improvement'].append('Engaging more with peer learning and collaboration')
        
        if consistency_score < 0.5:
            insights['areas_for_improvement'].append('Developing more regular study patterns')
        
        # Generate recommendations
        insights['recommendations'] = self._generate_recommendations(user_stats)
        
        # Identify next achievable achievements
        insights['next_achievements'] = self._get_next_achievements(user_stats)
        
        # Progress summary
        insights['progress_summary'] = {
            'current_level': self._get_user_title(user_stats),
            'points_to_next_level': self._calculate_points_to_next_level(total_points),
            'completion_percentage': self._calculate_overall_completion(user_stats),
            'house_contribution': user_stats.get('house_points_contributed', 0)
        }
        
        return insights
    
    def _generate_recommendations(self, user_stats: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        study_streak = user_stats.get('current_study_streak', 0)
        quiz_average = user_stats.get('quiz_average', 0)
        peers_helped = user_stats.get('peers_helped', 0)
        
        if study_streak < 7:
            recommendations.append('Try to study for at least 15 minutes daily to build a strong streak')
        
        if quiz_average < 80:
            recommendations.append('Focus on active recall and practice testing to improve quiz scores')
        
        if peers_helped < 5:
            recommendations.append('Join study groups or help answer questions to earn collaboration points')
        
        if user_stats.get('total_points', 0) < 500:
            recommendations.append('Complete daily study sessions to steadily accumulate points')
        
        recommendations.append('Set specific learning goals for the week to maintain motivation')
        
        return recommendations[:4]  # Limit to 4 recommendations
    
    def _get_next_achievements(self, user_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get next achievable achievements"""
        next_achievements = []
        current_achievements = set(user_stats.get('achievements', []))
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id not in current_achievements:
                progress = self._calculate_achievement_progress(achievement_id, user_stats)
                if progress > 0:
                    next_achievements.append({
                        'id': achievement_id,
                        'name': achievement['name'],
                        'description': achievement['description'],
                        'points': achievement['points'],
                        'progress': progress,
                        'icon': achievement['icon']
                    })
        
        # Sort by progress (closest to completion first)
        next_achievements.sort(key=lambda x: x['progress'], reverse=True)
        
        return next_achievements[:5]  # Top 5 closest achievements
    
    def _calculate_achievement_progress(self, achievement_id: str, user_stats: Dict[str, Any]) -> float:
        """Calculate progress towards a specific achievement"""
        study_sessions = user_stats.get('study_sessions_completed', 0)
        peers_helped = user_stats.get('peers_helped', 0)
        study_streak = user_stats.get('current_study_streak', 0)
        
        progress_calculations = {
            'first_steps': min(1.0, study_sessions / 1),
            'knowledge_seeker': min(1.0, study_sessions / 10),
            'scholar': min(1.0, study_sessions / 50),
            'master_learner': min(1.0, study_sessions / 100),
            'helping_hand': min(1.0, peers_helped / 10),
            'streak_warrior': min(1.0, study_streak / 30),
            'mentor': min(1.0, user_stats.get('students_mentored', 0) / 5)
        }
        
        return progress_calculations.get(achievement_id, 0.0)
    
    def _calculate_points_to_next_level(self, current_points: int) -> int:
        """Calculate points needed to reach next title level"""
        level_thresholds = [500, 1000, 2000, 5000, 10000]
        
        for threshold in level_thresholds:
            if current_points < threshold:
                return threshold - current_points
        
        return 0  # Already at max level
    
    def _calculate_overall_completion(self, user_stats: Dict[str, Any]) -> float:
        """Calculate overall completion percentage"""
        # This is a simplified calculation
        # In a real system, this would be based on curriculum completion
        
        total_points = user_stats.get('total_points', 0)
        study_sessions = user_stats.get('study_sessions_completed', 0)
        achievements = len(user_stats.get('achievements', []))
        
        # Normalize different metrics to 0-1 scale
        points_score = min(1.0, total_points / 5000)  # 5000 points = 100%
        sessions_score = min(1.0, study_sessions / 100)  # 100 sessions = 100%
        achievements_score = min(1.0, achievements / 10)  # 10 achievements = 100%
        
        # Weighted average
        overall_completion = (points_score * 0.4) + (sessions_score * 0.4) + (achievements_score * 0.2)
        
        return round(overall_completion * 100, 1)  # Return as percentage
    
    def create_challenge(self, challenge_type: str, duration_days: int = 7) -> Dict[str, Any]:
        """Create a house or individual challenge"""
        challenges = {
            'study_streak': {
                'name': 'Study Streak Challenge',
                'description': f'Maintain a study streak for {duration_days} consecutive days',
                'goal': duration_days,
                'points_reward': duration_days * 10,
                'type': 'individual'
            },
            'house_collaboration': {
                'name': 'House Collaboration Challenge',
                'description': f'House members help each other for {duration_days} days',
                'goal': duration_days * 5,  # 5 helps per day
                'points_reward': 500,
                'type': 'house'
            },
            'quiz_mastery': {
                'name': 'Quiz Mastery Challenge',
                'description': f'Achieve 85%+ average on quizzes for {duration_days} days',
                'goal': 85,
                'points_reward': duration_days * 15,
                'type': 'individual'
            },
            'knowledge_sharing': {
                'name': 'Knowledge Sharing Challenge',
                'description': f'Share insights or help peers for {duration_days} days',
                'goal': duration_days * 2,  # 2 shares per day
                'points_reward': duration_days * 20,
                'type': 'individual'
            }
        }
        
        if challenge_type not in challenges:
            challenge_type = 'study_streak'
        
        challenge = challenges[challenge_type].copy()
        challenge.update({
            'id': f"{challenge_type}_{datetime.now().strftime('%Y%m%d')}",
            'start_date': datetime.now().isoformat(),
            'end_date': (datetime.now() + timedelta(days=duration_days)).isoformat(),
            'duration_days': duration_days,
            'participants': [],
            'status': 'active'
        })
        
        return challenge

# Global instance
house_points_system = HousePointsSystem()