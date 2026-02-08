from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class BloodReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_reports')
    date = models.DateField()
    
    # Complete Blood Count (CBC)
    hemoglobin_g_dl = models.FloatField(null=True, blank=True, help_text='g/dL')
    hematocrit_percent = models.FloatField(null=True, blank=True, help_text='%')
    wbc_k_ul = models.FloatField(null=True, blank=True, help_text='K/µL')
    platelets_k_ul = models.FloatField(null=True, blank=True, help_text='K/µL')
    
    # Metabolic Panel
    glucose_mg_dl = models.FloatField(null=True, blank=True, help_text='mg/dL')
    creatinine_mg_dl = models.FloatField(null=True, blank=True, help_text='mg/dL')
    bun_mg_dl = models.FloatField(null=True, blank=True, help_text='mg/dL')
    
    # Lipid Panel
    total_cholesterol_mg_dl = models.FloatField(null=True, blank=True, help_text='mg/dL')
    ldl_cholesterol_mg_dl = models.FloatField(null=True, blank=True, help_text='mg/dL')
    hdl_cholesterol_mg_dl = models.FloatField(null=True, blank=True, help_text='mg/dL')
    triglycerides_mg_dl = models.FloatField(null=True, blank=True, help_text='mg/dL')
    
    # Liver Function
    ast_u_l = models.FloatField(null=True, blank=True, help_text='U/L')
    alt_u_l = models.FloatField(null=True, blank=True, help_text='U/L')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class VitalSigns(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vital_signs')
    date = models.DateField()
    time = models.TimeField()
    
    systolic_bp = models.IntegerField(null=True, blank=True, help_text='mmHg')
    diastolic_bp = models.IntegerField(null=True, blank=True, help_text='mmHg')
    heart_rate_bpm = models.IntegerField(null=True, blank=True, help_text='beats per minute')
    temperature_celsius = models.FloatField(null=True, blank=True, help_text='°C')
    respiratory_rate = models.IntegerField(null=True, blank=True, help_text='breaths per minute')
    oxygen_saturation = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='%')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']
        verbose_name_plural = "Vital Signs"

    def __str__(self):
        return f"{self.user.username} - {self.date} {self.time}"


class HealthMetric(models.Model):
    METRIC_TYPES = [
        ('weight', 'Weight'),
        ('height', 'Height'),
        ('sleep', 'Sleep Hours'),
        ('exercise', 'Exercise Minutes'),
        ('water_intake', 'Water Intake (ml)'),
        ('mood', 'Mood Score'),
        ('stress', 'Stress Level'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_metrics')
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    value = models.FloatField()
    date = models.DateField()
    notes = models.TextField(blank=True)
    
    # Goal tracking fields
    target_value = models.FloatField(null=True, blank=True, help_text='Target goal value')
    goal_date = models.DateField(null=True, blank=True, help_text='Target date to achieve goal')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'metric_type', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.get_metric_type_display()} - {self.date}"
    
    @property
    def progress_percentage(self):
        """Calculate progress towards goal"""
        if self.target_value and self.target_value > 0:
            return min((self.value / self.target_value) * 100, 100)
        return 0
    
    @property
    def is_goal_achieved(self):
        """Check if goal is achieved"""
        if self.target_value:
            return self.value >= self.target_value
        return False
