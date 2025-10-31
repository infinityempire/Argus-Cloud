#!/bin/bash

# 🚀 Argus Cloud - Deploy to Vercel Script
# This script will deploy your Argus Cloud project to Vercel

set -e

echo "🚀 Argus Cloud - Deploy to Vercel"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found!"
    echo "Please run this script from the Argus-Cloud directory"
    exit 1
fi

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo "✅ Vercel CLI is installed"
echo ""

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
echo ""
echo "⚠️  You will be asked to login to Vercel if not already logged in."
echo "⚠️  Please follow the instructions in the terminal."
echo ""

vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Your Argus Cloud is now live at: https://arguscloud.vercel.app"
echo ""
echo "📝 Next steps:"
echo "1. Make sure environment variables are set in Vercel dashboard:"
echo "   - DATABASE_URL"
echo "   - NEON_API_KEY"
echo ""
echo "2. Test your deployment:"
echo "   curl https://arguscloud.vercel.app/api/health"
echo ""
echo "3. Open in browser:"
echo "   https://arguscloud.vercel.app"
echo ""
