"""
SerpAPI Integration for Search and YouTube Content Discovery
Handles search queries and content recommendations using SerpAPI
"""

import os
import requests
from typing import Dict, List, Any

class SerpAPIService:
    def __init__(self):
        self.api_key = os.getenv('SERP_API_KEY')
        self.base_url = "https://serpapi.com/search"
    
    def search_educational_content(self, query: str, content_type: str = 'all') -> Dict[str, Any]:
        """Search for educational content using SerpAPI"""
        try:
            if not self.api_key:
                return self._get_mock_search_results(query, content_type)
            
            # Prepare search parameters
            params = {
                'api_key': self.api_key,
                'engine': 'google',
                'q': f"{query} educational tutorial learning",
                'num': 20
            }
            
            # Add content type specific parameters
            if content_type == 'videos':
                params['tbm'] = 'vid'
            elif content_type == 'academic':
                params['q'] += ' site:edu OR site:scholar.google.com'
            elif content_type == 'courses':
                params['q'] += ' course OR tutorial OR lesson'
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Process and format results
                formatted_results = self._format_search_results(data, content_type)
                
                return {
                    'success': True,
                    'query': query,
                    'content_type': content_type,
                    'results': formatted_results,
                    'total_results': len(formatted_results)
                }
            else:
                return self._get_mock_search_results(query, content_type)
                
        except Exception as e:
            print(f"SerpAPI search error: {e}")
            return self._get_mock_search_results(query, content_type)
    
    def search_youtube_educational(self, query: str, subject: str = 'general') -> Dict[str, Any]:
        """Search for educational YouTube videos"""
        try:
            if not self.api_key:
                return self._get_mock_youtube_results(query, subject)
            
            params = {
                'api_key': self.api_key,
                'engine': 'youtube',
                'search_query': f"{query} {subject} tutorial education",
                'num': 15
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Process YouTube results
                youtube_results = self._format_youtube_results(data)
                
                # Filter and rank by educational value
                educational_videos = self._filter_educational_content(youtube_results)
                
                return {
                    'success': True,
                    'query': query,
                    'subject': subject,
                    'videos': educational_videos,
                    'total_videos': len(educational_videos)
                }
            else:
                return self._get_mock_youtube_results(query, subject)
                
        except Exception as e:
            print(f"YouTube search error: {e}")
            return self._get_mock_youtube_results(query, subject)
    
    def search_academic_papers(self, query: str, field: str = 'general') -> Dict[str, Any]:
        """Search for academic papers and research"""
        try:
            if not self.api_key:
                return self._get_mock_academic_results(query, field)
            
            # Search Google Scholar
            params = {
                'api_key': self.api_key,
                'engine': 'google_scholar',
                'q': query,
                'num': 20,
                'as_ylo': '2020'  # Papers from 2020 onwards
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Process academic results
                academic_results = self._format_academic_results(data)
                
                return {
                    'success': True,
                    'query': query,
                    'field': field,
                    'papers': academic_results,
                    'total_papers': len(academic_results)
                }
            else:
                return self._get_mock_academic_results(query, field)
                
        except Exception as e:
            print(f"Academic search error: {e}")
            return self._get_mock_academic_results(query, field)
    
    def search_online_courses(self, subject: str, level: str = 'intermediate') -> Dict[str, Any]:
        """Search for online courses and MOOCs"""
        try:
            if not self.api_key:
                return self._get_mock_course_results(subject, level)
            
            # Search for courses on major platforms
            course_query = f"{subject} {level} course site:coursera.org OR site:edx.org OR site:udacity.com OR site:khanacademy.org"
            
            params = {
                'api_key': self.api_key,
                'engine': 'google',
                'q': course_query,
                'num': 15
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Process course results
                course_results = self._format_course_results(data)
                
                return {
                    'success': True,
                    'subject': subject,
                    'level': level,
                    'courses': course_results,
                    'total_courses': len(course_results)
                }
            else:
                return self._get_mock_course_results(subject, level)
                
        except Exception as e:
            print(f"Course search error: {e}")
            return self._get_mock_course_results(subject, level)
    
    def search_study_resources(self, topic: str, resource_type: str = 'all') -> Dict[str, Any]:
        """Search for study resources like practice tests, worksheets, etc."""
        try:
            if not self.api_key:
                return self._get_mock_study_resources(topic, resource_type)
            
            # Customize search based on resource type
            search_terms = {
                'practice_tests': f"{topic} practice test quiz exam",
                'worksheets': f"{topic} worksheet exercises problems",
                'study_guides': f"{topic} study guide notes summary",
                'flashcards': f"{topic} flashcards review cards",
                'all': f"{topic} study resources practice materials"
            }
            
            query = search_terms.get(resource_type, search_terms['all'])
            
            params = {
                'api_key': self.api_key,
                'engine': 'google',
                'q': query,
                'num': 20
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                # Process study resource results
                study_resources = self._format_study_resources(data, resource_type)
                
                return {
                    'success': True,
                    'topic': topic,
                    'resource_type': resource_type,
                    'resources': study_resources,
                    'total_resources': len(study_resources)
                }
            else:
                return self._get_mock_study_resources(topic, resource_type)
                
        except Exception as e:
            print(f"Study resources search error: {e}")
            return self._get_mock_study_resources(topic, resource_type)
    
    def _format_search_results(self, data: Dict, content_type: str) -> List[Dict[str, Any]]:
        """Format general search results"""
        results = []
        
        organic_results = data.get('organic_results', [])
        
        for result in organic_results:
            formatted_result = {
                'title': result.get('title', 'No Title'),
                'url': result.get('link', ''),
                'description': result.get('snippet', ''),
                'source': self._extract_domain(result.get('link', '')),
                'content_type': self._classify_content_type(result),
                'educational_score': self._calculate_educational_score(result)
            }
            
            # Add additional metadata if available
            if 'date' in result:
                formatted_result['date'] = result['date']
            
            results.append(formatted_result)
        
        # Sort by educational score
        results.sort(key=lambda x: x['educational_score'], reverse=True)
        
        return results[:15]  # Return top 15 results
    
    def _format_youtube_results(self, data: Dict) -> List[Dict[str, Any]]:
        """Format YouTube search results"""
        results = []
        
        video_results = data.get('video_results', [])
        
        for video in video_results:
            formatted_video = {
                'title': video.get('title', 'No Title'),
                'url': video.get('link', ''),
                'description': video.get('description', ''),
                'channel': video.get('channel', {}).get('name', 'Unknown Channel'),
                'duration': video.get('duration', 'Unknown'),
                'views': video.get('views', 0),
                'published_date': video.get('published_date', ''),
                'thumbnail': video.get('thumbnail', ''),
                'educational_indicators': self._identify_educational_indicators(video)
            }
            
            results.append(formatted_video)
        
        return results
    
    def _format_academic_results(self, data: Dict) -> List[Dict[str, Any]]:
        """Format academic paper results"""
        results = []
        
        organic_results = data.get('organic_results', [])
        
        for paper in organic_results:
            formatted_paper = {
                'title': paper.get('title', 'No Title'),
                'url': paper.get('link', ''),
                'authors': paper.get('publication_info', {}).get('authors', []),
                'publication': paper.get('publication_info', {}).get('summary', ''),
                'year': self._extract_year(paper.get('publication_info', {}).get('summary', '')),
                'citations': paper.get('inline_links', {}).get('cited_by', {}).get('total', 0),
                'abstract': paper.get('snippet', ''),
                'pdf_link': self._find_pdf_link(paper),
                'relevance_score': self._calculate_academic_relevance(paper)
            }
            
            results.append(formatted_paper)
        
        # Sort by relevance and citations
        results.sort(key=lambda x: (x['relevance_score'], x['citations']), reverse=True)
        
        return results[:12]  # Return top 12 papers
    
    def _format_course_results(self, data: Dict) -> List[Dict[str, Any]]:
        """Format online course results"""
        results = []
        
        organic_results = data.get('organic_results', [])
        
        for course in organic_results:
            platform = self._identify_course_platform(course.get('link', ''))
            
            formatted_course = {
                'title': course.get('title', 'No Title'),
                'url': course.get('link', ''),
                'description': course.get('snippet', ''),
                'platform': platform,
                'instructor': self._extract_instructor(course),
                'rating': self._extract_rating(course),
                'duration': self._extract_duration(course),
                'level': self._extract_course_level(course),
                'price': self._extract_price(course),
                'certificate': self._has_certificate(course, platform)
            }
            
            results.append(formatted_course)
        
        return results[:10]  # Return top 10 courses
    
    def _format_study_resources(self, data: Dict, resource_type: str) -> List[Dict[str, Any]]:
        """Format study resource results"""
        results = []
        
        organic_results = data.get('organic_results', [])
        
        for resource in organic_results:
            formatted_resource = {
                'title': resource.get('title', 'No Title'),
                'url': resource.get('link', ''),
                'description': resource.get('snippet', ''),
                'source': self._extract_domain(resource.get('link', '')),
                'resource_type': self._classify_study_resource_type(resource, resource_type),
                'difficulty_level': self._estimate_difficulty_level(resource),
                'format': self._identify_resource_format(resource),
                'quality_score': self._calculate_resource_quality_score(resource)
            }
            
            results.append(formatted_resource)
        
        # Sort by quality score
        results.sort(key=lambda x: x['quality_score'], reverse=True)
        
        return results[:12]  # Return top 12 resources
    
    def _filter_educational_content(self, videos: List[Dict]) -> List[Dict]:
        """Filter and rank videos by educational value"""
        educational_videos = []
        
        for video in videos:
            educational_score = 0
            
            # Check title for educational keywords
            title_lower = video['title'].lower()
            educational_keywords = [
                'tutorial', 'lesson', 'learn', 'course', 'education', 'teach',
                'explain', 'guide', 'how to', 'introduction', 'basics', 'fundamentals'
            ]
            
            for keyword in educational_keywords:
                if keyword in title_lower:
                    educational_score += 1
            
            # Check channel credibility
            channel = video['channel'].lower()
            credible_indicators = [
                'university', 'academy', 'education', 'school', 'institute',
                'professor', 'teacher', 'official'
            ]
            
            for indicator in credible_indicators:
                if indicator in channel:
                    educational_score += 2
            
            # Check duration (educational videos are usually longer)
            duration = video.get('duration', '')
            if any(indicator in duration for indicator in ['min', 'hour']) and not '1 min' in duration:
                educational_score += 1
            
            # Add educational score to video data
            video['educational_score'] = educational_score
            
            # Only include videos with some educational value
            if educational_score > 0:
                educational_videos.append(video)
        
        # Sort by educational score
        educational_videos.sort(key=lambda x: x['educational_score'], reverse=True)
        
        return educational_videos
    
    # Helper methods for data extraction and classification
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            return urlparse(url).netloc
        except:
            return 'unknown'
    
    def _classify_content_type(self, result: Dict) -> str:
        """Classify content type based on result data"""
        title = result.get('title', '').lower()
        url = result.get('link', '').lower()
        
        if any(indicator in url for indicator in ['youtube.com', 'vimeo.com']):
            return 'video'
        elif any(indicator in url for indicator in ['.edu', 'scholar.google']):
            return 'academic'
        elif any(indicator in title for indicator in ['course', 'tutorial', 'lesson']):
            return 'course'
        elif any(indicator in title for indicator in ['pdf', 'download']):
            return 'document'
        else:
            return 'article'
    
    def _calculate_educational_score(self, result: Dict) -> float:
        """Calculate educational value score"""
        score = 0.0
        
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()
        url = result.get('link', '').lower()
        
        # Educational keywords in title
        educational_keywords = [
            'tutorial', 'guide', 'learn', 'course', 'lesson', 'education',
            'teach', 'study', 'practice', 'exercise', 'example'
        ]
        
        for keyword in educational_keywords:
            if keyword in title:
                score += 0.3
            if keyword in snippet:
                score += 0.1
        
        # Credible domains
        credible_domains = [
            '.edu', 'khanacademy', 'coursera', 'edx', 'mit.edu',
            'stanford.edu', 'harvard.edu', 'wikipedia'
        ]
        
        for domain in credible_domains:
            if domain in url:
                score += 0.5
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _identify_educational_indicators(self, video: Dict) -> List[str]:
        """Identify educational indicators in video"""
        indicators = []
        
        title = video.get('title', '').lower()
        channel = video.get('channel', '').lower()
        
        if any(word in title for word in ['tutorial', 'lesson', 'course']):
            indicators.append('tutorial_content')
        
        if any(word in channel for word in ['university', 'academy', 'education']):
            indicators.append('educational_channel')
        
        if 'views' in video and video['views'] > 10000:
            indicators.append('popular_content')
        
        duration = video.get('duration', '')
        if any(indicator in duration for indicator in ['min', 'hour']):
            indicators.append('substantial_length')
        
        return indicators
    
    def _extract_year(self, publication_info: str) -> str:
        """Extract publication year from publication info"""
        import re
        year_match = re.search(r'\b(19|20)\d{2}\b', publication_info)
        return year_match.group() if year_match else 'Unknown'
    
    def _find_pdf_link(self, paper: Dict) -> str:
        """Find PDF link in paper data"""
        inline_links = paper.get('inline_links', {})
        
        for link_type, link_data in inline_links.items():
            if 'pdf' in link_type.lower():
                return link_data.get('link', '')
        
        return ''
    
    def _calculate_academic_relevance(self, paper: Dict) -> float:
        """Calculate academic relevance score"""
        score = 0.0
        
        # Citations boost relevance
        citations = paper.get('inline_links', {}).get('cited_by', {}).get('total', 0)
        if citations > 100:
            score += 0.5
        elif citations > 50:
            score += 0.3
        elif citations > 10:
            score += 0.1
        
        # Recent papers are more relevant
        year = self._extract_year(paper.get('publication_info', {}).get('summary', ''))
        if year.isdigit():
            year_int = int(year)
            if year_int >= 2020:
                score += 0.3
            elif year_int >= 2015:
                score += 0.2
        
        return score
    
    def _identify_course_platform(self, url: str) -> str:
        """Identify course platform from URL"""
        platforms = {
            'coursera.org': 'Coursera',
            'edx.org': 'edX',
            'udacity.com': 'Udacity',
            'khanacademy.org': 'Khan Academy',
            'udemy.com': 'Udemy',
            'pluralsight.com': 'Pluralsight',
            'linkedin.com/learning': 'LinkedIn Learning'
        }
        
        for domain, platform in platforms.items():
            if domain in url:
                return platform
        
        return 'Other'
    
    def _extract_instructor(self, course: Dict) -> str:
        """Extract instructor name from course data"""
        # This would typically parse the course description or title
        # For now, return a placeholder
        return 'Various Instructors'
    
    def _extract_rating(self, course: Dict) -> str:
        """Extract course rating"""
        snippet = course.get('snippet', '')
        import re
        
        # Look for rating patterns like "4.5 stars" or "4.5/5"
        rating_match = re.search(r'(\d+\.?\d*)\s*(?:stars?|/5|out of 5)', snippet)
        if rating_match:
            return f"{rating_match.group(1)}/5"
        
        return 'Not rated'
    
    def _extract_duration(self, course: Dict) -> str:
        """Extract course duration"""
        snippet = course.get('snippet', '')
        
        # Look for duration patterns
        duration_patterns = [
            r'(\d+)\s*weeks?',
            r'(\d+)\s*months?',
            r'(\d+)\s*hours?'
        ]
        
        for pattern in duration_patterns:
            import re
            match = re.search(pattern, snippet)
            if match:
                return match.group()
        
        return 'Self-paced'
    
    def _extract_course_level(self, course: Dict) -> str:
        """Extract course difficulty level"""
        text = (course.get('title', '') + ' ' + course.get('snippet', '')).lower()
        
        if any(word in text for word in ['beginner', 'intro', 'basic', 'fundamentals']):
            return 'Beginner'
        elif any(word in text for word in ['advanced', 'expert', 'master']):
            return 'Advanced'
        elif any(word in text for word in ['intermediate']):
            return 'Intermediate'
        else:
            return 'All Levels'
    
    def _extract_price(self, course: Dict) -> str:
        """Extract course price"""
        snippet = course.get('snippet', '')
        
        if any(word in snippet.lower() for word in ['free', 'no cost']):
            return 'Free'
        elif any(word in snippet.lower() for word in ['$', 'price', 'cost']):
            return 'Paid'
        else:
            return 'Unknown'
    
    def _has_certificate(self, course: Dict, platform: str) -> bool:
        """Check if course offers certificate"""
        text = (course.get('title', '') + ' ' + course.get('snippet', '')).lower()
        
        certificate_indicators = ['certificate', 'certification', 'credential']
        return any(indicator in text for indicator in certificate_indicators)
    
    def _classify_study_resource_type(self, resource: Dict, requested_type: str) -> str:
        """Classify study resource type"""
        title = resource.get('title', '').lower()
        url = resource.get('link', '').lower()
        
        if 'quiz' in title or 'test' in title:
            return 'practice_test'
        elif 'worksheet' in title or 'exercise' in title:
            return 'worksheet'
        elif 'guide' in title or 'notes' in title:
            return 'study_guide'
        elif 'flashcard' in title or 'cards' in title:
            return 'flashcards'
        elif '.pdf' in url:
            return 'document'
        else:
            return requested_type
    
    def _estimate_difficulty_level(self, resource: Dict) -> str:
        """Estimate difficulty level of resource"""
        text = (resource.get('title', '') + ' ' + resource.get('snippet', '')).lower()
        
        if any(word in text for word in ['basic', 'intro', 'beginner', 'elementary']):
            return 'Beginner'
        elif any(word in text for word in ['advanced', 'expert', 'graduate']):
            return 'Advanced'
        elif any(word in text for word in ['intermediate']):
            return 'Intermediate'
        else:
            return 'Mixed'
    
    def _identify_resource_format(self, resource: Dict) -> str:
        """Identify resource format"""
        url = resource.get('link', '').lower()
        title = resource.get('title', '').lower()
        
        if '.pdf' in url:
            return 'PDF'
        elif any(domain in url for domain in ['youtube.com', 'vimeo.com']):
            return 'Video'
        elif 'interactive' in title:
            return 'Interactive'
        else:
            return 'Web Page'
    
    def _calculate_resource_quality_score(self, resource: Dict) -> float:
        """Calculate resource quality score"""
        score = 0.0
        
        # Domain credibility
        url = resource.get('link', '').lower()
        credible_domains = ['.edu', 'khanacademy', 'coursera', 'mit', 'stanford']
        
        for domain in credible_domains:
            if domain in url:
                score += 0.4
                break
        
        # Title quality indicators
        title = resource.get('title', '').lower()
        quality_indicators = ['comprehensive', 'complete', 'guide', 'tutorial']
        
        for indicator in quality_indicators:
            if indicator in title:
                score += 0.2
        
        # Description quality
        snippet = resource.get('snippet', '')
        if len(snippet) > 100:  # Detailed description
            score += 0.2
        
        return min(score, 1.0)
    
    # Mock data methods for when API is unavailable
    
    def _get_mock_search_results(self, query: str, content_type: str) -> Dict[str, Any]:
        """Get mock search results"""
        mock_results = [
            {
                'title': f'{query} - Complete Tutorial Guide',
                'url': 'https://example-edu.com/tutorial',
                'description': f'Comprehensive tutorial covering all aspects of {query}',
                'source': 'example-edu.com',
                'content_type': 'tutorial',
                'educational_score': 0.9
            },
            {
                'title': f'Learn {query} - Free Online Course',
                'url': 'https://learning-platform.com/course',
                'description': f'Free online course for learning {query} from basics to advanced',
                'source': 'learning-platform.com',
                'content_type': 'course',
                'educational_score': 0.8
            }
        ]
        
        return {
            'success': True,
            'query': query,
            'content_type': content_type,
            'results': mock_results,
            'total_results': len(mock_results),
            'note': 'Mock data - connect SerpAPI for real results'
        }
    
    def _get_mock_youtube_results(self, query: str, subject: str) -> Dict[str, Any]:
        """Get mock YouTube results"""
        mock_videos = [
            {
                'title': f'{query} Explained - {subject} Tutorial',
                'url': 'https://youtube.com/watch?v=example1',
                'description': f'Clear explanation of {query} concepts in {subject}',
                'channel': 'Educational Channel',
                'duration': '15:30',
                'views': 125000,
                'published_date': '2 months ago',
                'thumbnail': 'https://img.youtube.com/vi/example1/default.jpg',
                'educational_indicators': ['tutorial_content', 'educational_channel'],
                'educational_score': 3
            },
            {
                'title': f'{subject} Fundamentals: {query}',
                'url': 'https://youtube.com/watch?v=example2',
                'description': f'Fundamental concepts of {query} in {subject}',
                'channel': 'University Lectures',
                'duration': '45:20',
                'views': 89000,
                'published_date': '1 month ago',
                'thumbnail': 'https://img.youtube.com/vi/example2/default.jpg',
                'educational_indicators': ['tutorial_content', 'educational_channel', 'substantial_length'],
                'educational_score': 4
            }
        ]
        
        return {
            'success': True,
            'query': query,
            'subject': subject,
            'videos': mock_videos,
            'total_videos': len(mock_videos),
            'note': 'Mock data - connect SerpAPI for real YouTube results'
        }
    
    def _get_mock_academic_results(self, query: str, field: str) -> Dict[str, Any]:
        """Get mock academic results"""
        mock_papers = [
            {
                'title': f'Recent Advances in {query}: A Comprehensive Review',
                'url': 'https://scholar.google.com/paper1',
                'authors': ['Dr. Smith', 'Prof. Johnson'],
                'publication': f'Journal of {field} Research, 2023',
                'year': '2023',
                'citations': 45,
                'abstract': f'This paper reviews recent developments in {query} research...',
                'pdf_link': 'https://example.edu/papers/paper1.pdf',
                'relevance_score': 0.8
            },
            {
                'title': f'Theoretical Framework for {query} Analysis',
                'url': 'https://scholar.google.com/paper2',
                'authors': ['Dr. Brown', 'Dr. Davis'],
                'publication': f'{field} Quarterly, 2022',
                'year': '2022',
                'citations': 78,
                'abstract': f'We present a new theoretical framework for analyzing {query}...',
                'pdf_link': 'https://example.edu/papers/paper2.pdf',
                'relevance_score': 0.7
            }
        ]
        
        return {
            'success': True,
            'query': query,
            'field': field,
            'papers': mock_papers,
            'total_papers': len(mock_papers),
            'note': 'Mock data - connect SerpAPI for real academic results'
        }
    
    def _get_mock_course_results(self, subject: str, level: str) -> Dict[str, Any]:
        """Get mock course results"""
        mock_courses = [
            {
                'title': f'Complete {subject} Course - {level} Level',
                'url': 'https://coursera.org/course1',
                'description': f'Comprehensive {level} course covering all {subject} topics',
                'platform': 'Coursera',
                'instructor': 'Prof. Expert',
                'rating': '4.7/5',
                'duration': '8 weeks',
                'level': level.title(),
                'price': 'Free',
                'certificate': True
            },
            {
                'title': f'{subject} Fundamentals for {level} Learners',
                'url': 'https://edx.org/course2',
                'description': f'Learn {subject} fundamentals at {level} level',
                'platform': 'edX',
                'instructor': 'Dr. Teacher',
                'rating': '4.5/5',
                'duration': '6 weeks',
                'level': level.title(),
                'price': 'Paid',
                'certificate': True
            }
        ]
        
        return {
            'success': True,
            'subject': subject,
            'level': level,
            'courses': mock_courses,
            'total_courses': len(mock_courses),
            'note': 'Mock data - connect SerpAPI for real course results'
        }
    
    def _get_mock_study_resources(self, topic: str, resource_type: str) -> Dict[str, Any]:
        """Get mock study resources"""
        mock_resources = [
            {
                'title': f'{topic} Practice Test - {resource_type}',
                'url': 'https://study-site.com/test1',
                'description': f'Comprehensive practice test for {topic}',
                'source': 'study-site.com',
                'resource_type': 'practice_test',
                'difficulty_level': 'Intermediate',
                'format': 'Interactive',
                'quality_score': 0.8
            },
            {
                'title': f'{topic} Study Guide and Worksheets',
                'url': 'https://education-hub.com/guide1',
                'description': f'Complete study guide with practice worksheets for {topic}',
                'source': 'education-hub.com',
                'resource_type': 'study_guide',
                'difficulty_level': 'Beginner',
                'format': 'PDF',
                'quality_score': 0.7
            }
        ]
        
        return {
            'success': True,
            'topic': topic,
            'resource_type': resource_type,
            'resources': mock_resources,
            'total_resources': len(mock_resources),
            'note': 'Mock data - connect SerpAPI for real study resources'
        }

# Global instance
serp_service = SerpAPIService()