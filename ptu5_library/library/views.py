from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
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

def authors(request):
    return render(request, 'library/authors.html', {'authors': Author.objects.all()}) 


def author(request, author_id):
    return render(request, 'library/author.html', {'author': get_object_or_404(Author,
    id=author_id)})

class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_id = self.request.GET.get('genre_id')
        if genre_id:
            queryset = queryset.filter(genre__id=genre_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['book_count'] = Book.objects.count()
        context['book_count'] = self.get_queryset().count()
        genre_id = self.request.GET.get('genre_id')
        context['genres'] = Genre.objects.all()
        if genre_id:
            context['genre'] = get_object_or_404(Genre, id=genre_id)
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'

