from django.shortcuts import render
from django.http import HttpResponse
from . models import Genre, Author, Book, BookInstance
# Create your views here.

def index(request):
    #return HttpResponse("Sveiki atvyke")#irasom ka norim ()

    # views gali buti 2 tipu funkciniai ir class based
    #funkciniai visada reikalauja request

    #Susirenkam duomenis is models.py
    # 4 skaitliukai
    book_count = Book.objects.count()#kiek knygu
    book_instances_count = Book.objects.count()#kiek kopiju
    #jeigu kintamasis iki 6 zodziu, gali buti aprasytas, paskui trumpinamas
    book_instances_available_count = BookInstance.objects.filter(status='a').count()#kiek avalaible knygu
    # status = 'a' - available
    author_count = Author.objects.count()#kiek autoriu

    #context - obj, kuri pasiduoda i templates
    context = {
        'book_count': book_count, #ivadas: reiksme
        'book_instances_count': book_instances_count,
        'book_instances_available_count': book_instances_available_count,
        'author_count': author_count,
        'genre_count': Genre.objects.count()#zanrus pasiduodam cia, tokiu budu

    }

    return render(request, 'library/index.html', context)
    #return render - nupies template
    #gautas request
    #template pavadinimas, savo apps katalogo pavadinimas,
        #irasomas tas, kuris pirmas yra settings.py/installed_apps
    #context - visada trecias argumentas