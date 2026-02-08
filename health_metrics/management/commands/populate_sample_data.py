"""
Management command to populate sample health data for testing
Usage: python manage.py populate_sample_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from health_metrics.models import BloodReport, VitalSigns, HealthMetric
from accounts.models import UserProfile
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate sample health data for testing purposes'

    def handle(self, *args, **options):
        # Create test user if not exists
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('testuser123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user: testuser'))

        # Create or update profile
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'age': 35,
                'gender': 'M',
                'height_cm': 175,
                'weight_kg': 80
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created user profile'))

        # Generate sample blood reports (last 30 days)
        for i in range(0, 30, 7):  # One report per week
            date = datetime.now().date() - timedelta(days=i)
            
            # Vary the values slightly
            glucose = random.uniform(90, 130)
            cholesterol = random.uniform(180, 240)
            hdl = random.uniform(35, 60)
            ldl = cholesterol - hdl - random.uniform(20, 40)
            
            blood_report, created = BloodReport.objects.get_or_create(
                user=user,
                date=date,
                defaults={
                    'hemoglobin_g_dl': random.uniform(13, 15),
                    'hematocrit_percent': random.uniform(38, 46),
                    'wbc_k_ul': random.uniform(4, 11),
                    'platelets_k_ul': random.uniform(150, 400),
                    'glucose_mg_dl': glucose,
                    'creatinine_mg_dl': random.uniform(0.7, 1.2),
                    'bun_mg_dl': random.uniform(7, 20),
                    'total_cholesterol_mg_dl': cholesterol,
                    'ldl_cholesterol_mg_dl': ldl,
                    'hdl_cholesterol_mg_dl': hdl,
                    'triglycerides_mg_dl': random.uniform(50, 150),
                    'ast_u_l': random.uniform(10, 40),
                    'alt_u_l': random.uniform(7, 40),
                }
            )
            if created:
                self.stdout.write(f'Created blood report for {date}')

        # Generate sample vital signs (last 7 days, 2 per day)
        for i in range(0, 7):
            date = datetime.now().date() - timedelta(days=i)
            
            for time_idx in range(2):
                time = datetime.strptime(f"{8 + time_idx * 8}:00", "%H:%M").time()
                
                # Vary systolic BP (normally between 120-140)
                systolic = random.uniform(120, 140)
                diastolic = random.uniform(70, 90)
                
                vital, created = VitalSigns.objects.get_or_create(
                    user=user,
                    date=date,
                    time=time,
                    defaults={
                        'systolic_bp': int(systolic),
                        'diastolic_bp': int(diastolic),
                        'heart_rate_bpm': random.randint(60, 80),
                        'temperature_celsius': random.uniform(36.5, 37.5),
                        'respiratory_rate': random.randint(12, 20),
                        'oxygen_saturation': random.uniform(95, 100),
                    }
                )
                if created:
                    self.stdout.write(f'Created vital signs for {date} {time}')

        # Generate sample health metrics (last 7 days)
        metrics_data = [
            ('sleep', 7, 'hours'),
            ('exercise', 45, 'minutes'),
            ('water_intake', 2000, 'ml'),
            ('mood', 7, 'score'),
            ('stress', 4, 'level'),
        ]
        
        for metric_type, base_value, unit in metrics_data:
            for i in range(7):
                date = datetime.now().date() - timedelta(days=i)
                
                # Add some randomness
                value = base_value + random.uniform(-2, 2)
                
                metric, created = HealthMetric.objects.get_or_create(
                    user=user,
                    metric_type=metric_type,
                    date=date,
                    defaults={
                        'value': max(0, value),
                        'notes': f'Sample {metric_type} data'
                    }
                )
                if created:
                    self.stdout.write(
                        f'Created {metric_type} metric for {date}: {value:.1f} {unit}'
                    )

        self.stdout.write(
            self.style.SUCCESS(
                '\n✓ Sample data population completed!\n'
                'Login with:\n'
                '  Username: testuser\n'
                '  Password: testuser123'
            )
        )
