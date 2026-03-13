"""
Deployment Check Script - Validates all requirements before Render deployment
Run this script to identify and fix common deployment issues
"""

import sys
import os
from pathlib import Path

def check_mediapipe():
    """Verify MediaPipe version is correct for mp.solutions API"""
    try:
        import mediapipe
        version = mediapipe.__version__
        if version.startswith("0.10.14"):
            print("✅ MediaPipe version: OK (0.10.14.x)")
            return True
        else:
            print(f"❌ MediaPipe version: WRONG ({version})")
            print("   Fix: Use mediapipe==0.10.14 (newer versions removed mp.solutions)")
            return False
    except ImportError:
        print("❌ MediaPipe: NOT INSTALLED")
        return False

def check_flask():
    """Verify Flask is installed"""
    try:
        import flask
        print(f"✅ Flask: OK ({flask.__version__})")
        return True
    except ImportError:
        print("❌ Flask: NOT INSTALLED")
        return False

def check_opencv():
    """Verify OpenCV is installed"""
    try:
        import cv2
        print(f"✅ OpenCV: OK ({cv2.__version__})")
        return True
    except ImportError:
        print("❌ OpenCV: NOT INSTALLED")
        return False

def check_numpy():
    """Verify NumPy is installed"""
    try:
        import numpy
        print(f"✅ NumPy: OK ({numpy.__version__})")
        return True
    except ImportError:
        print("❌ NumPy: NOT INSTALLED")
        return False

def check_env_file():
    """Verify required environment variables exist"""
    frontend_dir = Path(__file__).parent
    env_file = frontend_dir / ".env"
    
    if not env_file.exists():
        print("⚠️  .env file: MISSING (create from .env.example)")
        return False
    
    required_vars = ["SECRET_KEY", "FLASK_ENV", "GROQ_API_KEY", 
                     "DB_HOST", "DB_USER", "DB_PASSWORD", "DB_PORT", "DB_NAME"]
    
    with open(env_file) as f:
        env_content = f.read()
    
    missing = [var for var in required_vars if f"{var}=" not in env_content]
    
    if missing:
        print(f"❌ .env: Missing variables - {', '.join(missing)}")
        return False
    
    print("✅ .env: OK (all required variables present)")
    return True

def check_app_structure():
    """Verify required app files exist"""
    frontend_dir = Path(__file__).parent
    required_files = [
        "run.py",
        "app/__init__.py",
        "app/config.py",
        "app/routes/yoga.py",
        "ml/pose_detector.py",
        "ml/evaluation_config.py"
    ]
    
    missing = []
    for file_path in required_files:
        full_path = frontend_dir / file_path
        if not full_path.exists():
            missing.append(file_path)
    
    if missing:
        print(f"❌ App structure: Missing files - {', '.join(missing)}")
        return False
    
    print("✅ App structure: OK (all required files present)")
    return True

def check_requirements_file():
    """Verify requirements.txt exists and mediapipe version is correct"""
    root_dir = Path(__file__).parent.parent
    req_file = root_dir / "requirements.txt"
    
    if not req_file.exists():
        print("❌ requirements.txt: NOT FOUND at project root")
        return False
    
    with open(req_file) as f:
        req_content = f.read()
    
    if "mediapipe==0.10.14" in req_content:
        print("✅ requirements.txt: OK (mediapipe==0.10.14)")
        return True
    elif "mediapipe==0.10.30" in req_content:
        print("❌ requirements.txt: WRONG mediapipe version (0.10.30)")
        print("   Fix: Change to mediapipe==0.10.14")
        return False
    else:
        print("❌ requirements.txt: Cannot find mediapipe version specification")
        return False

def check_procfile():
    """Verify Procfile syntax for Render (Linux path handling)"""
    root_dir = Path(__file__).parent.parent
    procfile = root_dir / "Procfile"
    
    if not procfile.exists():
        print("❌ Procfile: NOT FOUND")
        return False
    
    with open(procfile) as f:
        procfile_content = f.read().strip()
    
    # Check for Windows-style backslashes (won't work on Linux/Render)
    if "\\" in procfile_content:
        print(f"❌ Procfile: Windows path syntax detected")
        print(f"   Current: {procfile_content}")
        print('   Fix: Use   web: cd "FRONT END" && python run.py')
        return False
    
    if 'cd "FRONT END"' in procfile_content and "python run.py" in procfile_content:
        print("✅ Procfile: OK (correct Linux syntax)")
        return True
    else:
        print(f"⚠️  Procfile: Syntax may need review")
        print(f"   Current: {procfile_content}")
        return False

def main():
    """Run all deployment checks"""
    print("\n" + "="*60)
    print("DEPLOYMENT CHECK - Render.com Verification")
    print("="*60 + "\n")
    
    checks = [
        ("Requirements.txt", check_requirements_file),
        ("MediaPipe Version", check_mediapipe),
        ("Flask", check_flask),
        ("OpenCV", check_opencv),
        ("NumPy", check_numpy),
        (".env File", check_env_file),
        ("App Structure", check_app_structure),
        ("Procfile", check_procfile),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error during check: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"SUMMARY: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ All deployment checks passed!")
        print("Your app is ready to deploy to Render.com")
        return 0
    else:
        print(f"\n❌ {total - passed} check(s) failed. Fix issues above before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
