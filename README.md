# Health Forecast Dashboard

A comprehensive Django web application for tracking health metrics, blood reports, and vital signs with AI-powered health forecasting and risk assessment.

## Features

### 📊 Dashboard
- **Overall Health Score**: 0-100 comprehensive health assessment
- **Risk Assessments**: Cardiovascular and Diabetes risk evaluation
- **Health Recommendations**: AI-generated personalized health suggestions
- **Real-time Analytics**: Visual representation of health trends

### 🩸 Health Data Management
- **Blood Reports**: Track CBC, metabolic panel, lipid panel, and liver function tests
- **Vital Signs**: Record blood pressure, heart rate, temperature, oxygen saturation, and respiratory rate
- **Health Metrics**: Log daily metrics like sleep, exercise, water intake, mood, and stress levels
- **User Profile**: Maintain personal health information and BMI calculation

### 🔐 User Features
- User registration and authentication
- Secure personal health data storage
- Profile management
- Health history tracking

### 🤖 AI-Powered Forecasting
The app includes intelligent health analysis that:
- Analyzes blood glucose levels for diabetes risk
- Assesses blood pressure and cholesterol for cardiovascular health
- Evaluates lifestyle metrics (sleep, exercise, stress)
- Provides personalized health recommendations
- Generates risk scores based on medical standards

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- SQLite (included with Python) or PostgreSQL

### Setup Instructions

1. **Clone or navigate to the project**
   ```bash
   cd "c:\developments\django\health forcast"
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## Project Structure

```
health_forecast/
├── config/              # Project settings and URLs
│   ├── settings.py     # Django settings
│   ├── urls.py         # URL configuration
│   ├── wsgi.py         # WSGI configuration
│   └── asgi.py         # ASGI configuration
│
├── accounts/           # User authentication and profiles
│   ├── models.py       # UserProfile model
│   ├── views.py        # Registration and profile views
│   ├── forms.py        # User forms
│   └── urls.py         # App URLs
│
├── health_metrics/     # Health data management
│   ├── models.py       # BloodReport, VitalSigns, HealthMetric models
│   ├── views.py        # Views for health data management
│   ├── forms.py        # Data entry forms
│   ├── serializers.py  # REST API serializers
│   └── urls.py         # App URLs
│
├── dashboard/          # Analytics and forecasting
│   ├── models.py       # HealthForecast model
│   ├── views.py        # Dashboard views
│   ├── forecaster.py   # AI forecasting engine
│   ├── admin.py        # Admin interface
│   └── urls.py         # App URLs
│
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── dashboard/      # Dashboard templates
│   ├── accounts/       # Account templates
│   ├── health_metrics/ # Health data templates
│   └── registration/   # Authentication templates
│
├── static/             # Static files (CSS, JS, images)
├── media/              # User uploaded files
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Models Overview

### UserProfile
- Extends Django User model
- Stores age, gender, height, weight
- Calculates BMI automatically

### BloodReport
- Complete Blood Count (CBC)
- Metabolic Panel (glucose, creatinine, BUN)
- Lipid Panel (cholesterol, HDL, LDL, triglycerides)
- Liver Function Tests (AST, ALT)

### VitalSigns
- Blood pressure (systolic/diastolic)
- Heart rate
- Temperature
- Respiratory rate
- Oxygen saturation

### HealthMetric
- Weight tracking
- Sleep hours
- Exercise minutes
- Water intake
- Mood score
- Stress level

### HealthForecast
- Overall health score (0-100)
- Cardiovascular risk level
- Diabetes risk level
- Personalized recommendations

## API Endpoints

The app includes REST API endpoints for developers:

- `GET/POST /api/metrics/blood-reports/` - Blood reports
- `GET/POST /api/metrics/vital-signs/` - Vital signs
- `GET/POST /api/metrics/health-metrics/` - Health metrics
- `GET /dashboard/api/blood-trend/` - Blood trend data
- `GET /dashboard/api/vital-trend/` - Vital signs trend data
- `GET /dashboard/api/health-metrics-trend/` - Metrics trend data

## Usage Guide

### Adding Blood Reports
1. Navigate to Dashboard → Add Blood Report
2. Fill in the date and available blood test results
3. Submit to save

### Recording Vital Signs
1. Go to Dashboard → Add Vital Signs
2. Enter date, time, and measurements
3. Submit to record

### Tracking Health Metrics
1. Access Dashboard → Add Health Metric
2. Select metric type (sleep, exercise, etc.)
3. Enter value and date
4. Add notes if needed

### Viewing Dashboard
The main dashboard displays:
- Current health score
- Risk assessments
- Latest test results
- Health recommendations
- Quick action buttons

## Health Assessment Criteria

### Health Score (0-100)
- Base score: 70
- Adjusted based on:
  - Blood glucose levels
  - Cholesterol levels
  - Blood pressure
  - Heart rate
  - Sleep quality
  - Exercise levels
  - Stress management

### Cardiovascular Risk
- **Low**: Score < 25
- **Moderate**: Score 25-50
- **High**: Score > 50

### Diabetes Risk
- **Low**: Score < 25
- **Moderate**: Score 25-50
- **High**: Score > 50

## Administration

### Accessing Django Admin
1. Go to `http://localhost:8000/admin`
2. Login with superuser credentials
3. Manage users, health data, and forecasts

### Managing Data
- View all user health records
- Edit or delete health metrics
- Monitor risk assessments
- Generate health reports

## Security Considerations

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement proper user authentication
- Regular database backups

## Future Enhancements

- [ ] Advanced AI predictions using machine learning
- [ ] Integration with wearable devices
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Email notifications for health alerts
- [ ] PDF report generation
- [ ] Data export features
- [ ] Telemedicine integration
- [ ] Historical trend analysis
- [ ] Comparative health benchmarking

## Technology Stack

- **Backend**: Django 4.2
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Frontend**: Bootstrap 5, jQuery, Chart.js
- **REST API**: Django REST Framework
- **Analysis**: NumPy, Pandas, Scikit-learn

## Troubleshooting

### Database Issues
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Reset Database
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## Performance Tips

- Implement caching for frequently accessed data
- Use pagination for large datasets
- Index database fields frequently used in filters
- Consider celery for background tasks
- Use Redis for session management

## Contributing

To contribute to this project:
1. Create a new branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
- Check the troubleshooting section
- Review Django documentation
- Check Django REST Framework docs
- Consult health data standards (CDC, WHO)

## Disclaimer

This application is for educational and personal health tracking purposes only. It does not replace professional medical advice. Always consult with healthcare professionals for medical decisions.

---

**Created**: 2026  
**Version**: 1.0.0  
**Status**: Active Development
