from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from . import models


def index(request):
    context = dict()
    if request.method == 'GET':
        context["nodes"] = models.CrawlerNode.objects.all()
        return render(request, 'crawler/list_node.html', context)


@csrf_exempt
def add_node(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        host = request.POST.get("host")
        port = request.POST.get("port")
        node = models.CrawlerNode(name=name, host=host, port=port)
        node.save()

        messages.add_message(request, messages.SUCCESS, 'Crawler Node Added.')
        return redirect(reverse("crawler:index"))
