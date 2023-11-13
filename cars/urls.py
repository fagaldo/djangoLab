from django.urls import path, include
from .views import index, add, get, edit, delete_car

urlpatterns = [
    path('', index, name="view_cars"),
    path('add/', add, name="add"),
    path('<int:id>/', get, name='get'),
    path('<int:id>/edit/', edit, name="edit"),
    path('<int:id>/delete/', delete_car, name="delete_car"),
    path('edit/', edit, name="edit")
]
