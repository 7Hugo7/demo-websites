#!/bin/bash

# Demo Builder - Quick Start Script (macOS optimized)

echo "🚀 Demo Website Builder - Starting..."
echo ""

# Navigate to script directory
cd "$(dirname "$0")"

# Check if Homebrew Python is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    echo "❌ Python 3 not found. Please install Python 3:"
    echo "   brew install python@3.11"
    exit 1
fi

echo "✅ Using Python: $($PYTHON_CMD --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Skip pip upgrade (it's hanging)
echo "⏭️  Skipping pip upgrade (using existing version)..."
echo ""

# Install dependencies (with progress)
echo "📥 Installing dependencies (PyQt6 is large, ~200MB)..."
echo "   This may take 2-5 minutes on first install..."
echo "   You should see download progress bars below..."
echo ""

# Use verbose output with unbuffered mode
python3 -u -m pip install -v -r requirements.txt || {
    echo ""
    echo "❌ Installation failed!"
    echo "Try running manually:"
    echo "  cd automation"
    echo "  source venv/bin/activate"
    echo "  pip install anthropic PyQt6 PyQt6-WebEngine requests python-dotenv"
    exit 1
}

echo ""
echo "✅ Installation complete!"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env and add your ANTHROPIC_API_KEY"
    echo "   Or use the 'Manage Keys' button in the app"
fi

# Check for PyQt6 specific issues on macOS
if [ "$(uname)" == "Darwin" ]; then
    echo "🍎 macOS detected - checking Qt installation..."
    echo ""

    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "⚠️  Homebrew not found. Qt6 installation skipped."
        echo "   Install Homebrew: https://brew.sh"
    else
        # Check if Qt6 is installed via Homebrew
        if ! command -v qmake6 &> /dev/null && ! brew list qt@6 &> /dev/null; then
            echo "📦 Installing Qt6 via Homebrew for better performance..."
            echo "   This may take a few minutes..."
            echo ""
            brew install qt@6
            echo ""
            echo "✅ Qt6 installed!"
        else
            echo "✅ Qt6 already installed"
        fi
    fi
    echo ""
fi

# Ask user which version to use
echo "Which version do you want to use?"
echo ""
echo "1. 🤖 Fully Automated (needs macOS permissions)"
echo "   - Automatically opens Terminal and sends prompt"
echo "   - Requires: System Settings → Accessibility → Add Terminal"
echo ""
echo "2. 📋 Simple (no permissions needed)"
echo "   - You copy/paste prompt to Claude manually"
echo "   - Works immediately, no setup"
echo ""
read -p "Enter 1 or 2: " choice

echo ""

if [ "$choice" = "1" ]; then
    echo "✨ Starting Fully Automated Version..."
    echo "💰 FREE - No API costs!"
    echo ""
    echo "If you get a permission error:"
    echo "→ See PERMISSIONS.md for setup guide"
    echo ""
    python demo_builder_auto.py
else
    echo "✨ Starting Simple Version..."
    echo "💰 FREE - No API costs!"
    echo ""
    echo "How it works:"
    echo "1. Click 'Generate Prompt'"
    echo "2. Click 'Copy Prompt'"
    echo "3. Open Terminal → run: claude"
    echo "4. Paste (Cmd+V)"
    echo "5. Click 'Start Monitoring'"
    echo ""
    python demo_builder_simple.py
fi

# Deactivate venv on exit
deactivate 2>/dev/null
