from django.shortcuts import render

from . import models


def index(request):
    context = dict()
    if request.method == 'GET':
        return render(request, 'crawler/list_node.html', context)
