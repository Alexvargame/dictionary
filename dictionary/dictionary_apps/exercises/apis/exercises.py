from django.shortcuts import render


def exercises_page(request):

    return render(request, 'exercises/exercises.html')
