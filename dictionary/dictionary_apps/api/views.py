from django.shortcuts import render


def main_page(request):

    return render(request, 'main_page.html')


def detail_object(request):
    return render(request, 'property/property_object_detail.html')