from django.shortcuts import render




def show_mysite(request):
    return render(request, 'show.html')

