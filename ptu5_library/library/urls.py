from django.urls import path
from . import views
#toks buna visada su 3 argumentais
# nurodomas kelias, kuris paliekamas tuscias
#nurodom koks views naudojamas, su apsirasytu is views.py
# ir kaip vadinsis puslapis su pavadinimu
urlpatterns =[
    path('', views.index, name='index')
]