from django.shortcuts import render
from django.http import HttpResponse

def currentgame(request):
    
    return render(request, 'boxscores.html')
    


