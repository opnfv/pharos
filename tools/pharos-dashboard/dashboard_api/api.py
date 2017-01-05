##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


import logging

import requests

URLS = {
    'resources': '/api/resources/',
    'servers': '/api/servers/',
    'bookings': '/api/bookings',
    'resource_status': '/api/resource_status/',
}

class DashboardAPI(object):
    def __init__(self, dashboard_url, api_token='', verbose=False):
        self._api_token = api_token
        self._verbose = verbose
        self._resources_url = dashboard_url + URLS['resources']
        self._servers_url = dashboard_url + URLS['servers']
        self._bookings_url = dashboard_url + URLS['bookings']
        self._resources_status_url = dashboard_url + URLS['resource_status']
        self._logger = logging.getLogger(__name__)

    def get_all_resources(self):
        return self._get_json(self._resources_url)

    def get_resource(self, id='', name='', url=''):
        if url != '':
            return self._get_json(url)[0]
        url = self._resources_url + self._url_parameter(id=id, name=name)
        return self._get_json(url)[0]

    def get_all_bookings(self):
        return self._get_json(self._bookings_url)

    def get_resource_bookings(self, resource_id):
        url = self._bookings_url + self._url_parameter(resource_id=resource_id)
        return self._get_json(url)

    def get_booking(self, id):
        url = self._bookings_url + self._url_parameter(id=id)
        return self._get_json(url)[0]

    def post_resource_status(self, resource_id, type, title, content):
        data = {
            'resource': resource_id,
            'type': type,
            'title': title,
            'content': content
        }
        return self._post_json(self._resources_status_url, data)

    def get_url(self, url):
        return self._get_json(url)

    def _url_parameter(self, **kwargs):
        res = ''
        prefix = '?'
        for key, val in kwargs.items():
            res += prefix + key + '=' + str(val)
            prefix = '&'
        return res

    def _get_json(self, url):
        try:
            response = requests.get(url)
            if self._verbose:
                print('Get JSON: ' + url)
                print(response.status_code, response.content)
            return response.json()
        except requests.exceptions.RequestException as e:
            self._logger.exception(e)
        except ValueError as e:
            self._logger.exception(e)

    def _post_json(self, url, json):
        if self._api_token == '':
            raise Exception('Need api token to POST data.')
        response = requests.post(url, json, headers={'Authorization': 'Token ' + self._api_token})
        if self._verbose:
            print('Post JSON: ' + url)
            print(response.status_code, response.content)
        return response.status_code
