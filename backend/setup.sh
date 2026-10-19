#!/bin/bash
# Setup script untuk AI Trading Agent - Fase 2
# Analysis Engine dependencies installation

echo "======================================================================"
echo "🚀 AI Trading Agent - Fase 2 Setup"
echo "======================================================================"
echo ""

# Check if virtual environment is active
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Virtual environment not detected!"
    echo "   Recommended: Create and activate virtual environment first"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate  # Linux/Mac"
    echo "   venv\\Scripts\\activate     # Windows"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Installing dependencies..."
echo ""

# Install main dependencies
pip install pandas-ta==0.3.14b textblob==0.17.1

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi

echo ""
echo "📥 Downloading TextBlob corpora..."
echo ""

# Download TextBlob corpora
python -m textblob.download_corpora

if [ $? -eq 0 ]; then
    echo "✅ TextBlob corpora downloaded successfully"
else
    echo "❌ Error downloading TextBlob corpora"
    exit 1
fi

echo ""
echo "======================================================================"
echo "✅ Setup completed successfully!"
echo "======================================================================"
echo ""
echo "🎯 Next steps:"
echo "   1. Start data collector: python -m data_collector.main_collector"
echo "   2. Start analysis engine: python -m analysis.main_analysis"
echo ""
echo "📚 Documentation:"
echo "   - Main README: ../README.md"
echo "   - Analysis README: analysis/README.md"
echo ""
echo "🚀 Ready to analyze!"
echo ""
