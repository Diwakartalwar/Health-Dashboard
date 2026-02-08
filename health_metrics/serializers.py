from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BloodReport, VitalSigns, HealthMetric


class BloodReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodReport
        fields = '__all__'


class VitalSignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSigns
        fields = '__all__'


class HealthMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthMetric
        fields = '__all__'
