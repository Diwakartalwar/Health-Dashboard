# Project Overview & Architecture

## Health Forecast Dashboard - Technical Documentation

### What This Application Does

The Health Forecast Dashboard is a comprehensive health tracking and analytics platform that:

1. **Collects Health Data**
   - Blood test reports (CBC, metabolic panel, lipid panel, liver function)
   - Vital signs (blood pressure, heart rate, temperature, O₂ saturation)
   - Lifestyle metrics (sleep, exercise, water intake, mood, stress)
   - Personal health information (age, gender, height, weight)

2. **Analyzes Health Metrics**
   - Processes blood test results against medical standards
   - Evaluates vital signs for abnormalities
   - Tracks lifestyle patterns
   - Calculates BMI and other health indicators

3. **Generates Forecasts & Risk Assessments**
   - Calculates overall health score (0-100)
   - Assesses cardiovascular disease risk
   - Evaluates diabetes risk
   - Generates personalized health recommendations

4. **Provides User-Friendly Dashboard**
   - Visual display of health trends
   - Quick access to add new data
   - Risk level indicators
   - Action recommendations

---

## System Architecture

### Frontend Layer
- **Framework**: Bootstrap 5
- **Templates**: Django template engine
- **Interactivity**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js for data visualization (ready to implement)

### Backend Layer
- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Authentication**: Django auth + Session-based
- **Database ORM**: Django ORM

### Database Layer
- **Primary**: SQLite (development) / PostgreSQL (production)
- **Models**: 
  - User (Django built-in)
  - UserProfile (custom)
  - BloodReport (health data)
  - VitalSigns (vital metrics)
  - HealthMetric (lifestyle tracking)
  - HealthForecast (analysis results)

### Business Logic Layer
- **Forecaster Module**: Health analysis and prediction
- **Risk Calculators**: Cardiovascular & Diabetes risk assessment
- **Recommendation Engine**: Personalized health suggestions

---

## Database Models & Relationships

```
User (Django built-in)
├── UserProfile (1-to-1)
│   ├── age
│   ├── gender
│   ├── height_cm
│   ├── weight_kg
│   └── calculated_bmi
│
├── BloodReport (1-to-many)
│   ├── date
│   ├── glucose_mg_dl
│   ├── hemoglobin_g_dl
│   ├── total_cholesterol_mg_dl
│   ├── ldl_cholesterol_mg_dl
│   ├── hdl_cholesterol_mg_dl
│   ├── triglycerides_mg_dl
│   ├── ast_u_l
│   ├── alt_u_l
│   └── ... (14+ fields)
│
├── VitalSigns (1-to-many)
│   ├── date
│   ├── time
│   ├── systolic_bp
│   ├── diastolic_bp
│   ├── heart_rate_bpm
│   ├── temperature_celsius
│   ├── respiratory_rate
│   └── oxygen_saturation
│
├── HealthMetric (1-to-many)
│   ├── metric_type (weight, sleep, exercise, etc.)
│   ├── value
│   ├── date
│   └── notes
│
└── HealthForecast (1-to-1)
    ├── health_score (0-100)
    ├── cardiovascular_risk
    ├── diabetes_risk
    └── recommendations (JSON array)
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERACTIONS                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Register → Login → Profile Setup → Enter Health Data      │
│                                                               │
│        Blood Reports  |  Vital Signs  |  Health Metrics     │
│                                                               │
└────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE STORAGE                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  SQLite Database (Development) / PostgreSQL (Production)    │
│  ├── User Accounts                                           │
│  ├── Health Data Records                                     │
│  ├── Forecast Results                                        │
│  └── System Metadata                                         │
│                                                               │
└────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  ANALYSIS ENGINE                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Data Aggregation                                         │
│     ├── Latest blood report                                  │
│     ├── Latest vital signs                                   │
│     └── 7-30 day metrics history                             │
│                                                               │
│  2. Health Analysis                                          │
│     ├── Blood metric evaluation                              │
│     ├── Vital sign assessment                                │
│     └── Lifestyle pattern review                             │
│                                                               │
│  3. Risk Calculation                                         │
│     ├── Cardiovascular risk scoring                          │
│     ├── Diabetes risk scoring                                │
│     └── Overall health score                                 │
│                                                               │
│  4. Recommendation Generation                                │
│     ├── Medical standard-based suggestions                   │
│     ├── Personalized action items                            │
│     └── Warning alerts                                       │
│                                                               │
└────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  DASHBOARD PRESENTATION                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Health Score Display                                        │
│  ├── Color-coded risk indicators                             │
│  ├── Latest metrics summary                                  │
│  ├── Historical trends                                       │
│  └── Actionable recommendations                              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Health Analysis Algorithms

### 1. Overall Health Score Calculation

**Base Score**: 70/100

**Adjustments**:
- Glucose levels: ±10 points
- Cholesterol levels: ±10 points
- Blood pressure: ±15 points
- Sleep quality: ±8 points
- Exercise frequency: ±5 points
- Stress levels: ±8 points
- Hemoglobin levels: ±8 points

**Formula**:
```
Final Score = Base(70) + Sum(Adjustments)
Range: 0-100 (clamped)
```

### 2. Cardiovascular Risk Assessment

**Risk Factors** (Weighted):
- Systolic BP ≥ 160 or Diastolic ≥ 100: +30 points
- Systolic BP ≥ 140 or Diastolic ≥ 90: +20 points
- Systolic BP ≥ 130 or Diastolic ≥ 80: +10 points
- Total Cholesterol > 240: +25 points
- Total Cholesterol > 200: +10 points
- Low HDL (< 40): +15 points

**Classification**:
- Score ≥ 50: HIGH RISK
- Score 25-49: MODERATE RISK
- Score < 25: LOW RISK

### 3. Diabetes Risk Assessment

**Risk Factors** (Weighted):
- Fasting Glucose ≥ 126 mg/dL: +40 points
- Fasting Glucose ≥ 100 mg/dL: +20 points
- BMI ≥ 30 (Obese): +30 points
- BMI ≥ 25 (Overweight): +15 points

**Classification**:
- Score ≥ 50: HIGH RISK
- Score 25-49: MODERATE RISK
- Score < 25: LOW RISK

---

## Application URLs & Routes

```
/                                    # Home/Login page
/accounts/register/                  # User registration
/accounts/login/                     # User login
/accounts/logout/                    # User logout
/accounts/profile/                   # User profile management

