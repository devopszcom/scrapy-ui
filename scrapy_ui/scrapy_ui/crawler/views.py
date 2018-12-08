from datetime import datetime

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


def status_node(request, node_id, project_name):
    context = dict()
    node = models.CrawlerNode.objects.get(pk=node_id)
    scrapy_client = ScraydAPI(host=node.host, port=node.port)
    status = scrapy_client.daemonstatus()

    spiders = scrapy_client.listspiders()["spiders"]

    jobs = scrapy_client.listjobs()

    jobs['finished'] = list(reversed(jobs['finished']))[:15]

    for job in jobs['finished']:
        during = datetime.strptime(job["end_time"], "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(
            job["start_time"], "%Y-%m-%d %H:%M:%S.%f")
        job["during"] = during.total_seconds() / 60

    context['status'] = status
    context['jobs'] = jobs
    context['spiders'] = spiders
    context['log_url'] = ""
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
