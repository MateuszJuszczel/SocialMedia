from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request,  *args, **kwargs):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save(*args, **kwargs)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Twoje konto {username} zostalo stowrzone!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
@transaction.atomic
def profile_user(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Twoje dane zostaly zaktualizowane')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    ctx = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
    return render(request, 'users/profile.html', ctx)
