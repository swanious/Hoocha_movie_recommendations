from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods, require_safe
from django.contrib.auth import get_user_model, update_session_auth_hash

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomLoginForm, CustomPasswordChangeForm
from .serializers import CustomUserChangeSerializer

# Create your views here.
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
        
    if request.method == 'POST':
        form = CustomLoginForm(request, request.POST)
        if form.is_valid():
            # 로그인
            auth_login(request, form.get_user())
            print(request.GET.get('next'))
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = CustomLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


@api_view(['POST'])
def update(request):
    if request.user.is_authenticated:
        serializer = CustomUserChangeSerializer(data=request.data, instance=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data' : 'success'})


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('movies:index')


@login_required
@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile', request.user.username)
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {'form': form}
    return render(request, 'accounts/change_password.html', context)


def profile(request, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)