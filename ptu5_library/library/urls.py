from django.urls import path
from . import views
#toks buna visada su 3 argumentais
# nurodomas kelias, kuris paliekamas tuscias
#nurodom koks views naudojamas, su apsirasytu is views.py
# ir kaip vadinsis puslapis su pavadinimu
urlpatterns =[
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book')
]