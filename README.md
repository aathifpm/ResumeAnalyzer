# Smart Resume Analyzer

A sophisticated resume analysis tool that leverages AI to provide detailed insights, job role matching, and personalized recommendations for resume optimization.

## Features

### Resume Analysis
- Extracts and categorizes skills from uploaded resumes
- Analyzes resume sections and structure
- Provides ATS (Applicant Tracking System) compatibility scoring
- Identifies skill gaps and improvement areas

### Job Role Matching
- Matches resumes against multiple tech industry roles
- Provides confidence scores for each role match
- Identifies matched and missing skills for each role
- Suggests alternative career paths based on skillset

### Industry Analysis
- Detects relevant industry based on experience and skills
- Calculates industry match scores
- Provides industry-specific recommendations
- Identifies critical missing skills for target industries

### Smart Recommendations
- Generates personalized improvement suggestions
- Provides ATS optimization tips
- Recommends skills to acquire based on target roles
- Suggests format and content improvements

## Tech Stack

### Frontend
- React.js with Material-UI
- Chart.js for data visualization
- Responsive design with CSS animations
- PDF preview and file upload handling

### Backend
- Python Flask REST API
- Machine Learning models for skill extraction
- Natural Language Processing for text analysis
- Industry and role matching algorithms

## Getting Started

### Prerequisites
- Node.js (v14+)
- Python (v3.8+)
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/aathifpm/ResumeAnalyzer.git
cd ResumeAnalyzer
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Start the Flask server:
```bash
python app.py
```

4. Install frontend dependencies:
```bash
cd ../frontend
npm install
```

5. Start the React development server:
```bash
npm start
```

## Usage

1. Upload your resume (PDF, DOCX supported)
2. Select your target job role
3. Review the comprehensive analysis:
   - Overall match score
   - ATS compatibility score
   - Skills breakdown
   - Role-specific recommendations
   - Industry insights

## API Documentation

### POST /analyze
Analyzes a resume and returns detailed insights.

#### Request
- Method: POST
- Content-Type: multipart/form-data
- Body:
  - resume: File (PDF/DOCX)
  - job_role: String (optional)



## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- Resume parsing libraries and tools
- NLP frameworks and models
- Industry standard job requirements data
- Open source UI component libraries
```
