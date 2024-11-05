import re
from datetime import datetime

class ATSAnalyzer:
    def __init__(self):
        self.scoring_weights = {
            'keyword_match': 0.30,
            'skill_relevance': 0.25,
            'section_completeness': 0.15,
            'format_quality': 0.15,
            'experience_match': 0.15
        }
        
        self.required_sections = {
            'contact': {'weight': 1.0, 'keywords': ['email', 'phone', 'address']},
            'education': {'weight': 0.8, 'keywords': ['degree', 'university', 'gpa']},
            'experience': {'weight': 1.0, 'keywords': ['work', 'job', 'position']},
            'skills': {'weight': 0.9, 'keywords': ['skills', 'technologies', 'tools']}
        }

    def calculate_ats_score(self, text, role_requirements, sections, skills_found):
        try:
            requirements = {
                'keywords': list(role_requirements.get('keywords', [])),
                'required_skills': list(role_requirements.get('keywords', [])),
                'required_years': role_requirements.get('required_years', 2)
            }
            
            scores = {
                'keyword_match': self._calculate_keyword_match(text, requirements),
                'skill_relevance': self._calculate_skill_relevance(skills_found, requirements),
                'section_completeness': self._calculate_section_score(sections),
                'format_quality': self._analyze_format_quality(text),
                'experience_match': self._analyze_experience_match(text, requirements)
            }
            
            final_score = sum(
                scores[metric] * self.scoring_weights[metric]
                for metric in scores
            )
            
            recommendations = self._generate_ats_recommendations(scores)
            
            return {
                'overall_score': round(final_score, 2),
                'detailed_scores': {k: round(float(v), 2) for k, v in scores.items()},
                'recommendations': [{'category': rec['category'], 'message': str(rec['message'])} 
                                  for rec in recommendations]
            }
            
        except Exception as e:
            print(f"Error in ATS analysis: {str(e)}")
            return {
                'overall_score': 50.0,
                'detailed_scores': {k: 50.0 for k in self.scoring_weights.keys()},
                'recommendations': [{'category': 'error', 'message': 'Error analyzing resume'}]
            }

    def _calculate_keyword_match(self, text, requirements):
        try:
            text = text.lower()
            total_keywords = len(requirements['keywords'])
            if total_keywords == 0:
                return 50.0
            matched = sum(1 for keyword in requirements['keywords'] 
                         if str(keyword).lower() in text)
            return float(matched / total_keywords * 100)
        except Exception:
            return 50.0

    def _calculate_skill_relevance(self, skills_found, requirements):
        try:
            if not requirements.get('required_skills') or not skills_found:
                return 50.0
            
            required_skills = {str(skill).lower() for skill in requirements['required_skills']}
            found_skills = {str(skill).lower() for skill in skills_found.keys()}
            
            if not required_skills:
                return 50.0
                
            matched_skills = required_skills.intersection(found_skills)
            return float(len(matched_skills) / len(required_skills) * 100)
        except Exception:
            return 50.0

    def _calculate_section_score(self, sections):
        try:
            total_weight = sum(section['weight'] for section in self.required_sections.values())
            if total_weight == 0:
                return 50.0
            earned_weight = sum(
                self.required_sections[section]['weight']
                for section, present in sections.items()
                if present and section in self.required_sections
            )
            return float(earned_weight / total_weight * 100)
        except Exception:
            return 50.0

    def _analyze_format_quality(self, text):
        try:
            format_score = 100.0
            penalties = {
                'long_paragraphs': 10,
                'inconsistent_spacing': 5,
                'special_characters': 5,
                'complex_formatting': 10
            }
            
            if len(max(text.split('\n'), key=len, default='')) > 500:
                format_score -= penalties['long_paragraphs']
            
            if '\t' in text or '  ' in text:
                format_score -= penalties['inconsistent_spacing']
                
            special_chars = sum(1 for char in text if not char.isalnum() 
                              and char not in ' .,()-:;/')
            if special_chars > 20:
                format_score -= penalties['special_characters']
                
            return max(0.0, float(format_score))
        except Exception:
            return 50.0

    def _analyze_experience_match(self, text, requirements):
        try:
            required_years = float(requirements.get('required_years', 0))
            years_found = []
            
            # Extract years of experience
            year_matches = re.findall(r'(\d+)[\+]?\s*(?:years?|yrs?)', text, re.IGNORECASE)
            years_found.extend(int(year) for year in year_matches if year.isdigit())
            
            # Extract from date ranges
            date_ranges = re.findall(r'(\d{4})\s*-\s*(?:present|current|\d{4})', text, re.IGNORECASE)
            current_year = datetime.now().year
            years_found.extend(current_year - int(year) for year in date_ranges if year.isdigit())
            
            if not years_found:
                return 50.0
                
            max_years = float(max(years_found))
            if max_years >= required_years:
                return 100.0
            return float(max_years / required_years * 100)
        except Exception:
            return 50.0

    def _generate_ats_recommendations(self, scores):
        recommendations = []
        
        if scores['keyword_match'] < 70:
            recommendations.append({
                'category': 'keywords',
                'message': 'Include more relevant keywords from the job description'
            })
            
        if scores['format_quality'] < 80:
            recommendations.append({
                'category': 'format',
                'message': 'Simplify formatting and avoid special characters'
            })
            
        if scores['section_completeness'] < 90:
            recommendations.append({
                'category': 'sections',
                'message': 'Ensure all essential sections are present and complete'
            })
            
        return recommendations