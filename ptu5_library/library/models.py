from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
import uuid#unique identifier, random generuojamas id


# Create your models here.

class Genre(models.Model):#is models paveldi Model
    name = models.CharField(_('name'), max_length=200, help_text=_('Enter name of book genre'))
    #help_text padeda useriui ka reikia irasyti
    #CharField yra laukeliai kuriuose bus ivedama info

    def __str__(self) -> str:#type def ->
        return self.name#siuo atveju visada bus return self.name

    def link_filtered_books(self):
        link = reverse('books')+'?genre_id='+str(self.id)
        return format_html('<a class="genre" href="{link}">{name}</a>', link=link, name=self.name)

class Author(models.Model):
    first_name = models.CharField(_('first_name'), max_length=50)#first name
    last_name = models.CharField(_('last_name'), max_length=50)#last name

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def display_books(self) -> str:
        return ', '.join(book.title for book in self.books.all())
    display_books.short_description = _('books')#padaro trumpa lauko pavadinima

    def link(self) -> str:
        link = reverse('author', kwargs={'author_id': self.id})
        #reverse in python == url in html
        #reverse suformuoja adresa
        return format_html('<a href="{link}">{author}</a>', link=link, author=self.__str__())
        #format_html - yra saugi funkcija, suformuojanm link.
            #migraciju daryti nereikia
        #galima padaryti author=self.author in class Book, tada nelieka <>

    class Meta:# aprasomas papild funkcionalumas kreipimuisi i DB
        ordering = ['last_name', 'first_name']
        #verbose_name = 'Author'
        #verbose_name_plural = 'Authors'
        #ordering yra rusiavimas, nurodomas, kaip sarasas []
        #rusiuoja pagal pavarde, paskui varda
        #class Meta aprasomoji klase klaseje


class Book(models.Model):
    title = models.CharField(_('title'), max_length=200)
    summary = HTMLField(_('summary'))#textField, bus tuscias didelis laukas, neribotas kiekis simboliu
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True,
        help_text=_('<a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN code</a> consisting of 13 symbols'))
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name ='books')
    #related_name - parodo kokias knygas parase autoriai
    #pasirasom funkc i Author def display_books
    genre = models.ManyToManyField(Genre, help_text=_('Choose genre(s) for this book'), verbose_name=_('genre(s)'))
    cover = models.ImageField(_("cover"), upload_to="covers", blank=True, null=True)
    # null=True ir blank=True leidzia palikti laukeli tuscia is ISBN
    #null=True yra nuoroda BD
    #blank=True yra nuoroda adminui django, formoms
    #ForeignKey - sasajos tarp lenteliu. pirmoje vietoje nurodo i kur eina sasaja(Author)
    #on_delete yra BUTINA SALYGA
    #SET_NULL - jeigu istrinsim Author, jam bus priskirtos null reiksmes
    #PROTECT - neleis istrinti Author, jeigu jis turi knygu
    #CASCADE - jeigu trinsi Author, istrins ir jo knygas
    #verbose_name - gali buti vns ar dgs, nusirodo papildomai foreignkey
    def __str__(self) -> str:
        return f"{self.author} {self.title}"

    def display_genre(self) -> str:
        #si eilute grazina genre sarasa per kableli iki 3
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = _('genre')
        #', ' naudojamas kai bus daugiau negu 2 zanrai
        #[:3] apribojimas ima iki 3 genre


class BookInstance(models.Model):
    unique_id = models.UUIDField(_('unique ID'), default=uuid.uuid4, editable=False)#editable - neleis redaguoti
    book = models.ForeignKey(Book, verbose_name=_('book'), on_delete=models.CASCADE)
    due_back = models.DateField(_('due back'), null=True, blank=True)
    #due_back DateField- suformuoja kalendoriu saite su grazinimo laiku
    #uuid1 - generuoja pagal hostid, eiliskuma ir dabartini laika
    #uuid4 - random id
    #uuid3 ir uuid5 - reikia paduoti teksto pagal kuri generuos
    #editable=False - neleidzia redaguoti unique reiksmes
    LOAN_STATUS = (#pasirinkimu laukas saite, konstanta kuria naudosim lauko viduje
    # del to rasoma didziosiomis raidemis
        ('m', _("managed")),
        ('t', _("taken")),
        ('a', _("available")),
        ('r', _("reserved"))
    )

    status = models.CharField(_('status'), max_length=1, choices=LOAN_STATUS, default='m')
    #choices - sukuria pasirinkimu laukeli
    #max_length1 - DB saugosim tik 1 simboli
    #price = models.DecimalField('price', max_digits=18, decimal_places=2)
    #max_digits - kiek max skaitmenu skaiciuje
    #decimal_places - kiek skaiciu po kablelio
    reader = models.ForeignKey(
        get_user_model(),
        verbose_name=_('reader'),
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name= 'taken_books',
    )

    @property
    def is_overdue(self):
        if self.due_back and self.due_back < datetime.date(datetime.now()):
            return True
        return False


    def __str__(self) -> str:
        return f"{self.unique_id} {self.book.title}"

    class Meta:
        ordering = ['due_back']


class BookReview(models.Model):
    book = models.ForeignKey(Book, verbose_name=_('book'), on_delete=models.CASCADE, related_name='reviews')
    reader = models.ForeignKey(get_user_model(), verbose_name=_('reader'), on_delete=models.CASCADE, related_name='book_reviews')
    #related_name - kad atiduotu atgal, kas yra su jais susije
    created_at =models.DateTimeField(_('created at'), auto_now_add=True)
    content = models.TextField(_("content"), max_length=10000)

    def __str__(self):
        return f"{self.reader} on {self.book} at {self.created_at}"

    class Meta:
        ordering = ('-created_at', )
