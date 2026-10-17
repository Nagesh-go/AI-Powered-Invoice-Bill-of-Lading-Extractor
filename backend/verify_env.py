"""
Environment Verification Script.
Ensures that all required libraries are installed and can be imported cleanly.
"""
import sys

def verify():
    print(f"Python executable : {sys.executable}")
    print(f"Python version    : {sys.version.split()[0]}\n")
    
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("pypdf", "pypdf"),
        ("dotenv", "python-dotenv"),
        ("google.genai", "Google GenAI SDK"),
        ("pytest", "Pytest"),
        ("httpx", "HTTPX"),
    ]
    
    all_ok = True
    for module_name, display_name in packages:
        try:
            mod = __import__(module_name, fromlist=["__version__"])
            version = getattr(mod, "__version__", "installed (no __version__)")
            print(f"  [OK] {display_name:<18} : v{version}")
        except ImportError as exc:
            print(f"  [FAIL] {display_name:<18} : Not found ({exc})")
            all_ok = False
            
    print("-" * 50)
    if all_ok:
        print(" Environment verification SUCCESSFUL! Ready for Phase 2.")
    else:
        print(" Some packages are missing. Run: pip install -r backend/requirements.txt")

if __name__ == "__main__":
    verify()
