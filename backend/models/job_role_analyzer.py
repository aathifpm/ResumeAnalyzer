from collections import defaultdict
import re

class JobRoleAnalyzer:
    def __init__(self):
        # Define job roles and their associated keywords
        self.job_roles = {
            'software_engineer': {
                'keywords': {
                    'python', 'java', 'javascript', 'software development', 'algorithms',
                    'data structures', 'git', 'api', 'backend', 'frontend', 'full stack',
                    'software engineering', 'object oriented', 'debugging', 'testing'
                },
                'weight': 1.0
            },
            'data_scientist': {
                'keywords': {
                    'machine learning', 'python', 'r', 'statistics', 'data analysis',
                    'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy',
                    'scikit-learn', 'data visualization', 'big data', 'neural networks',
                    'regression', 'classification', 'clustering'
                },
                'weight': 1.0
            },
            'web_developer': {
                'keywords': {
                    'html', 'css', 'javascript', 'react', 'angular', 'vue', 'node.js',
                    'frontend', 'responsive design', 'web development', 'sass', 'webpack',
                    'typescript', 'redux', 'rest api', 'graphql', 'web security'
                },
                'weight': 1.0
            },
            'devops_engineer': {
                'keywords': {
                    'aws', 'docker', 'kubernetes', 'jenkins', 'ci/cd', 'terraform',
                    'ansible', 'cloud', 'linux', 'automation', 'monitoring', 'security',
                    'infrastructure as code', 'configuration management', 'scalability'
                },
                'weight': 1.0
            },
            'mobile_developer': {
                'keywords': {
                    'android', 'ios', 'swift', 'kotlin', 'react native', 'flutter',
                    'mobile development', 'app development', 'ui/ux', 'mobile security',
                    'app store', 'play store', 'mobile testing', 'responsive design'
                },
                'weight': 1.0
            },
            'cloud_architect': {
                'keywords': {
                    'aws', 'azure', 'gcp', 'cloud architecture', 'microservices',
                    'distributed systems', 'cloud security', 'serverless', 'iaas',
                    'paas', 'saas', 'cloud migration', 'hybrid cloud', 'multi-cloud'
                },
                'weight': 1.2
            },
            'security_engineer': {
                'keywords': {
                    'cybersecurity', 'penetration testing', 'security audit', 'encryption',
                    'firewall', 'vulnerability assessment', 'security protocols', 'owasp',
                    'incident response', 'security tools', 'ethical hacking', 'siem'
                },
                'weight': 1.2
            },
            'data_engineer': {
                'keywords': {
                    'etl', 'data warehouse', 'sql', 'data modeling', 'data pipeline',
                    'hadoop', 'spark', 'airflow', 'kafka', 'data infrastructure',
                    'data architecture', 'data quality', 'data governance'
                },
                'weight': 1.1
            },
            'ml_engineer': {
                'keywords': {
                    'machine learning', 'deep learning', 'mlops', 'model deployment',
                    'model optimization', 'feature engineering', 'tensorflow', 'pytorch',
                    'model training', 'hyperparameter tuning', 'ml pipeline'
                },
                'weight': 1.2
            },
            'ui_ux_designer': {
                'keywords': {
                    'user interface', 'user experience', 'wireframing', 'prototyping',
                    'figma', 'sketch', 'adobe xd', 'user research', 'usability testing',
                    'interaction design', 'visual design', 'accessibility'
                },
                'weight': 1.0
            },
            'qa_engineer': {
                'keywords': {
                    'testing', 'test automation', 'selenium', 'junit', 'test cases',
                    'quality assurance', 'bug tracking', 'regression testing',
                    'performance testing', 'test planning', 'cypress', 'jira'
                },
                'weight': 1.0
            },
            'blockchain_developer': {
                'keywords': {
                    'blockchain', 'smart contracts', 'solidity', 'ethereum', 'web3',
                    'cryptocurrency', 'distributed ledger', 'consensus mechanisms',
                    'defi', 'nft', 'crypto', 'dapps'
                },
                'weight': 1.3
            },
            'game_developer': {
                'keywords': {
                    'unity', 'unreal engine', 'c++', 'game development', '3d modeling',
                    'game design', 'physics engine', 'animation', 'graphics programming',
                    'shader programming', 'game optimization', 'multiplayer', 'game mechanics'
                },
                'weight': 1.2
            },
            'embedded_systems': {
                'keywords': {
                    'c', 'embedded c', 'rtos', 'microcontrollers', 'firmware',
                    'embedded systems', 'arm', 'assembly', 'hardware interfaces',
                    'device drivers', 'bare metal programming', 'embedded linux'
                },
                'weight': 1.2
            },
            'network_engineer': {
                'keywords': {
                    'cisco', 'networking', 'tcp/ip', 'routing', 'switching',
                    'network security', 'vpn', 'firewall', 'wan', 'lan',
                    'network protocols', 'network monitoring', 'network architecture'
                },
                'weight': 1.1
            },
            'system_administrator': {
                'keywords': {
                    'linux', 'windows server', 'active directory', 'system administration',
                    'bash scripting', 'powershell', 'virtualization', 'backup solutions',
                    'troubleshooting', 'patch management', 'system monitoring'
                },
                'weight': 1.0
            },
            'database_administrator': {
                'keywords': {
                    'sql', 'oracle', 'mysql', 'postgresql', 'database administration',
                    'database security', 'backup recovery', 'performance tuning',
                    'replication', 'clustering', 'database optimization'
                },
                'weight': 1.1
            }
        }

    def analyze_job_roles(self, text, skills_found):
        text = text.lower()
        scores = defaultdict(float)
        
        for role, details in self.job_roles.items():
            # Calculate keyword match score
            keyword_matches = sum(1 for keyword in details['keywords'] 
                                if keyword.lower() in text)
            base_score = (keyword_matches / len(details['keywords'])) * 100
            
            # Calculate skill match score using the skills dictionary
            if skills_found:
                skill_matches = sum(1 for skill in skills_found.keys() 
                                  if any(kw in skill.lower() for kw in details['keywords']))
                skill_score = (skill_matches / len(details['keywords'])) * 100
            else:
                skill_score = 0
            
            # Combined weighted score
            final_score = (base_score * 0.4 + skill_score * 0.6) * details['weight']
            if final_score > 20:  # Only include roles with >20% match
                scores[role] = final_score

        # Sort roles by score
        sorted_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        roles_with_confidence = [
            {
                'role': role,
                'confidence': min(100, score),  # Cap at 100%
                'requirements': sorted(list(self.job_roles[role]['keywords']))[:8],  # Top 8 requirements
                'matched_keywords': [kw for kw in self.job_roles[role]['keywords'] 
                                   if kw.lower() in text or 
                                   any(kw.lower() in skill.lower() for skill in skills_found.keys())]
            }
            for role, score in sorted_roles
        ]

        return roles_with_confidence[:3]  # Return top 3 matching roles

    def analyze_specific_role(self, text, skills_found, role):
        text = text.lower()
        details = self.job_roles[role]
        
        # Calculate keyword match score
        keyword_matches = sum(1 for keyword in details['keywords'] 
                            if keyword.lower() in text)
        base_score = (keyword_matches / len(details['keywords'])) * 100
        
        # Calculate skill match score
        if skills_found:
            skill_matches = sum(1 for skill in skills_found.keys() 
                              if any(kw in skill.lower() for kw in details['keywords']))
            skill_score = (skill_matches / len(details['keywords'])) * 100
        else:
            skill_score = 0
        
        # Combined weighted score
        final_score = (base_score * 0.4 + skill_score * 0.6) * details['weight']
        
        return {
            'role': role,
            'confidence': min(100, final_score),  # Cap at 100%
            'requirements': sorted(list(details['keywords']))[:8],
            'matched_keywords': [kw for kw in details['keywords'] 
                               if kw.lower() in text or 
                               any(kw.lower() in skill.lower() for skill in skills_found.keys())]
        }