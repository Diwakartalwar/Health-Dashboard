from django import forms
from .models import BloodReport, VitalSigns, HealthMetric
from datetime import date


class BloodReportForm(forms.ModelForm):
    class Meta:
        model = BloodReport
        fields = [
            'date', 'hemoglobin_g_dl', 'hematocrit_percent', 'wbc_k_ul', 'platelets_k_ul',
            'glucose_mg_dl', 'creatinine_mg_dl', 'bun_mg_dl',
            'total_cholesterol_mg_dl', 'ldl_cholesterol_mg_dl', 'hdl_cholesterol_mg_dl', 'triglycerides_mg_dl',
            'ast_u_l', 'alt_u_l'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hemoglobin_g_dl': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'hematocrit_percent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'wbc_k_ul': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'platelets_k_ul': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'glucose_mg_dl': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'creatinine_mg_dl': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bun_mg_dl': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'total_cholesterol_mg_dl': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'ldl_cholesterol_mg_dl': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'hdl_cholesterol_mg_dl': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'triglycerides_mg_dl': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'ast_u_l': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'alt_u_l': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = date.today()


class VitalSignsForm(forms.ModelForm):
    class Meta:
        model = VitalSigns
        fields = ['date', 'time', 'systolic_bp', 'diastolic_bp', 'heart_rate_bpm', 'temperature_celsius', 'respiratory_rate', 'oxygen_saturation']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'systolic_bp': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'diastolic_bp': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'heart_rate_bpm': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'temperature_celsius': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'respiratory_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'oxygen_saturation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = date.today()


class HealthMetricForm(forms.ModelForm):
    class Meta:
        model = HealthMetric
        fields = ['metric_type', 'value', 'date', 'notes', 'target_value', 'goal_date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'metric_type': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'target_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Set your goal target'}),
            'goal_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False
        self.fields['target_value'].required = False
        self.fields['goal_date'].required = False
        
        # Add helpful labels
        self.fields['target_value'].label = 'Goal Target (Optional)'
        self.fields['goal_date'].label = 'Goal Date (Optional)'
        if not self.instance.pk:
            self.fields['date'].initial = date.today()
