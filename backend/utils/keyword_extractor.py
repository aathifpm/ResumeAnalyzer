import spacy
from collections import defaultdict
import re

class KeywordExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
        # Expanded skill patterns by category
        self.skill_patterns = {
            'Programming Languages': {
                'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 
                'kotlin', 'golang', 'rust', 'typescript', 'scala', 'perl', 'r'
            },
            'Web Technologies': {
                'html', 'css', 'html5', 'css3', 'xml', 'json', 'rest', 'api',
                'websocket', 'sass', 'less', 'webpack', 'babel'
            },
            'Frameworks & Libraries': {
                'django', 'flask', 'fastapi', 'spring', 'react', 'angular', 'vue',
                'node.js', 'express', 'bootstrap', 'jquery', 'laravel', 'asp.net',
                'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn'
            },
            'Databases': {
                'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'sqlite', 
                'redis', 'elasticsearch', 'cassandra', 'dynamodb', 'firebase'
            },
            'Cloud & DevOps': {
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab',
                'terraform', 'ansible', 'circleci', 'travis', 'nginx', 'apache'
            },
            'Tools & Version Control': {
                'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence',
                'slack', 'vscode', 'intellij', 'eclipse', 'postman'
            },
            'Soft Skills': {
                'leadership', 'communication', 'teamwork', 'problem solving',
                'analytical', 'project management', 'agile', 'scrum', 'kanban'
            }
        }

    def extract_keywords(self, text):
        text = text.lower()
        keywords_by_category = defaultdict(list)
        
        # Process text with spaCy
        doc = self.nlp(text)
        
        # Extract keywords by category
        for category, skills in self.skill_patterns.items():
            for skill in skills:
                # Use regex to find whole word matches only
                pattern = r'\b' + re.escape(skill) + r'\b'
                matches = re.findall(pattern, text)
                if matches:
                    # Count occurrences
                    count = len(matches)
                    keywords_by_category[category].append({
                        'keyword': skill,
                        'count': count,
                        'confidence': self._calculate_confidence(count)
                    })
        
        # Sort keywords by count within each category
        for category in keywords_by_category:
            keywords_by_category[category].sort(key=lambda x: x['count'], reverse=True)
        
        return dict(keywords_by_category)

    def _calculate_confidence(self, count):
        # Simple confidence calculation based on frequency
        if count >= 3:
            return "High"
        elif count == 2:
            return "Medium"
        else:
            return "Low"

    def calculate_relevance(self, keywords, job_requirements):
        # Flatten all found keywords
        all_keywords = set()
        for category in keywords.values():
            for item in category:
                all_keywords.add(item['keyword'])
        
        matches = set(job_requirements).intersection(all_keywords)
        return len(matches) / len(job_requirements) if job_requirements else 0
