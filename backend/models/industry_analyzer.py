import json
import os
from collections import Counter

class IndustryAnalyzer:
    def __init__(self):
        self.industry_patterns = {
            'Technology': ['software', 'technology', 'programming', 'development', 'IT'],
            'Finance': ['banking', 'finance', 'investment', 'trading', 'financial'],
            'Healthcare': ['medical', 'healthcare', 'clinical', 'health', 'patient'],
            'Manufacturing': ['manufacturing', 'production', 'industrial', 'assembly'],
            'Retail': ['retail', 'sales', 'customer service', 'merchandising'],
            'Education': ['education', 'teaching', 'academic', 'training'],
        }
        
        self.benchmarks = {
            'Technology': {
                'required_skills': ['programming', 'software development', 'agile'],
                'preferred_skills': ['cloud computing', 'devops', 'machine learning']
            },
            'Finance': {
                'required_skills': ['financial analysis', 'excel', 'modeling'],
                'preferred_skills': ['python', 'sql', 'risk management']
            },
            # Add more industry benchmarks as needed
        }

    def load_industry_patterns(self):
        try:
            with open('backend/data/industry_patterns.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: industry_patterns.json not found. Using default patterns.")
            return {
                "Technology": [
                    "Software", "Development", "Programming", "IT", "Technical"
                ],
                "Finance": [
                    "Banking", "Investment", "Trading", "Financial", "Accounting"
                ],
                "Healthcare": [
                    "Medical", "Clinical", "Healthcare", "Patient", "Hospital"
                ]
            }

    def load_industry_benchmarks(self):
        try:
            with open('backend/data/industry_benchmarks.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: industry_benchmarks.json not found. Using default benchmarks.")
            return {
                "Technology": {
                    "required_skills": ["Programming", "Software Development"],
                    "minimum_experience": 2,
                    "skill_weights": {
                        "technical_skills": 0.6,
                        "soft_skills": 0.2,
                        "tools": 0.2
                    }
                }
            }

    def detect_industry(self, text):
        industry_scores = {}
        for industry, patterns in self.industry_patterns.items():
            score = sum(1 for pattern in patterns if pattern.lower() in text.lower())
            industry_scores[industry] = score
        
        # Return industry with highest score, default to "Technology" if no matches
        if not industry_scores or max(industry_scores.values()) == 0:
            return "Technology"
        return max(industry_scores.items(), key=lambda x: x[1])[0]

    def calculate_match_score(self, skills, benchmark):
        if not benchmark or not skills:
            return 50  # Default score if no benchmark or skills
        
        required_skills = set(benchmark.get('required_skills', []))
        candidate_skills = set(skills.keys())
        
        matched_skills = required_skills.intersection(candidate_skills)
        score = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 50
        
        return min(100, max(0, score))

    def identify_missing_skills(self, skills, benchmark):
        if not benchmark or not skills:
            return []
            
        required_skills = set(benchmark.get('required_skills', []))
        candidate_skills = set(skills.keys())
        
        return list(required_skills - candidate_skills)

    def generate_recommendations(self, skills, benchmark):
        recommendations = []
        missing_skills = self.identify_missing_skills(skills, benchmark)
        
        if missing_skills:
            recommendations.append(f"Consider acquiring these skills: {', '.join(missing_skills)}")
        
        return recommendations or ["No specific recommendations at this time."]

    def analyze_industry_fit(self, resume_text, skills):
        detected_industry = self.detect_industry(resume_text)
        benchmark = self.benchmarks.get(detected_industry, {})
        
        analysis = {
            'industry': detected_industry,
            'match_score': self.calculate_match_score(skills, benchmark),
            'missing_skills': self.identify_missing_skills(skills, benchmark),
            'recommendations': self.generate_recommendations(skills, benchmark)
        }
        
        return analysis 