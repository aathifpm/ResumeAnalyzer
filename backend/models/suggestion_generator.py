from typing import Dict, List, Set
import random

class SuggestionGenerator:
    def __init__(self):
        self.skill_importance = {
            'software_engineer': {
                'critical': {'python', 'java', 'javascript', 'data structures', 'algorithms'},
                'important': {'git', 'sql', 'api development', 'testing'},
                'bonus': {'docker', 'aws', 'agile', 'microservices'}
            },
            'data_scientist': {
                'critical': {'python', 'machine learning', 'statistics', 'sql'},
                'important': {'tensorflow', 'pandas', 'numpy', 'data visualization'},
                'bonus': {'deep learning', 'big data', 'spark', 'cloud platforms'}
            },
            'web_developer': {
                'critical': {'html', 'css', 'javascript', 'react', 'responsive design'},
                'important': {'node.js', 'typescript', 'rest api', 'web security'},
                'bonus': {'webpack', 'graphql', 'sass', 'vue', 'angular'}
            },
            'devops_engineer': {
                'critical': {'docker', 'kubernetes', 'ci/cd', 'linux', 'aws'},
                'important': {'terraform', 'ansible', 'monitoring', 'automation'},
                'bonus': {'jenkins', 'configuration management', 'scalability'}
            },
            'mobile_developer': {
                'critical': {'android', 'ios', 'react native', 'mobile development'},
                'important': {'flutter', 'swift', 'kotlin', 'mobile testing'},
                'bonus': {'app store optimization', 'mobile security', 'ui/ux'}
            },
            'cloud_architect': {
                'critical': {'aws', 'azure', 'cloud architecture', 'microservices'},
                'important': {'cloud security', 'distributed systems', 'serverless'},
                'bonus': {'multi-cloud', 'cloud migration', 'hybrid cloud'}
            },
            'security_engineer': {
                'critical': {'cybersecurity', 'penetration testing', 'security audit'},
                'important': {'encryption', 'security protocols', 'incident response'},
                'bonus': {'ethical hacking', 'siem', 'vulnerability assessment'}
            },
            'data_engineer': {
                'critical': {'sql', 'etl', 'data warehouse', 'python'},
                'important': {'hadoop', 'spark', 'data modeling', 'data pipeline'},
                'bonus': {'airflow', 'kafka', 'data governance'}
            },
            'ml_engineer': {
                'critical': {'machine learning', 'python', 'deep learning', 'tensorflow'},
                'important': {'mlops', 'model deployment', 'feature engineering'},
                'bonus': {'model optimization', 'hyperparameter tuning', 'ml pipeline'}
            },
            'ui_ux_designer': {
                'critical': {'figma', 'user interface', 'user experience', 'wireframing'},
                'important': {'prototyping', 'user research', 'interaction design'},
                'bonus': {'adobe xd', 'sketch', 'accessibility', 'visual design'}
            },
            'qa_engineer': {
                'critical': {'test automation', 'selenium', 'test cases', 'api testing'},
                'important': {'quality assurance', 'regression testing', 'jira'},
                'bonus': {'performance testing', 'cypress', 'test planning'}
            },
            'blockchain_developer': {
                'critical': {'solidity', 'smart contracts', 'ethereum', 'web3'},
                'important': {'defi', 'cryptocurrency', 'distributed ledger'},
                'bonus': {'consensus mechanisms', 'nft', 'dapps'}
            },
            'game_developer': {
                'critical': {'unity', 'unreal engine', 'c++', 'game design'},
                'important': {'3d modeling', 'physics engine', 'animation'},
                'bonus': {'shader programming', 'game optimization', 'multiplayer'}
            },
            'embedded_systems': {
                'critical': {'c', 'embedded c', 'microcontrollers', 'firmware'},
                'important': {'rtos', 'embedded systems', 'hardware interfaces'},
                'bonus': {'arm', 'assembly', 'device drivers', 'embedded linux'}
            },
            'network_engineer': {
                'critical': {'cisco', 'networking', 'tcp/ip', 'routing'},
                'important': {'network security', 'vpn', 'firewall', 'wan'},
                'bonus': {'network protocols', 'network monitoring', 'network architecture'}
            }
        }
        
        self.improvement_templates = {
            'missing_critical': [
                "❗ Critical Skills Gap: Your resume lacks essential {role} skills: {skills}",
                "⚠️ Priority Focus Needed: Add these fundamental skills: {skills}",
            ],
            'missing_important': [
                "📈 Enhance Your Profile: Consider adding these important skills: {skills}",
                "💡 Skill Enhancement: Your profile would benefit from: {skills}",
            ],
            'missing_bonus': [
                "🌟 Stand Out More: These bonus skills could set you apart: {skills}",
                "✨ Extra Edge: Consider learning: {skills}",
            ],
            'section_improvements': {
                'experience': [
                    "💼 Experience Section: Add more quantifiable achievements (e.g., 'Increased efficiency by X%')",
                    "🎯 Impact: Highlight specific project outcomes and metrics",
                ],
                'education': [
                    "📚 Education: Include relevant coursework and certifications",
                    "🎓 Academic Projects: Highlight technical projects related to {role}",
                ],
                'skills': [
                    "🔧 Skills Section: Organize skills by categories (e.g., Languages, Tools, Frameworks)",
                    "⚡ Technical Proficiency: Add proficiency levels to your skills",
                ]
            },
            'format_suggestions': [
                "📋 Format: Use bullet points for better readability",
                "📱 Keywords: Optimize for ATS systems by including role-specific keywords",
                "📊 Layout: Ensure consistent formatting and spacing throughout",
            ]
        }

    def generate_suggestions(self, role: str, found_skills: Set[str], 
                           sections: Dict[str, bool]) -> List[Dict]:
        suggestions = []
        
        # Analyze skill gaps
        if role in self.skill_importance:
            role_skills = self.skill_importance[role]
            
            # Check critical skills
            missing_critical = role_skills['critical'] - found_skills
            if missing_critical:
                suggestions.append({
                    'type': 'critical',
                    'icon': '❗',
                    'title': 'Critical Skills Gap',
                    'message': random.choice(self.improvement_templates['missing_critical']).format(
                        role=role.replace('_', ' '),
                        skills=', '.join(missing_critical)
                    )
                })
            
            # Check important skills
            missing_important = role_skills['important'] - found_skills
            if missing_important:
                suggestions.append({
                    'type': 'important',
                    'icon': '📈',
                    'title': 'Important Skills',
                    'message': random.choice(self.improvement_templates['missing_important']).format(
                        skills=', '.join(missing_important)
                    )
                })
            
            # Check bonus skills
            missing_bonus = role_skills['bonus'] - found_skills
            if missing_bonus:
                suggestions.append({
                    'type': 'bonus',
                    'icon': '🌟',
                    'title': 'Bonus Skills',
                    'message': random.choice(self.improvement_templates['missing_bonus']).format(
                        skills=', '.join(missing_bonus)
                    )
                })

        # Section-specific suggestions
        for section, exists in sections.items():
            if not exists and section in self.improvement_templates['section_improvements']:
                suggestion = random.choice(
                    self.improvement_templates['section_improvements'][section]
                ).format(role=role.replace('_', ' '))
                suggestions.append({
                    'type': 'section',
                    'icon': '📝',
                    'title': f'Improve {section.title()} Section',
                    'message': suggestion
                })

        # Add format suggestions
        suggestions.append({
            'type': 'format',
            'icon': '📋',
            'title': 'Format Improvements',
            'message': random.choice(self.improvement_templates['format_suggestions'])
        })

        return suggestions 