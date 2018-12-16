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
        job["during_unit"] = "minutes"
        if job["during"] > 60:
            job["during"] = job["during"] / 60
            job["during_unit"] = "hours"

    context['status'] = status
    context['node'] = node
    context['project_name'] = project_name
    context['jobs'] = jobs
    context['spiders'] = spiders
    context['log_url'] = "http://{}:{}/logs/{}".format(node.host, node.port, project_name)
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


@csrf_exempt
def delete_node(request, node_id):
    if request.method == 'POST':
        node = models.CrawlerNode.objects.get(pk=node_id)
        node.delete()
        messages.add_message(request, messages.SUCCESS, 'Deleted Node: {}'.format(node_id))
        return redirect(reverse("crawler:index"))

@csrf_exempt
def add_job(request, node_id, project_name, spider_name):
    node = models.CrawlerNode.objects.get(pk=node_id)
    scrapy_client = ScraydAPI(host=node.host, port=node.port)
    result = scrapy_client.schedule(spider_name, project_name)
    if result["status"] == "ok":
        messages.add_message(request, messages.SUCCESS, 'Job id: {}'.format(result["jobid"]))
    else:
        messages.add_message(request, messages.ERROR, '{}'.format(result["message"]))
    return redirect(reverse("crawler:status_node", kwargs={"node_id": node.id, "project_name": project_name}))


@csrf_exempt
def cancel_job(request, node_id, project_name, job_id):
    node = models.CrawlerNode.objects.get(pk=node_id)
    scrapy_client = ScraydAPI(host=node.host, port=node.port)
    result = scrapy_client.cancel(job_id, project_name)
    if result["status"] == "ok":
        messages.add_message(request, messages.SUCCESS, 'Cancel job id: {}. Received SIGTERM, shutting down gracefully. Please wait or send again to force'.format(job_id))
    else:
        messages.add_message(request, messages.ERROR, '{}'.format(result["message"]))
    return redirect(reverse("crawler:status_node", kwargs={"node_id": node.id, "project_name": project_name}))
