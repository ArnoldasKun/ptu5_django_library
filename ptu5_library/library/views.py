from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Sveiki atvyke")#irasom ka norim ()

    # views gali buti 2 tipu funkciniai ir class based
    #funkciniai visada reikalauja request