#!/bin/bash
# Disable Vercel Authentication Protection - Version 2
# Using correct API endpoints

set -e

echo "🚀 Disabling Vercel Authentication Protection..."
echo ""

# Load environment variables
source ~/infinity_secure/auto_keys.env

# Get project ID
echo "🔍 Getting project ID..."
PROJECT_ID=$(vercel project ls --token "$VERCEL_TOKEN" 2>&1 | grep arguscloud | awk '{print $1}')

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Could not find project ID"
    exit 1
fi

echo "✅ Project ID: $PROJECT_ID"
echo ""

# Get current project settings
echo "🔍 Checking current settings..."
CURRENT=$(curl -s -X GET \
  "https://api.vercel.com/v9/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $VERCEL_TOKEN")

echo "📋 Current protection settings:"
echo "$CURRENT" | jq '{
  ssoProtection: .ssoProtection,
  passwordProtection: .passwordProtection,
  trustedIps: .trustedIps
}' 2>/dev/null || echo "Could not parse"
echo ""

# Try to disable SSO protection
echo "🔓 Attempting to disable SSO protection..."
RESULT1=$(curl -s -X PATCH \
  "https://api.vercel.com/v9/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ssoProtection": null
  }')

echo "📋 SSO Protection result:"
echo "$RESULT1" | jq '.' 2>/dev/null || echo "$RESULT1"
echo ""

# Try to disable password protection
echo "🔓 Attempting to disable password protection..."
RESULT2=$(curl -s -X PATCH \
  "https://api.vercel.com/v9/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "passwordProtection": null
  }')

echo "📋 Password Protection result:"
echo "$RESULT2" | jq '.' 2>/dev/null || echo "$RESULT2"
echo ""

# Try to set trusted IPs to allow all
echo "🔓 Attempting to allow all IPs..."
RESULT3=$(curl -s -X PATCH \
  "https://api.vercel.com/v9/projects/$PROJECT_ID" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "trustedIps": {
      "addresses": [],
      "protectionMode": "disabled"
    }
  }')

echo "📋 Trusted IPs result:"
echo "$RESULT3" | jq '.' 2>/dev/null || echo "$RESULT3"
echo ""

# Wait for changes
echo "⏳ Waiting for changes to propagate..."
sleep 10

# Test API
echo "🧪 Testing API..."
API_RESPONSE=$(curl -s https://arguscloud.vercel.app/api/health)

echo "📋 API Response:"
echo "$API_RESPONSE"
echo ""

if echo "$API_RESPONSE" | grep -q "healthy"; then
    echo "🎉 SUCCESS! API is working!"
    exit 0
else
    echo "⚠️  API still not accessible"
    echo "   You may need to disable protection manually in Vercel Dashboard"
    exit 1
fi

