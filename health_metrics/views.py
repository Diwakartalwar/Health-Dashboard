from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import BloodReport, VitalSigns, HealthMetric
from .forms import BloodReportForm, VitalSignsForm, HealthMetricForm
from .serializers import BloodReportSerializer, VitalSignsSerializer, HealthMetricSerializer


class BloodReportViewSet(viewsets.ModelViewSet):
    serializer_class = BloodReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BloodReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VitalSignsViewSet(viewsets.ModelViewSet):
    serializer_class = VitalSignsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VitalSigns.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HealthMetricViewSet(viewsets.ModelViewSet):
    serializer_class = HealthMetricSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HealthMetric.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Views for web interface
@login_required
@require_http_methods(["GET", "POST"])
def add_blood_report(request):
    if request.method == 'POST':
        form = BloodReportForm(request.POST)
        if form.is_valid():
            blood_report = form.save(commit=False)
            blood_report.user = request.user
            blood_report.save()
            return redirect('health_metrics:blood_report_list')
    else:
        form = BloodReportForm()

    return render(request, 'health_metrics/add_blood_report.html', {'form': form})


@login_required
def blood_report_list(request):
    blood_reports = BloodReport.objects.filter(user=request.user)
    return render(request, 'health_metrics/blood_report_list.html', {'blood_reports': blood_reports})


@login_required
@require_http_methods(["GET", "POST"])
def edit_blood_report(request, pk):
    blood_report = get_object_or_404(BloodReport, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = BloodReportForm(request.POST, instance=blood_report)
        if form.is_valid():
            form.save()
            return redirect('health_metrics:blood_report_list')
    else:
        form = BloodReportForm(instance=blood_report)

    return render(request, 'health_metrics/edit_blood_report.html', {'form': form, 'blood_report': blood_report})


@login_required
@require_http_methods(["POST"])
def delete_blood_report(request, pk):
    blood_report = get_object_or_404(BloodReport, pk=pk, user=request.user)
    blood_report.delete()
    return redirect('health_metrics:blood_report_list')


@login_required
@require_http_methods(["GET", "POST"])
def add_vital_signs(request):
    if request.method == 'POST':
        form = VitalSignsForm(request.POST)
        if form.is_valid():
            vital_signs = form.save(commit=False)
            vital_signs.user = request.user
            vital_signs.save()
            return redirect('health_metrics:vital_signs_list')
    else:
        form = VitalSignsForm()

    return render(request, 'health_metrics/add_vital_signs.html', {'form': form})


@login_required
def vital_signs_list(request):
    vital_signs = VitalSigns.objects.filter(user=request.user)
    return render(request, 'health_metrics/vital_signs_list.html', {'vital_signs': vital_signs})


@login_required
@require_http_methods(["GET", "POST"])
def add_health_metric(request):
    if request.method == 'POST':
        form = HealthMetricForm(request.POST)
        if form.is_valid():
            metric = form.save(commit=False)
            metric.user = request.user
            metric.save()
            return redirect('health_metrics:health_metric_list')
    else:
        form = HealthMetricForm()

    return render(request, 'health_metrics/add_health_metric.html', {'form': form})


@login_required
def health_metric_list(request):
    health_metrics = HealthMetric.objects.filter(user=request.user)
    return render(request, 'health_metrics/health_metric_list.html', {'health_metrics': health_metrics})
