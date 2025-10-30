# 🚀 Argus Cloud - Quick Start Guide

## הפעלה מהירה

### 1. הפעלת השרת
```bash
cd /home/ubuntu/Argus-Cloud
bash scripts/start.sh
```

### 2. פתיחת הממשק
פתח דפדפן וגש ל:
```
http://localhost:8000
```

### 3. בדיקת תקינות
```bash
bash scripts/test.sh
```

---

## API Endpoints

### בדיקת בריאות
```bash
curl http://localhost:8000/api/health
```

### קריאת כל הזיכרונות
```bash
curl http://localhost:8000/api/memory
```

### יצירת זיכרון חדש
```bash
curl -X POST http://localhost:8000/api/memory \
  -H "Content-Type: application/json" \
  -d '{"content":"My memory","metadata":{"tag":"test"}}'
```

### מחיקת זיכרון
```bash
curl -X DELETE http://localhost:8000/api/memory/1
```

---

## משתני סביבה

הקובץ `/home/ubuntu/infinity_secure/auto_keys.env` מכיל:
- `DATABASE_URL` - חיבור ל-Neon PostgreSQL
- `NEON_API_KEY` - מפתח API של Neon

---

## פתרון בעיות

### השרת לא עולה?
```bash
# בדוק שהפורט פנוי
netstat -tuln | grep 8000

# בדוק לוגים
cat /home/ubuntu/Argus-Cloud/server.log
```

### בעיית חיבור למסד נתונים?
```bash
# בדוק משתני סביבה
source /home/ubuntu/infinity_secure/auto_keys.env
echo $DATABASE_URL
```

---

## תמיכה

לשאלות ובעיות, פנה לתיעוד המלא ב-`ARGUS_SUCCESS_REPORT.md`
