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
- HTML, CSS, JavaScript with Bootstrap
- Chart.js for data visualization
- Responsive design with CSS animations
- File upload handling

### Backend
- Python Flask REST API
- Natural Language Processing for text analysis
- Industry and role matching algorithms

## Getting Started

### Prerequisites
- Python (v3.8+)
- pip package manager

### Installation & Running Locally

1. Clone the repository:
```bash
git clone https://github.com/aathifpm/ResumeAnalyzer.git
cd ResumeAnalyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the application:
```bash
python app.py
```

4. Open your browser and go to:
```
http://localhost:5000
```

## Deployment

### Deploying to Render

1. Create a Render account at [render.com](https://render.com)
2. From your dashboard, click "New" and select "Web Service"
3. Connect your GitHub repository containing this project
4. Configure your web service with these settings:
   - Name: resume-analyzer (or your preferred name)
   - Environment: Python 3
   - Build Command: `./build.sh` 
   - Start Command: `gunicorn app:app`
   - Select the appropriate instance type (even Free tier works)
   - Add environment variables if needed
   
5. Click "Create Web Service"
6. Once deployed, your app will be available at https://your-app-name.onrender.com

**Note:** The first deployment may take longer as it needs to install all dependencies and build the required packages.

### Deploying to Heroku

1. Create a Heroku account and install the Heroku CLI
2. Login to Heroku CLI:
```bash
heroku login
```

3. Create a new Heroku app:
```bash
heroku create your-app-name
```

4. Push to Heroku:
```bash
git push heroku main
```

5. Open the deployed app:
```bash
heroku open
```

### Deploying to Other Platforms

The application can be deployed to any platform that supports Python applications. Make sure to:

1. Set the appropriate environment variables if needed
2. Install the required dependencies from requirements.txt
3. Run the application using gunicorn (for production) as specified in the Procfile

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
