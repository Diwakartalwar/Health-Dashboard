# Health Forecast Dashboard - Quick Reference Guide

## 📍 Application URLs Quick Map

```
┌─ BASE (http://localhost:8000)
│
├─ Authentication
│  ├─ /accounts/register/      → User Registration
│  ├─ /accounts/login/         → User Login  
│  ├─ /accounts/logout/        → User Logout
│  └─ /accounts/profile/       → User Profile
│
├─ Dashboard
│  └─ /dashboard/overview/     → Main Dashboard
│
├─ Health Data Entry
│  ├─ /health_metrics/blood-reports/        → Blood Reports List
│  ├─ /health_metrics/blood-reports/add/    → Add Blood Report
│  ├─ /health_metrics/vital-signs/          → Vital Signs List
│  ├─ /health_metrics/vital-signs/add/      → Add Vital Signs
│  ├─ /health_metrics/health-metrics/       → Health Metrics List
│  └─ /health_metrics/health-metrics/add/   → Add Health Metric
│
├─ API Endpoints (REST)
│  ├─ /api/metrics/blood-reports/           → Blood Reports API
│  ├─ /api/metrics/vital-signs/             → Vital Signs API
│  └─ /api/metrics/health-metrics/          → Health Metrics API
│
├─ Admin
│  └─ /admin/                               → Django Admin Panel
│
└─ Static & Media
   ├─ /static/                              → CSS, JS, Images
   └─ /media/                               → User Uploads
```

## 🔑 Key Data Entry Fields

### Blood Report
```
Date                              [Required]
├─ Glucose (mg/dL)               [Diabetes indicator]
├─ Hemoglobin (g/dL)             [Oxygen capacity]
├─ WBC (K/µL)                    [Immune system]
├─ Platelets (K/µL)              [Blood clotting]
├─ Total Cholesterol (mg/dL)     [Heart health]
├─ HDL Cholesterol (mg/dL)       [Good cholesterol ↑]
├─ LDL Cholesterol (mg/dL)       [Bad cholesterol ↓]
├─ Triglycerides (mg/dL)         [Fat level]
├─ AST (U/L)                     [Liver enzyme]
└─ ALT (U/L)                     [Liver enzyme]
```

### Vital Signs
```
Date                             [Required]
Time                             [Required]
├─ Systolic BP (mmHg)            [Pressure during heartbeat]
├─ Diastolic BP (mmHg)           [Pressure between beats]
├─ Heart Rate (bpm)              [Beats per minute]
├─ Temperature (°C)              [Body temperature]
├─ Respiratory Rate              [Breaths per minute]
└─ Oxygen Saturation (%)         [Blood oxygen level]
```

### Health Metrics
```
Date                             [Required]
Metric Type                      [Required]
├─ Sleep (hours)                 [Recommended: 7-9]
├─ Exercise (minutes)            [Recommended: 150/week]
├─ Water Intake (ml)             [Recommended: 2000-3000]
├─ Mood (score 1-10)             [Subjective wellness]
├─ Stress (level 1-10)           [Stress assessment]
└─ Weight (kg)                   [Body weight tracking]

Notes (Optional)                 [Additional context]
```

## 📊 Health Score Interpretation

```
90-100  🟢 EXCELLENT   │ Exceptional health status
80-89   🟢 VERY GOOD   │ Strong health indicators
70-79   🟡 GOOD        │ Healthy with room for improvement
60-69   🟡 FAIR        │ Needs attention in some areas
50-59   🔴 POOR        │ Multiple health concerns
0-49    🔴 CRITICAL    │ Seek medical attention
```

## 🎯 Risk Assessment Levels

### Cardiovascular Risk
```
Risk Score Calculation:
BP ≥ 160/100: +30
BP ≥ 140/90:  +20
BP ≥ 130/80:  +10
Cholesterol > 240: +25
Cholesterol > 200: +10
Low HDL < 40: +15

Classification:
≥ 50  🔴 HIGH       → Consult doctor
25-49 🟡 MODERATE   → Lifestyle changes
< 25  🟢 LOW        → Continue current habits
```

### Diabetes Risk
```
Risk Score Calculation:
Glucose ≥ 126: +40
Glucose ≥ 100: +20
BMI ≥ 30: +30
BMI ≥ 25: +15

Classification:
≥ 50  🔴 HIGH       → Medical attention needed
25-49 🟡 MODERATE   → Monitor closely
< 25  🟢 LOW        → Maintain good habits
```

## 💻 Common Commands

### Setup & Installation
```bash
# Windows
setup.bat

# Linux/Mac
bash setup.sh

# Manual
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

### Development
```bash
# Start server
python manage.py runserver

# Load sample data
python manage.py populate_sample_data

# Access Django shell
python manage.py shell

# Create new app
python manage.py startapp app_name

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests
python manage.py test
```

### Database
```bash
# Show all migrations
python manage.py showmigrations

