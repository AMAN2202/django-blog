from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegistrationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    return render(request, 'registration.html', locals())


@login_required
def createprofile(request):
    obj = get_object_or_404(UserProfile, user=request.user)
    form = UserProfileForm(instance=obj)
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.completed=True
            obj.save()
            return redirect('accounts:profile')
    return render(request, 'editprofile.html', locals())


@login_required
def changepass(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:profile')
    heading = 'Change Password'
    return render(request, 'login.html', locals())


@login_required
def viewprofile(request, id=None):
    if id is None:
        a=UserProfile.objects.get(user=request.user)
        if a.completed:
            u = get_object_or_404(User, username=request.user)
        else:
            return redirect('accounts:edit_profile')
    else:
        u = get_object_or_404(User, pk=id)
    return render(request, 'viewprofile.html', locals())