/dashboard/overview/                 # Main dashboard
/dashboard/api/blood-trend/          # Blood data API
/dashboard/api/vital-trend/          # Vital signs API
/dashboard/api/health-metrics-trend/ # Health metrics API

/health_metrics/blood-reports/       # Blood reports list
/health_metrics/blood-reports/add/   # Add blood report
/health_metrics/blood-reports/<id>/edit/    # Edit blood report
/health_metrics/blood-reports/<id>/delete/  # Delete blood report

/health_metrics/vital-signs/         # Vital signs list
/health_metrics/vital-signs/add/     # Add vital signs

/health_metrics/health-metrics/      # Health metrics list
/health_metrics/health-metrics/add/  # Add health metric

/admin/                              # Django admin panel
```

---

## Tech Stack Details

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Bootstrap 5 | Responsive UI |
| | HTML5/CSS3 | Markup & Styling |
| | JavaScript | Interactivity |
| | Chart.js | Data Visualization |
| **Backend** | Django 4.2 | Web Framework |
| | DRF | REST API |
| | SQLite/PostgreSQL | Database |
| **Analysis** | NumPy | Numerical Computing |
| | Pandas | Data Analysis |
| | Scikit-learn | ML Capabilities |
| **Utilities** | Pillow | Image Processing |
| | Celery | Task Queue (Future) |
| | Redis | Caching (Future) |

---

## Security Features Implemented

✅ User authentication & session management
✅ CSRF protection on forms
✅ SQL injection prevention (ORM usage)
✅ Password hashing
✅ Permission-based data access
✅ Input validation on forms

**Production Recommendations**:
- [ ] Switch to environment-based settings
- [ ] Enable HTTPS/SSL
- [ ] Implement CORS properly
- [ ] Add rate limiting
- [ ] Setup logging & monitoring
- [ ] Regular security audits
- [ ] Database encryption
- [ ] API authentication tokens

---

## Scalability Considerations

### Current Setup (Development)
- Single database (SQLite)
- Synchronous request processing
- In-memory session storage

### Scalability Improvements

1. **Database**: PostgreSQL with connection pooling
2. **Caching**: Redis for session & data caching
3. **Task Queue**: Celery for background processing
4. **CDN**: Static file distribution
5. **Load Balancing**: Multiple server instances
6. **Monitoring**: Prometheus + Grafana
7. **API Rate Limiting**: DRF throttling

---

## Future Enhancements

### Phase 2 - AI & ML
- [ ] Predictive health modeling
- [ ] Anomaly detection
- [ ] Personalized recommendations
- [ ] Trend forecasting

### Phase 3 - Integration
- [ ] Wearable device APIs (Fitbit, Apple Watch)
- [ ] EHR systems integration
- [ ] Third-party lab APIs
- [ ] Insurance provider APIs

### Phase 4 - Advanced Features
- [ ] Telemedicine integration
- [ ] AI-powered chatbot
- [ ] Community features
- [ ] Gamification elements

---

## Performance Optimization

### Already Implemented
- Database query optimization with select_related
- Form validation to prevent errors
- Pagination for large datasets
- Session-based caching

### Recommended
```python
# Use Django cache framework
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def dashboard_overview(request):
    pass

# Use database indexes
class BloodReport(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['user', 'date']),
        ]
```

---

## Testing Strategy

### Unit Tests
```bash
python manage.py test accounts
python manage.py test health_metrics
python manage.py test dashboard
```

### Integration Tests
- User registration flow
- Data entry validation
- Dashboard calculation accuracy

### Performance Tests
- Database query optimization
- Response time monitoring
- Load testing

---

## Deployment Checklist

- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup environment variables
- [ ] Configure PostgreSQL
- [ ] Setup Redis
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Setup logging
- [ ] Create automated backups
- [ ] Setup monitoring & alerts
- [ ] Run security checks
- [ ] Optimize static files
- [ ] Setup CI/CD pipeline
- [ ] Create database indexes

---

**This documentation provides a comprehensive overview of the Health Forecast Dashboard architecture and functionality.**

For implementation details, refer to individual app documentation or code comments.
