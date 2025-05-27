from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from collections import Counter
import json

def login_view(request):
    if request.user.is_authenticated:
        return redirect('users')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def users_view(request):
    user = get_user_model()
    all_users = CustomUser.objects.all()
    return render(request, 'users.html', {'all_users': all_users})

@login_required
def user_stats_view(request):
    user = get_user_model()
    total_users = CustomUser.objects.count()
    all_users = CustomUser.objects.all()
    return render(request, 'user_stats.html', {'total_users': total_users, 'all_users': all_users})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def get_age_bucket(age):
    if age <= 10:
        return '0-10'
    elif age <= 20:
        return '11-20'
    elif age <= 30:
        return '21-30'
    elif age <= 40:
        return '31-40'
    elif age <= 50:
        return '41-50'
    elif age <= 60:
        return '51-60'
    else:
        return '60+'

@login_required
def age_chart_view(request):
    ages = CustomUser.objects.values_list('age', flat=True)

    age_buckets = {'0-10': 0, '11-20': 0, '21-30': 0, '31-40': 0, '41-50': 0, '51-60': 0, '60+': 0}
    for age in ages:
        bucket = get_age_bucket(age)
        age_buckets[bucket] += 1

    context = {
        'age_labels': json.dumps(list(age_buckets.keys())),
        'age_data': json.dumps(list(age_buckets.values())),
    }
    return render(request, 'age_chart.html', context)