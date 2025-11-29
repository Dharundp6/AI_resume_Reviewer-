"""
Quick test script to verify installation
Run this to check if everything is set up correctly
"""

import sys
import os

# Fix Unicode encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠ Warning: Python 3.8+ recommended")
        return False
    return True

def test_dependencies():
    """Check if required packages are installed"""
    required = [
        'fastapi',
        'uvicorn',
        'PyPDF2',
        'google.generativeai',
        'docx',
        'pydantic',
        'aiofiles'
    ]

    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)

    if missing:
        print(f"\n⚠ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    return True

def test_imports():
    """Test if project modules can be imported"""
    try:
        from core.config import settings
        print("✓ core.config")

        from api import resume, company, documents, analysis
        print("✓ api modules")

        from services import gemini_service, pdf_service, document_service
        print("✓ services")

        from models.schemas import ResumeAnalysisResponse
        print("✓ models")

        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_api_key():
    """Check if API key is configured"""
    try:
        from core.config import settings

        if settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 20:
            print(f"✓ Gemini API key configured ({len(settings.GEMINI_API_KEY)} chars)")
            return True
        else:
            print("✗ Gemini API key not configured")
            print("  Add your API key to .env file")
            return False
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False

def test_directories():
    """Check if required directories exist"""
    dirs = ['uploads', 'outputs']

    for directory in dirs:
        if os.path.exists(directory):
            print(f"✓ {directory}/ directory exists")
        else:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ {directory}/ directory created")

    return True

def test_frontend():
    """Check if frontend is set up"""
    if os.path.exists('frontend/package.json'):
        print("✓ Frontend directory exists")

        if os.path.exists('frontend/node_modules'):
            print("✓ Frontend dependencies installed")
            return True
        else:
            print("⚠ Frontend dependencies not installed")
            print("  Run: cd frontend && npm install")
            return False
    else:
        print("⚠ Frontend not found")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Job Application Optimizer - Setup Test")
    print("=" * 50)
    print()

    results = []

    print("1. Checking Python Version...")
    results.append(test_python_version())
    print()

    print("2. Checking Python Dependencies...")
    results.append(test_dependencies())
    print()

    print("3. Checking Project Imports...")
    results.append(test_imports())
    print()

    print("4. Checking API Key...")
    results.append(test_api_key())
    print()

    print("5. Checking Directories...")
    results.append(test_directories())
    print()

    print("6. Checking Frontend...")
    results.append(test_frontend())
    print()

    print("=" * 50)
    if all(results):
        print("✓ ALL CHECKS PASSED!")
        print("=" * 50)
        print()
        print("Your setup is complete and ready to use!")
        print()
        print("Next steps:")
        print("  Windows: Run start.bat")
        print("  Mac/Linux: Run ./start.sh")
        print()
        print("Then open: http://localhost:3000")
    else:
        print("⚠ SOME CHECKS FAILED")
        print("=" * 50)
        print()
        print("Please fix the issues above before running the application.")
        print()
        print("Common fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Configure API key in .env file")
        print("  - Install frontend: cd frontend && npm install")
    print()

if __name__ == "__main__":
    main()
