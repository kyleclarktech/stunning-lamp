#!/bin/bash
# Quick script to run query system tests

echo "🚀 Query System Testing Suite"
echo "============================"
echo ""

# Check if services are running
echo "📋 Checking services..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ API service not running. Start with: docker-compose up -d"
    exit 1
fi

if ! curl -s http://localhost:11434 > /dev/null; then
    echo "❌ Ollama service not running. Start with: docker-compose up -d"
    exit 1
fi

echo "✅ Services are running"
echo ""

# Validate data first
echo "🔍 Validating database state..."
python validate_data.py --summary 2>/dev/null || python validate_data.py

echo ""
echo "Press Enter to continue with query tests..."
read

# Run quick test
echo ""
echo "🧪 Running quick query test..."
python test_websocket.py

echo ""
echo "Press Enter to run comprehensive tests..."
read

# Run full test suite
echo ""
echo "🏃 Running comprehensive test suite..."
echo "This will test 20+ query patterns and take about 1-2 minutes..."
python test_query_system.py

echo ""
echo "✅ Testing complete! Check the generated log and JSON files for detailed results."
echo ""
echo "💡 Next steps:"
echo "   - Review test results in query_test_results_*.json"
echo "   - Check logs in query_test_*.log" 
echo "   - Use debug_query_tool.py for manual testing"
echo "   - See QUERY_TESTING_GUIDE.md for more information"