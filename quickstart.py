#!/usr/bin/env python3
"""
Quick Start Script for AI Website Generator
This script helps you quickly set up and run the full-stack application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python():
    """Check Python version"""
    print("✓ Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_node():
    """Check if Node.js is installed"""
    print("✓ Checking Node.js installation...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Node.js {result.stdout.strip()} detected")
            return True
    except FileNotFoundError:
        print("❌ Node.js is not installed!")
        print("   Please install Node.js from: https://nodejs.org/")
        return False
    return False

def check_env_file():
    """Check if .env file exists"""
    print("✓ Checking environment configuration...")
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found!")
        print("   Creating .env file from template...")
        
        env_content = """# Google Gemini API Key (Required)
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Unsplash API Key (Optional - for images)
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here

# Flask Configuration
FLASK_ENV=development
PORT=5000
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✓ .env file created!")
        print("\n⚠️  IMPORTANT: Please edit .env file and add your API keys!")
        print("   - Get Google Gemini API key: https://aistudio.google.com/app/apikey")
        print("   - Get Unsplash API key (optional): https://unsplash.com/developers")
        return False
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key or api_key == 'your_google_gemini_api_key_here':
        print("⚠️  GOOGLE_API_KEY not configured in .env file!")
        print("   Please edit .env file and add your API key.")
        return False
    
    print("✓ Environment configuration found")
    return True

def install_python_deps():
    """Install Python dependencies"""
    print_header("Installing Python Dependencies")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✓ Python dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies!")
        return False

def install_node_deps():
    """Install Node.js dependencies"""
    print_header("Installing Node.js Dependencies")
    frontend_dir = Path('frontend')
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    try:
        os.chdir('frontend')
        subprocess.run(['npm', 'install'], check=True)
        os.chdir('..')
        print("✓ Node.js dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Node.js dependencies!")
        os.chdir('..')
        return False

def start_backend():
    """Start Flask backend"""
    print_header("Starting Flask Backend")
    print("📡 Backend will start on: http://localhost:5000")
    print("   (Press Ctrl+C to stop)\n")
    
    try:
        subprocess.run([sys.executable, 'api.py'])
    except KeyboardInterrupt:
        print("\n✓ Backend stopped")

def start_frontend():
    """Start React frontend"""
    print_header("Starting React Frontend")
    print("🌐 Frontend will start on: http://localhost:3000")
    print("   (Press Ctrl+C to stop)\n")
    
    try:
        os.chdir('frontend')
        subprocess.run(['npm', 'run', 'dev'])
        os.chdir('..')
    except KeyboardInterrupt:
        print("\n✓ Frontend stopped")
        os.chdir('..')

def main():
    """Main quick start function"""
    print_header("AI Website Generator - Quick Start")
    
    # Check prerequisites
    if not check_python():
        return
    
    if not check_node():
        return
    
    env_ok = check_env_file()
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Install dependencies (first time setup)")
    print("2. Start backend server (Flask)")
    print("3. Start frontend server (React)")
    print("4. Full setup and start both servers")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == '1':
        if not env_ok:
            print("\n⚠️  Please configure .env file before installing dependencies")
            return
        install_python_deps()
        install_node_deps()
        print_header("Setup Complete!")
        print("✓ All dependencies installed successfully!")
        print("\nNext steps:")
        print("  1. Run this script again and choose option 4")
        print("  2. Or manually start backend: python api.py")
        print("  3. And frontend: cd frontend && npm run dev")
    
    elif choice == '2':
        if not env_ok:
            print("\n⚠️  Please configure .env file before starting backend")
            return
        start_backend()
    
    elif choice == '3':
        start_frontend()
    
    elif choice == '4':
        if not env_ok:
            print("\n⚠️  Please configure .env file before starting")
            return
        
        print("\n⚠️  This will install dependencies (if needed) and start both servers.")
        print("   You'll need to run them in separate terminal windows.")
        print("\nTo run both servers:")
        print("  Terminal 1: python api.py")
        print("  Terminal 2: cd frontend && npm run dev")
        print("\nWould you like to install dependencies now? (y/n): ", end='')
        
        if input().lower() == 'y':
            install_python_deps()
            install_node_deps()
            print_header("Setup Complete!")
            print("✓ Dependencies installed!")
            print("\nNow start both servers in separate terminals:")
            print("  Terminal 1: python api.py")
            print("  Terminal 2: cd frontend && npm run dev")
    
    elif choice == '5':
        print("\n👋 Goodbye!")
        return
    
    else:
        print("\n❌ Invalid choice!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
