from django.urls import path, include
from .views import index, add, get, edit, delete_news

urlpatterns = [
    path('', index, name="view_news"),
    path('add/', add, name="add"),
    path('<int:id>/', get, name='get'),
    path('<int:id>/edit/', edit, name="edit"),
    path('<int:id>/delete/', delete_news, name="delete_news"),
    path('edit/', edit, name="edit")
]
