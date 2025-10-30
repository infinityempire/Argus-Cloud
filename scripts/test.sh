#!/bin/bash

echo "🧪 Testing Argus Cloud API..."
echo ""

# Test root endpoint
echo "1️⃣ Testing root endpoint..."
curl -s http://127.0.0.1:8000 | python3 -m json.tool
echo ""

# Test health endpoint
echo "2️⃣ Testing health endpoint..."
curl -s http://127.0.0.1:8000/api/health | python3 -m json.tool
echo ""

# Test get memories
echo "3️⃣ Testing get memories..."
curl -s http://127.0.0.1:8000/api/memory | python3 -m json.tool
echo ""

# Test create memory
echo "4️⃣ Testing create memory..."
curl -s -X POST http://127.0.0.1:8000/api/memory \
  -H "Content-Type: application/json" \
  -d '{"content":"Test memory from script"}' | python3 -m json.tool
echo ""

echo "✅ Tests completed!"
