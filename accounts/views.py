from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else: #for the get request which happens when a user navigates to the page, show the user an empty form.
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def account_settings(request):
    if request.method == 'POST':
        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, 'Your password was successfully updated!')
                return redirect('account_settings')
        elif 'delete_account' in request.POST:
            # Optional: Add confirmation logic here
            request.user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('register')
    else:
        password_form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/account_settings.html', {
        'password_form': password_form
    })