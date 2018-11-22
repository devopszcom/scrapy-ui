from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .scrapyd import ScraydAPI

from . import models


def index(request):
    context = dict()
    if request.method == 'GET':
        nodes = models.CrawlerNode.objects.all()
        for node in nodes:
            try:
                scrapy_client = ScraydAPI(host=node.host, port=node.port)
                node.projects = scrapy_client.listprojects()
            except Exception:
                node.projects = []

        context["nodes"] = nodes
        return render(request, 'crawler/list_node.html', context)


def status_node(request, node_id):
    context = dict()
    if request.method == 'GET':
        context["nodes"] = models.CrawlerNode.objects.all()
        return render(request, 'crawler/status_node.html', context)


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
