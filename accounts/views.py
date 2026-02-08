from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard:overview')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile.age = form.cleaned_data.get('age') or user_profile.age
            user_profile.gender = form.cleaned_data.get('gender') or user_profile.gender
            user_profile.height_cm = form.cleaned_data.get('height_cm') or user_profile.height_cm
            user_profile.weight_kg = form.cleaned_data.get('weight_kg') or user_profile.weight_kg
            user_profile.save()
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(initial={
            'age': user_profile.age,
            'gender': user_profile.gender,
            'height_cm': user_profile.height_cm,
            'weight_kg': user_profile.weight_kg,
        })
    
    return render(request, 'accounts/profile.html', {'form': form, 'profile': user_profile})
