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

# Check yt-dlp
if ! command -v yt-dlp &>/dev/null; then
    echo "ERROR: yt-dlp not found. Install with: brew install yt-dlp"
    exit 1
fi
YTDLP_VERSION=$(yt-dlp --version 2>&1)
echo "yt-dlp: $YTDLP_VERSION"

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
if "$VENV_DIR/bin/python" -c "import youtube_transcript_api; print('youtube-transcript-api: ok')" 2>/dev/null; then
    echo "Setup complete. All dependencies ready."
else
    echo "ERROR: youtube-transcript-api installation failed."
    exit 1
fi

echo ""
echo "To use scripts manually:"
echo "  source $VENV_DIR/bin/activate"
echo "  python3 scripts/search_youtube.py --query 'topic' --max-results 5"
