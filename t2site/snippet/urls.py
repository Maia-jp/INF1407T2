from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.new, name='new'),
    path('<str:id>/edit',views.snippetEdit, name='snippetEdit'),
    path('<str:id>',views.snippetTemplate, name='snippetTemplate'),
]