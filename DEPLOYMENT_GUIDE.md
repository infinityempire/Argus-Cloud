# 🚀 מדריך פריסה ל-Vercel - Argus Cloud

## שלב 1: הכנה

וודא שאתה בתיקיית הפרויקט:
```bash
cd ~/Argus-Cloud
```

## שלב 2: הרצת סקריפט הפריסה

הרץ את הסקריפט:
```bash
bash deploy_to_vercel.sh
```

## שלב 3: התחברות ל-Vercel

אם זו הפעם הראשונה שאתה מפרוס:

1. הסקריפט יבקש ממך להתחבר ל-Vercel
2. תקבל קישור לדפדפן
3. פתח את הקישור בדפדפן
4. התחבר עם חשבון Vercel שלך (GitHub/Google/Email)
5. אשר את ההתחברות
6. חזור לטרמינל והמשך

## שלב 4: הגדרת משתני סביבה ב-Vercel

**חשוב מאוד!** לאחר הפריסה, עליך להגדיר את משתני הסביבה ב-Vercel:

### דרך 1: דרך ממשק Vercel (מומלץ)

1. פתח: https://vercel.com/talush1s-projects/arguscloud/settings/environment-variables
2. הוסף את המשתנים הבאים:

**DATABASE_URL:**
```
postgresql://neondb_owner:npg_djGZMq1XR0by@ep-bitter-breeze-a4b3o4nf-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

**NEON_API_KEY:**
```
napi_1wx0v0xrm16n5dxgug3ge34z01hllax30950au5mtzlpsssa03syru2dudswuinr
```

3. בחר "Production" עבור כל משתנה
4. לחץ "Save"

### דרך 2: דרך CLI

```bash
# הוסף DATABASE_URL
vercel env add DATABASE_URL production
# הדבק את הערך כשתתבקש:
# postgresql://neondb_owner:npg_djGZMq1XR0by@ep-bitter-breeze-a4b3o4nf-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# הוסף NEON_API_KEY
vercel env add NEON_API_KEY production
# הדבק את הערך כשתתבקש:
# napi_1wx0v0xrm16n5dxgug3ge34z01hllax30950au5mtzlpsssa03syru2dudswuinr
```

## שלב 5: פריסה מחדש עם משתני הסביבה

לאחר הוספת משתני הסביבה, פרוס מחדש:
```bash
vercel --prod
```

## שלב 6: בדיקת הפריסה

בדוק שהכל עובד:

```bash
# בדיקת health
curl https://arguscloud.vercel.app/api/health

# בדיקת memories
curl https://arguscloud.vercel.app/api/memory
```

או פתח בדפדפן:
```
https://arguscloud.vercel.app
```

## פתרון בעיות

### שגיאה: "FUNCTION_INVOCATION_FAILED"

זה אומר שמשתני הסביבה לא מוגדרים. חזור לשלב 4.

### שגיאה: "500: INTERNAL_SERVER_ERROR"

1. בדוק את הלוגים ב-Vercel:
   ```bash
   vercel logs arguscloud --prod
   ```

2. או בממשק:
   https://vercel.com/talush1s-projects/arguscloud/deployments

### השרת לא מגיב

המתן כמה דקות - Vercel לוקח זמן לפרוס.

## עדכון הפרויקט בעתיד

כאשר אתה משנה קוד:

```bash
cd ~/Argus-Cloud
git add .
git commit -m "תיאור השינוי"
git push origin main
```

Vercel יפרוס אוטומטית את השינויים!

או פרוס ידנית:
```bash
vercel --prod
```

---

## סיכום מהיר

```bash
# 1. עבור לתיקיית הפרויקט
cd ~/Argus-Cloud

# 2. הרץ את סקריפט הפריסה
bash deploy_to_vercel.sh

# 3. הגדר משתני סביבה ב-Vercel (פעם אחת)
# עשה זאת דרך ממשק Vercel או CLI

# 4. פרוס מחדש
vercel --prod

# 5. בדוק
curl https://arguscloud.vercel.app/api/health
```

---

**בהצלחה! 🎉**
