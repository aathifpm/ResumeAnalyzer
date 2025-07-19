import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import backend modules
from backend.parsers.resume_parser import ResumeParser
from backend.utils.keyword_extractor import KeywordExtractor
from backend.models.job_role_analyzer import JobRoleAnalyzer
from backend.models.suggestion_generator import SuggestionGenerator
from backend.models.ats_analyzer import ATSAnalyzer
from backend.models.industry_analyzer import IndustryAnalyzer

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Sample job requirements
JOB_REQUIREMENTS = {
    'software_engineer': ['python', 'javascript', 'sql', 'git', 'aws'],
    'data_scientist': ['python', 'machine learning', 'sql', 'statistics', 'tensorflow'],
    'web_developer': ['html', 'css', 'javascript', 'react', 'node.js'],
    'devops_engineer': ['docker', 'kubernetes', 'jenkins', 'aws', 'terraform'],
    'mobile_developer': ['android', 'ios', 'react native', 'flutter', 'mobile testing'],
    'cloud_architect': ['aws', 'azure', 'cloud architecture', 'microservices', 'security'],
    'security_engineer': ['cybersecurity', 'penetration testing', 'security audit', 'encryption'],
    'data_engineer': ['sql', 'etl', 'hadoop', 'spark', 'data warehouse'],
    'ml_engineer': ['machine learning', 'deep learning', 'python', 'tensorflow', 'mlops'],
    'ui_ux_designer': ['figma', 'user research', 'wireframing', 'prototyping', 'adobe xd'],
    'qa_engineer': ['selenium', 'test automation', 'jira', 'test planning', 'api testing'],
    'blockchain_developer': ['solidity', 'smart contracts', 'web3', 'ethereum', 'defi'],
    'game_developer': ['unity', 'unreal engine', 'c++', 'game design', '3d modeling'],
    'embedded_systems': ['c', 'embedded c', 'rtos', 'microcontrollers', 'firmware'],
    'network_engineer': ['cisco', 'networking', 'tcp/ip', 'security', 'vpn']
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve frontend files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['resume']
        selected_role = request.form.get('job_role', 'software_engineer')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            try:
                # Parse resume
                parser = ResumeParser()
                text = parser.extract_text(file_path)
                sections = parser.extract_sections()
                
                # Extract keywords
                extractor = KeywordExtractor()
                keywords = extractor.extract_keywords(text)
                
                # Initialize suggestions list
                suggestions = []
                
                # Analyze suitable job roles
                job_analyzer = JobRoleAnalyzer()
                role_match = job_analyzer.analyze_specific_role(text, keywords, selected_role)
                suitable_roles = job_analyzer.analyze_job_roles(text, keywords)
                
                # Use the score from the selected role
                score = role_match['confidence']
                
                # Generate sophisticated suggestions
                suggestion_generator = SuggestionGenerator()
                suggestions = suggestion_generator.generate_suggestions(
                    role=selected_role,
                    found_skills=set(keywords.keys()),
                    sections=sections
                )
                
                # Create job requirements structure for ATS
                role_requirements = {
                    'keywords': JOB_REQUIREMENTS[selected_role],
                    'required_years': 2,  # Default requirement
                    'weight': 1.0
                }
                
                ats_analyzer = ATSAnalyzer()
                ats_results = ats_analyzer.calculate_ats_score(
                    text=text,
                    role_requirements=role_requirements,
                    sections=sections,
                    skills_found=keywords
                )
                
                # Get industry analysis
                industry_analyzer = IndustryAnalyzer()
                industry_analysis = industry_analyzer.analyze_industry_fit(text, keywords)
                
                return jsonify({
                    'score': round(score, 2),
                    'ats_score': ats_results['overall_score'],
                    'ats_details': ats_results['detailed_scores'],
                    'ats_recommendations': ats_results['recommendations'],
                    'sections_found': sections,
                    'keywords': keywords,
                    'suitable_roles': suitable_roles,
                    'suggestions': suggestions,
                    'industry_analysis': industry_analysis
                })
                
            except Exception as e:
                print(f"Analysis error: {str(e)}")
                return jsonify({'error': f'Error analyzing resume: {str(e)}'}), 500
            finally:
                # Always try to clean up the uploaded file
                try:
                    os.remove(file_path)
                except:
                    pass
        
        return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=5000) 