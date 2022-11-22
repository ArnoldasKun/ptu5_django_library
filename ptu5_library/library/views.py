from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
#from django.http import HttpResponse
from . models import Genre, Author, Book, BookInstance
from . forms import BookReviewForm
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
    paginator = Paginator(Author.objects.all(), 2)#nurodom objects lista ir kiek matosi puslapyje
    page_number = request.GET.get('page')#pasiemam is request
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
        query = self.request.GET.get('query')#cia darom paieska su query
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(summary__icontains=query))
            #paieska vykdoma pagal title ir summary
        genre_id = self.request.GET.get('genre_id')#pasiduodam genre per GET parametra
        #susikuriam genre_id kintamaji, panaudosim filtravimui
        # i raide nurodo, kad ieskos ir mazasias ir didziasias raides       
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


class BookDetailView(FormMixin, DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    form_class = BookReviewForm

    def get_success_url(self):
        return reverse('book', kwargs={'pk': self.get_object().id})

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(self.request, "You are posting too much!")
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.get_object()
        form.instance.reader = self.request.user
        form.save()
        messages.success(self.request, 'Your review have beed posted')
        return super().form_valid(form)

    def get_initial(self):
        return {
            'book': self.get_object(),
            'reader': self.request.user,
        }

    
class UserBookListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'library/user_book_list.html'
    #paginate_by: 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(reader=self.request.user).order_by('due_back')
        return queryset
        

class UserBookInstanceCreateView(LoginRequiredMixin, CreateView):
    model = BookInstance
    fields = ('book', 'due_back',)
    template_name = 'library/user_bookinstance_form.html'
    success_url = reverse_lazy('user_books')

    def form_valid(self, form):
        form.instance.reader = self.request.user
        form.instance.status = 'r'
        messages.success(self.request, 'Book reserved.')
        return super().form_valid(form)


class UserBookInstanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BookInstance
    fields = ('book', 'due_back',)
    template_name = 'library/user_bookinstance_form.html'
    success_url = reverse_lazy('user_books')

    def form_valid(self, form):
        form.instance.reader = self.request.user
        form.instance.status = 't'
        messages.success(self.request, 'Book taken or extended')
        return super().form_valid(form)

    def test_func(self):
        book_instance = self.get_object()
        return self.request.user == book_instance.reader

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_object().status == 't':
            context['action'] = 'Extend'
        else:
            context['action'] = 'Take'
        return context


class UserBookInstanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BookInstance
    template_name = 'library/user_bookinstance_delete.html'
    success_url = reverse_lazy('user_books')

    def test_func(self):
        book_instance = self.get_object()
        return self.request.user == book_instance.reader

    def form_valid(self, form):
        book_instance = self.get_object()
        if book_instance.status == 't':
            messages.success(self.request, 'Book returned and recycled')
        else:
            messages.success(self.request, 'Book reservation canceled')
        return super().form_valid(form)