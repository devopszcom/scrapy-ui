"""
Client for scrapyd API
Visit: https://scrapyd.readthedocs.io/en/stable/overview.html

@author: cuongnb14@gmail.com
"""
import requests


class ScraydAPI:
    def __init__(self, host="localhost", port=6800):
        self.base_url = "http://{}:{}".format(host, port)

    def daemonstatus(self):
        response = requests.get("{}/daemonstatus.json".format(self.base_url))
        return response.json()

    def schedule(self, spider, project='default'):
        data = {
            "project": project,
            "spider": spider,
        }
        response = requests.post("{}/schedule.json".format(self.base_url), data=data)
        return response.json()

    def listjobs(self, project='default'):
        params = {
            'project': project
        }
        response = requests.get("{}/listjobs.json".format(self.base_url), params=params)
        return response.json()

    def listspiders(self, project='default'):
        params = {
            'project': project
        }
        response = requests.get("{}/listspiders.json".format(self.base_url), params=params)
        return response.json()

    def listprojects(self):
        response = requests.get("{}/listprojects.json".format(self.base_url))
        return response.json()["projects"]

    def cancel(self, job, project='default'):
        params = {
            'project': project,
            'job': job,
        }
        response = requests.post("{}/cancel.json".format(self.base_url), params=params)
        return response.json()
