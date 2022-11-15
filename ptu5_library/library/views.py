from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
#from django.http import HttpResponse
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
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count + 1

    #context - obj, kuri pasiduoda i templates
    context = {
        'book_count': book_count, #ivadas: reiksme
        'book_instances_count': book_instances_count,
        'book_instances_available_count': book_instances_available_count,
        'author_count': author_count,
        'genre_count': Genre.objects.count(),#zanrus pasiduodam cia, tokiu budu
        'visits_count': visits_count,

    }

    return render(request, 'library/index.html', context)
    #return render - nupies template
    #gautas request
    #template pavadinimas, savo apps katalogo pavadinimas,
        #irasomas tas, kuris pirmas yra settings.py/installed_apps
    #context - visada trecias argumentas

def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    return render(request, 'library/authors.html', {'authors': paged_authors}) 


def author(request, author_id):
    #per author_id galesim matyti, koki authoriu norim matyti
    return render(request, 'library/author.html', {'author': get_object_or_404(Author, id=author_id)})
    #jeigu nerastume ogjekto, mums ismes puslapi su 404 klaida

class BookListView(ListView):#paveldi ListView
    model = Book
    paginate_by = 3
    template_name = 'library/book_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()#perimam queryset funkc
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(summary__icontains=query))
        genre_id = self.request.GET.get('genre_id')#pasiduodam genre per GET parametra
        #susikuriam genre_id kintamaji, panaudosim filtravimui       
        if genre_id:#cia pasitikrinam ar filtruoja
            queryset = queryset.filter(genre__id=genre_id)
            #genre - yra manytomany todel __ naudojami
            #saite paieskai vykdoma per ? - 127.0.0.1:8000/books/?genre_id=1
            # =1 - zanru id, irasius kita skaiciu, ismes kita zanra 
        return queryset


    #vienintelis budas isgauti genre pavadinimus ir skaitliuka
    #1 = suskaiciuoti knygoms
    #2 = isgauti genre pavadinima
    #3 = genre context, prisideda pildant book_list.html
    def get_context_data(self, **kwargs):#1
        context = super().get_context_data(**kwargs)#1
        #su super pasiemam visa kontext kuri buvom iki siol 
        # suformave ir pridedam savo kintamaji.
        #context['book_count'] = Book.objects.count()#kitas variant susk. knygas
        context['book_count'] = self.get_queryset().count()#1#suskaiciuojam knygas
        # self.get_queryset() - grazina nurodyto objekto sarasa
        genre_id = self.request.GET.get('genre_id')#2
        context['genres'] = Genre.objects.all()#3
        if genre_id:#2
            context['genre'] = get_object_or_404(Genre, id=genre_id)#2
        return context#1


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'

