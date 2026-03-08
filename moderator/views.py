from django.shortcuts import render


def dashboard(request):
    return render(request, 'moderator/dashboard.html')
