#!/usr/bin/env python3
"""
Start script for the HR & Payroll SaaS API
Run this script to start the server with default settings
"""

import subprocess
import sys
import os

def main():
    print("="*60)
    print("Starting HR & Payroll SaaS API Server")
    print("="*60)
    print()

    # Check if virtual environment is activated
    if sys.prefix == sys.base_prefix:
        print("⚠️  Warning: Virtual environment is not activated!")
        print("   It's recommended to activate the virtual environment first:")
        print("   source venv/bin/activate  (Linux/Mac)")
        print("   venv\\Scripts\\activate (Windows)")
        print()

    # Start the server
    try:
        print("Starting server on http://localhost:8000")
        print("API Documentation available at:")
        print("  - Swagger UI: http://localhost:8000/docs")
        print("  - ReDoc: http://localhost:8000/redoc")
        print()
        print("Press Ctrl+C to stop the server")
        print("="*60)
        print()

        # Run uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ], check=True)

    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
