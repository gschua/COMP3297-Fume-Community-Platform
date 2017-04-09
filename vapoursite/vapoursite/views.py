from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )
# Create your views here.

def main_view(request):
    return render(request, "vapoursite/main.html", {})

#redirected to login page if not logged in user tries to access this view
@login_required(login_url='/login/')
def loginmain_view(request):
    return render(request, "vapoursite/main-loggedin.html", {})
