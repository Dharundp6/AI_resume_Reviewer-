# Job Application Optimizer

A full-stack AI-powered application that uses Google Gemini AI to optimize job applications with resume analysis, ATS checking, company research, and automated document generation.

## 🌟 Features

- **Resume Upload & Analysis**: Extract text from PDF resumes and analyze them with AI
- **ATS Compatibility Check**: Score resumes against Applicant Tracking Systems (0-100%)
- **Company Research**: Automated research on target companies
- **AI-Powered Recommendations**: Personalized suggestions for resume improvement and interview prep
- **Document Generation**: Create optimized resumes and cover letters as Word documents (.docx)
- **Modern Web Interface**: Beautiful React frontend with Material-UI
- **RESTful API**: Clean, well-documented API endpoints using FastAPI

## 🚀 Quick Start

### TL;DR - Get Running in 2 Commands
```bash
npm run install:all  # Install dependencies
npm start            # Run the application
```
Then open http://localhost:3000

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google Gemini API key (free at https://makersuite.google.com/app/apikey)

### Installation

#### Step 1: Install Dependencies
```bash
# Install all dependencies (backend + frontend)
npm run install:all
```

Or install separately:
```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
cd ..
```

#### Step 2: Run the Application
```bash
# Start both backend and frontend together
npm start
```

Or run separately (requires 2 terminals):
```bash
# Terminal 1 - Backend
npm run start:backend
# or: python app.py

# Terminal 2 - Frontend
npm run start:frontend
# or: cd frontend && npm start
```

### Access Application

- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🎯 How to Use

1. **Upload Resume** - Drop your PDF resume
2. **Enter Job Details** - Provide job role, company name, and job description
3. **AI Analysis** - Wait ~30-60 seconds for comprehensive analysis
4. **View Results** - See scores, insights, and recommendations
5. **Generate Documents** - Create optimized resume and cover letter
6. **Download** - Save your improved documents

## 📁 Project Structure

```
app/
├── api/                    # API endpoints
│   ├── resume.py          # Resume operations
│   ├── company.py         # Company research
│   ├── documents.py       # Document generation
│   └── analysis.py        # AI recommendations
├── core/
│   └── config.py          # Configuration
├── models/
│   └── schemas.py         # Data models
├── services/
│   ├── gemini_service.py  # AI integration
│   ├── pdf_service.py     # PDF processing
│   └── document_service.py # DOCX generation
├── frontend/              # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   └── App.js
│   └── package.json
├── uploads/               # Temporary uploads
├── outputs/               # Generated documents
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Google Gemini AI** - Advanced language model (1.5 Pro)
- **PyPDF2** - PDF text extraction
- **python-docx** - Document generation
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **Material-UI** - Component library
- **Axios** - HTTP client
- **React Dropzone** - File upload

## 🔌 API Endpoints

### Resume
- `POST /api/resume/upload` - Upload resume PDF
- `POST /api/resume/analyze` - Analyze resume for job role
- `POST /api/resume/ats-check` - Check ATS compatibility

### Company
- `POST /api/company/research` - Research company information

### Analysis
- `POST /api/analysis/recommendations` - Generate personalized recommendations

### Documents
- `POST /api/documents/generate` - Generate optimized documents
- `GET /api/documents/download/{filename}` - Download document

## 📊 What You Get

### Resume Analysis
- Overall score (1-10)
- Strengths identification
- Skills to emphasize
- Keywords to add
- Areas for improvement

### ATS Compatibility
- ATS score (0-100%)
- Keyword match percentage
- Missing keywords
- Formatting issues
- Recommendations

### Company Insights
- Company overview
- Mission and values
- Recent news
- Company culture
- Leadership information

### AI Recommendations
- Resume alignment actions
- Cover letter talking points
- Cultural fit demonstrations
- Interview question predictions
- Preparation tips

### Generated Documents
- Optimized resume (DOCX)
- Personalized cover letter (DOCX)
- ATS-friendly formatting

## 🔑 Configuration

### API Key Setup

Add your Gemini API key to `.env`:
```env
GEMINI_API_KEY='your_api_key_here'
```

**Get your free API key:**
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Get API Key"
4. Copy and add to `.env`

**Free tier limits:**
- 1,500 requests/day
- 1M tokens/minute

### Optional Settings

Edit `core/config.py` to customize:
- `GEMINI_MODEL` - AI model (default: gemini-1.5-pro)
- `GEMINI_TEMPERATURE` - Creativity (default: 0.7)
- `MAX_UPLOAD_SIZE` - Max PDF size (default: 10MB)

## 🐛 Troubleshooting

### Backend Issues

**Module not found:**
```bash
pip install -r requirements.txt
```

**Gemini API error:**
- Check API key in `.env`
- Verify internet connection
- Check API quota

**PDF extraction failed:**
- Ensure PDF is not password-protected
- Verify PDF contains selectable text

### Frontend Issues

**npm install fails:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Cannot connect to backend:**
- Ensure backend is running on port 8000
- Check if port is already in use

### Port Already in Use

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

## 💡 Usage Example (Python)

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Upload resume
with open("resume.pdf", "rb") as f:
    response = requests.post(f"{BASE_URL}/resume/upload", files={"file": f})
    resume_text = response.json()["resume_text"]

# Analyze resume
response = requests.post(
    f"{BASE_URL}/resume/analyze",
    data={
        "resume_text": resume_text,
        "job_role": "Software Engineer",
        "job_description": "..."
    }
)
analysis = response.json()

# Check ATS compatibility
response = requests.post(
    f"{BASE_URL}/resume/ats-check",
    data={"resume_text": resume_text, "job_description": "..."}
)
ats_score = response.json()

# Research company
response = requests.post(
    f"{BASE_URL}/company/research",
    data={"company_name": "Google"}
)
company_info = response.json()

# Generate recommendations
response = requests.post(
    f"{BASE_URL}/analysis/recommendations",
    json={
        "job_role": "Software Engineer",
        "company_name": "Google",
        "analysis": analysis,
        "ats_score": ats_score,
        "company_research": company_info
    }
)
recommendations = response.json()

# Generate documents
response = requests.post(
    f"{BASE_URL}/documents/generate",
    json={
        "resume_text": resume_text,
        "job_role": "Software Engineer",
        "company_name": "Google",
        "analysis": analysis,
        "ats_score": ats_score,
        "company_research": company_info,
        "recommendations": recommendations
    }
)
documents = response.json()

print(f"Resume: {documents['resume_file_path']}")
print(f"Cover Letter: {documents['cover_letter_file_path']}")
```

## 🧪 Testing

Run the setup test:
```bash
npm test
# or: python test_setup.py
```

## 📋 NPM Commands Reference

| Command | Description |
|---------|-------------|
| `npm start` | Start both backend and frontend |
| `npm run start:backend` | Start backend only |
| `npm run start:frontend` | Start frontend only |
| `npm run install:all` | Install all dependencies |
| `npm run build` | Build frontend for production |
| `npm test` | Run setup verification test |

## 📝 Development

### Code Formatting
```bash
pip install black
black .
```

### Running Tests
```bash
pip install pytest pytest-asyncio
pytest
```

## 🔒 Security Notes

- Never commit `.env` file with real API keys
- Use environment variables in production
- Enable HTTPS in production
- Restrict CORS origins in production
- Implement rate limiting for APIs

## 📄 License

MIT License - Free for personal and commercial use

## 🙏 Acknowledgments

- Google Gemini AI for AI capabilities
- FastAPI for the excellent web framework
- React and Material-UI communities

## 📞 Support

- API Documentation: http://localhost:8000/docs
- Run `python test_setup.py` to verify installation
- Check troubleshooting section above

---

**Happy Job Hunting! 🎯**

Made by Dp 
