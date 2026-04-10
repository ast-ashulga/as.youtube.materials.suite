#!/bin/bash
# YouTube Materials Suite — Environment Setup
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$PROJECT_DIR/.venv"

echo "=== YouTube Materials Suite Setup ==="
echo "Project: $PROJECT_DIR"

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Install Python 3.11+ first."
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1)
echo "Python: $PYTHON_VERSION"

# Create venv if missing
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# Install/upgrade requirements
echo "Installing Python dependencies..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r "$SCRIPT_DIR/requirements.txt"

# Verify installation
if "$VENV_DIR/bin/python" -c "import requests; print('requests: ok')" 2>/dev/null; then
    echo "Setup complete. All dependencies ready."
else
    echo "ERROR: requests installation failed."
    exit 1
fi

echo ""
echo "=== API Keys Required ==="
echo ""
echo "This suite requires two API keys. Set them in your shell profile"
echo "(~/.zshrc or ~/.bashrc) or export them before running:"
echo ""
echo "1. YouTube Data API v3 (free — 10,000 units/day)"
echo "   Get key: https://console.cloud.google.com/apis/library/youtube.googleapis.com"
echo "   export YOUTUBE_API_KEY=your_key_here"
echo ""
echo "2. Supadata.ai Transcript API (free — 100 transcripts/month)"
echo "   Get key: https://supadata.ai"
echo "   export SUPADATA_API_KEY=your_key_here"
echo ""
echo "To verify keys are set:"
echo "  echo \$YOUTUBE_API_KEY"
echo "  echo \$SUPADATA_API_KEY"
echo ""
echo "To use scripts manually:"
echo "  source $VENV_DIR/bin/activate"
echo "  python3 scripts/search_youtube.py --query 'topic' --max-results 5"
echo "  python3 scripts/fetch_transcript.py --video-id VIDEO_ID"
echo "  python3 scripts/extract_metadata.py --url 'https://www.youtube.com/watch?v=VIDEO_ID'"
