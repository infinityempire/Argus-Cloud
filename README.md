# 🧠 Argus Cloud

AI-powered memory agent with FastAPI backend and PostgreSQL (Neon) database.

## 🚀 Quick Start

### Local Development

```bash
cd ~/Argus-Cloud
bash scripts/start.sh
```

Open http://localhost:8000 in your browser.

### Deploy to Vercel

```bash
bash deploy_to_vercel.sh
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Quick start guide for local development
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment guide for Vercel
- **[ARGUS_SUCCESS_REPORT.md](ARGUS_SUCCESS_REPORT.md)** - Full project report and testing results

## 🛠️ Tech Stack

- **Backend:** FastAPI + Python 3.11
- **Database:** PostgreSQL (Neon)
- **Frontend:** HTML + JavaScript
- **Deployment:** Vercel Serverless Functions
- **Version Control:** Git + GitHub

## 📦 Project Structure

```
Argus-Cloud/
├── api/
│   └── index.py           # Vercel entry point
├── server/
│   ├── app.py            # FastAPI application
│   └── requirements.txt  # Python dependencies
├── client/
│   └── index.html        # Frontend UI
├── scripts/
│   ├── start.sh          # Local server startup
│   └── test.sh           # API tests
├── vercel.json           # Vercel configuration
├── requirements.txt      # Root dependencies
└── .env                  # Environment variables
```

## 🔑 Environment Variables

Create a `.env` file or set these in Vercel:

```bash
DATABASE_URL=postgresql://user:password@host/database
NEON_API_KEY=your_neon_api_key
```

## 🌐 API Endpoints

### Health Check
```bash
GET /api/health
```

### Get All Memories
```bash
GET /api/memory
```

### Create Memory
```bash
POST /api/memory
Content-Type: application/json

{
  "content": "Memory content",
  "metadata": {"key": "value"}
}
```

### Delete Memory
```bash
DELETE /api/memory/{id}
```

## 🧪 Testing

Run local tests:
```bash
bash scripts/test.sh
```

Test production:
```bash
curl https://arguscloud.vercel.app/api/health
```

## 📝 License

MIT

## 👤 Author

Tal Darei - Infinity Empire

## 🔗 Links

- **Live Demo:** https://arguscloud.vercel.app
- **GitHub:** https://github.com/infinityempire/Argus-Cloud
- **Vercel Dashboard:** https://vercel.com/talush1s-projects/arguscloud

---

Made with ❤️ by Infinity Empire
