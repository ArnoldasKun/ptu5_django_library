from django.contrib import admin
from . import models

# Register your models here.

class BookInstanceInline(admin.TabularInline):
    #kad butu galima matyti ir redaguoti visus instance, tam reikia inline
    #ir aprasom inlines i BookAdmin
    model = models.BookInstance
    extra = 0#nusako kad dirbtinai bus sukuriama 0 instance eiluciu
    #readonly_fields = ('unique_id', )
    #sukuria naujus id uzsakymu lenteleje
    can_delete = False#redaguoti permisions


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')#sukuria naujus stulpeliu pavadinimus
    #naudoti kintamaji pavadinima is models
    #display_genre reikia suskurti i models.py def display_genre(self)
    inlines = (BookInstanceInline, )
    


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'book', 'status', 'due_back', 'reader')#sukuria nauju stulpeliu reiksmes
    #naudoti kintamaji pavadinima is models
    list_filter = ('status', 'due_back')#ivardijam laukus pagal kuriuos filtruosim
    readonly_fields = ('unique_id', 'is_overdue' )
    #editable padaro kad nerodytu, bet readonly grazina, kad rodytu, bet neleidzia redaguoti
    # kablelis parodo tuple ir sudaro jungima
    search_fields = ('unique_id', 'book__title', 'book__author__last_name', 'reader__last_name')#paieskos laukai
    #book__title - 'django lookups', book yra foreignkey
    list_editable = ('status', 'due_back', 'reader')#laukai redaguojami paciame liste

    fieldsets = (#nustato lauku tvarka, tuple tuplese
        ('General', {'fields': ('unique_id', 'book')}),
        #general - antraste,
        #fields - laukai, kaip diktas
        #kad galetume naudoti 'unique_id', pasidarom readonly_fields i BookInstanceAdmin 
        ('Availability', {'fields': (('status', 'due_back', 'is_overdue'), 'reader')}),
        #availability - antraste
        #fields - laukai, kaip diktas
        #papildomi () padaro horizontaliai vienoje eiluteje status ir due_back
    )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_books')#sukuria naujus stulpelius
    #naudoti kintamaji pavadinima is models
    #display_books reikia suskurti i models.py def display_books(self)
    list_display_link = ('last_name', )#ant kuriu stulpeliu linkai rasysis


class BookReviewAdmin(admin.ModelAdmin):
    list_display= ('book', 'reader', 'created_at')


admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.BookInstance, BookInstanceAdmin)
admin.site.register(models.BookReview, BookReviewAdmin)