# Undo last migration
python manage.py migrate app_name 0001

# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 🔐 Security Checklist

Development ✅:
- [ ] Use DEBUG=True
- [ ] Use default SECRET_KEY
- [ ] SQLite database
- [ ] Local development only

Production ⚠️:
- [ ] Set DEBUG=False
- [ ] Generate new SECRET_KEY
- [ ] Use PostgreSQL
- [ ] Enable HTTPS/SSL
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup Redis
- [ ] Configure email
- [ ] Setup backups
- [ ] Enable logging
- [ ] Setup monitoring

## 📱 User Workflow

```
┌─ New User
│
├─ Step 1: Register
│  └─ Create account with email
│
├─ Step 2: Login
│  └─ Access dashboard
│
├─ Step 3: Complete Profile
│  └─ Add age, gender, height, weight
│
├─ Step 4: Add Health Data
│  ├─ Blood reports (after lab tests)
│  ├─ Vital signs (daily/weekly)
│  └─ Health metrics (daily tracking)
│
└─ Step 5: View Dashboard
   ├─ See health score
   ├─ Review risk levels
   └─ Follow recommendations
```

## 📈 Health Tracking Best Practices

**Blood Reports**
- Record after lab tests
- Every 3-6 months for regular checkups
- More frequently if monitoring specific conditions

**Vital Signs**
- Daily: Same time for consistency
- Morning: Before breakfast/medication
- Evening: Before dinner

**Health Metrics**
- Sleep: Record daily before bed
- Exercise: Log immediately after activity
- Water: Track throughout day
- Mood/Stress: Daily evening reflection

## 🎨 UI Colors & Meanings

```
🔵 Blue         → Primary actions, information
🟢 Green        → Success, healthy, low risk
🟡 Yellow       → Warning, moderate risk, caution
🔴 Red          → Danger, high risk, critical
⚪ Gray         → Inactive, disabled, secondary
```

## 🚨 Alert Types

```
🚨 CRITICAL     → Seek immediate medical attention
⚠️  WARNING      → Consult healthcare professional
📌 NOTICE       → Monitor or take action
ℹ️  INFO         → Informational, helpful tip
```

## 📊 Example Health Data Ranges

### Blood Glucose
```
< 100 mg/dL      🟢 Normal (fasting)
100-125 mg/dL    🟡 Prediabetic
≥ 126 mg/dL      🔴 Diabetic
```

### Cholesterol
```
< 200 mg/dL      🟢 Desirable
200-239 mg/dL    🟡 Borderline high
≥ 240 mg/dL      🔴 High
```

### Blood Pressure
```
< 120/80         🟢 Normal
120-129/<80      🟡 Elevated
130-139/80-89    🟡 Stage 1 HTN
≥ 140/90         🔴 Stage 2 HTN
≥ 180/120        🚨 Critical
```

### Body Mass Index (BMI)
```
< 18.5           🔵 Underweight
18.5-24.9        🟢 Normal weight
25-29.9          🟡 Overweight
≥ 30             🔴 Obese
```

## 🔄 Data Sync & Backup

**Automatic Backups** (Production):
- Daily database backups
- Weekly incremental backups
- Monthly full system backups

**Manual Backup**:
```bash
# Database
pg_dump database_name > backup.sql

# Media files
tar -czf media_backup.tar.gz /path/to/media/
```

## 🐛 Debugging Tips

**Check Logs**:
```bash
# Django logs
tail -f logs/django.log

# Server logs
sudo journalctl -u health_forecast
```

**Debug Mode**:
```python
# In settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

**Test API Endpoints**:
```bash
# Using curl
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/api/metrics/blood-reports/

# Using python requests
import requests
response = requests.get('http://localhost:8000/api/metrics/blood-reports/')
print(response.json())
```

## 📚 File Structure Quick Reference

```
project/
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── db.sqlite3            # Database (dev)
├── config/               # Settings
├── accounts/             # Auth & profiles
├── health_metrics/       # Data models
├── dashboard/            # Analytics
├── templates/            # HTML
├── static/               # CSS/JS/Images
├── media/                # User files
├── *.md                  # Documentation
└── setup.bat/sh          # Setup scripts
```

## ⌨️ Keyboard Shortcuts

- `Ctrl+C`     → Stop server
- `Ctrl+K`     → Clear terminal
- `Tab`        → Auto-complete (shell)
- `↑/↓`        → Command history
- `Ctrl+L`     → Clear screen

## 📞 Quick Support Matrix

| Issue | Solution |
|-------|----------|
| Port in use | `python manage.py runserver 8001` |
| Import error | `pip install -r requirements.txt` |
| Database error | `python manage.py migrate` |
| Static files missing | `python manage.py collectstatic` |
| Permission denied | `chmod +x script.sh` |
| Connection refused | Check if server is running |

---

**This quick reference covers the essentials. For detailed info, see the full documentation files.**

Created: January 27, 2026
Updated: January 27, 2026
