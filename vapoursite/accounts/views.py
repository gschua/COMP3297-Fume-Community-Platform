from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
from django.utils import timezone
from .forms import UserLoginForm, UserRegisterForm, UserChangeEmailForm


def login_view(request):
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)

        if next:
            return redirect(next)

        return redirect("/")

    return render(request, "vapoursite/form.html", {"form":form, "title": title})

def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.acc_spending = 5.0
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        if next:
            return redirect(next)

        return redirect("/")

    context = {
        "form": form,
        "title": title
    }

    return render(request, "vapoursite/form.html", context)

def logout_view(request):
    logout(request)
    return redirect("/")

def change_email_view(request):
    next = request.GET.get('next')
    title = "Change email"
    form = UserChangeEmailForm(request.POST or None)
    user=request.user

    if request.method =='POST':
        if form.is_valid():
            email=form.cleaned_data.get("new_email")
            user.email=email
            user.save()
            if next:
                return redirect(next)
            return redirect("/")
    else:
        return render(request, "vapoursite/form.html", {"form":form, "title": title})   
