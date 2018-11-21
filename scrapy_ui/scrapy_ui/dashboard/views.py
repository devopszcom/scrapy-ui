from django.shortcuts import render


def index(request):
    context = dict()
    if request.method == 'GET':
        return render(request, 'base.html', context)
