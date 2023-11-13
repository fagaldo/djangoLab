from django.shortcuts import render, redirect, get_object_or_404
from .models import Cars
from .forms import CarsForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(request):
    #  Pobranie pozycji z bazy danych
    cars = Cars.objects.order_by('-create_time')
    # Stworzenie słownika przechowującego elementy bazy danych pod zmienną news
    context = {'cars': cars}
    # Przesłanie wyrenderowanej strony wraz z dodanymi elementami z bazy danych
    # elementy ze słownika context wykorzytywane są w pliku news/index.html 
    return render(request, 'cars/index.html', context)

@login_required(login_url='/login/')
def add(request):
    # Sprawdzenie metody jaką przyszło zapytanie HTTP
    # Jeżeli POST - szukamy danych w ciele zapytania
    # Jeżeli GET - wysyłałym formularz do wypełnienia 
    # (można przesyłać dane w zapytaniu GET - 
    # ale w tym rozwiązaniu tego nie wykorzystujemy)
    if request.method == 'POST':
        
        # Formularze w Django umożliwiają sprawdzenie poprawności danych
        # więc tworzymy obiekt formularza z zapytania
        cars = CarsForm(request.POST)

        # Jeżeli formularz - czyli dane przesłane z zapytania POST 
        # są proawidłowe dodajemy element do bazy danych 
        if cars.is_valid():
            cars = cars.save(commit=False)
            # news.author = request.user
            cars.create_time = timezone.now()
            cars.last_edit_time = timezone.now()
            cars.save()
            return redirect('view_cars')
        # Jeżeli nie są prawidłowe przesyłamy formularz z powrotem do kilenta 
        # Autmatyczny walidator tworzy również pola błędów, które są dostępne po
        # stronie klienta
        else:
            context = {'form': cars}
            return render(request, 'cars/add.html', context)
    
    # Jeżeli zapytanie typu GET przesyłamy pusty formularz
    else:
        cars = CarsForm()
        context = {'form': cars}
        return render(request, 'cars/add.html', context)
@login_required(login_url='/login/')
def edit(request, id):
    cars = get_object_or_404(Cars, id=id)
    if request.method == 'POST':
        
        # Formularze w Django umożliwiają sprawdzenie poprawności danych
        # więc tworzymy obiekt formularza z zapytania
        form = CarsForm(request.POST, instance = cars)

        # Jeżeli formularz - czyli dane przesłane z zapytania POST 
        # są proawidłowe dodajemy element do bazy danych 
        if form.is_valid():
            form = form.save(commit=False)
            # news.author = request.user
            form.last_edit_time = timezone.now()
            form.save()
            return redirect('view_cars')
        # Jeżeli nie są prawidłowe przesyłamy formularz z powrotem do kilenta 
        # Autmatyczny walidator tworzy również pola błędów, które są dostępne po
        # stronie klienta
        else:
            
            context = {{'form': form, 'cars': cars}}
            return render(request, 'cars/edit.html', context)
    
    # Jeżeli zapytanie typu GET przesyłamy pusty formularz
    else:
        form = CarsForm(instance = cars)
        return render(request, 'cars/edit.html', {'form': form, 'cars': cars})
@login_required(login_url='/login/')
def delete_car(request, id):
    car = get_object_or_404(Cars, id=id)

    if request.method == 'POST':
        car.delete()
        return redirect('view_cars')  # Zakładając, że masz widok o nazwie 'news_list' dla listy wiadomości

    return render(request, 'cars/delete_car.html', {'cars': car})
@login_required(login_url='/login/')
def get(request, id):
    # funkcja get_object_or_404 zwraca element z bazy 
    # danych o danej wartości argumentu
    # lub przesłyła do kilenta błąd
    cars = get_object_or_404(Cars, id=id)
    context = {'cars': cars}
    return render(request, 'cars/view.html', context)