import logging

import re
import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)


# TODO: implement caching decorator, cache get_* functions
def get_json(url):
    if cache.get(url) is None:
        try:
            response = requests.get(url)
            json = response.json()
            cache.set(url, json, 180)  # cache result for 180 seconds
            return json
        except requests.exceptions.RequestException as e:
            logger.exception(e)
        except ValueError as e:
            logger.exception(e)
    else:
        return cache.get(url)


def get_all_slaves():
    url = "https://build.opnfv.org/ci/computer/api/json?tree=computer[displayName,offline,idle]"
    json = get_json(url)
    if json is not None:
        return json['computer']  # return list of dictionaries
    return []


def get_slave(slavename):
    slaves = get_all_slaves()
    for slave in slaves:
        if slave['displayName'] == slavename:
            return slave
    return {}


def get_ci_slaves():
    url = "https://build.opnfv.org/ci/label/ci-pod/api/json?tree=nodes[nodeName,offline,idle]"
    json = get_json(url)
    if json is not None:
        return json['nodes']
    return []


def get_all_jobs():
    url = "https://build.opnfv.org/ci/api/json?tree=jobs[displayName,url,lastBuild[fullDisplayName,building,builtOn,timestamp,result]]"
    json = get_json(url)
    if json is not None:
        return json['jobs']  # return list of dictionaries
    return []


def get_jenkins_job(slavename):
    jobs = get_all_jobs()
    max_time = 0
    last_job = None
    for job in jobs:
        if job['lastBuild'] is not None:
            if job['lastBuild']['builtOn'] == slavename:
                if job['lastBuild']['building'] is True:
                    return job  # return active build
                if job['lastBuild']['timestamp'] > max_time:
                    last_job = job
                    max_time = job['lastBuild']['timestamp']
    return last_job


def is_ci_slave(slavename):
    ci_slaves = get_ci_slaves()
    for ci_slave in ci_slaves:
        if ci_slave['nodeName'] == slavename:
            return True
    return False


def is_dev_pod(slavename):
    if is_ci_slave(slavename):
        return False
    if slavename.find('pod') != -1:
        return True
    return False


def parse_job(job):
    result = parse_job_string(job['lastBuild']['fullDisplayName'])
    result['building'] = job['lastBuild']['building']
    result['result'] = ''
    if not job['lastBuild']['building']:
        result['result'] = job['lastBuild']['result']
    result['url'] = job['url']
    return result


def parse_job_string(full_displayname):
    job = {}
    job['scenario'] = ''
    job['installer'] = ''
    job['branch'] = ''
    tokens = re.split(r'[ -]', full_displayname)
    for i in range(len(tokens)):
        if tokens[i] == 'os':
            job['scenario'] = '-'.join(tokens[i: i + 4])
        elif tokens[i] in ['fuel', 'joid', 'apex', 'compass']:
            job['installer'] = tokens[i]
        elif tokens[i] in ['master', 'arno', 'brahmaputra', 'colorado']:
            job['branch'] = tokens[i]
    tokens = full_displayname.split(' ')
    job['name'] = tokens[0]
    return job

def get_slave_url(slave):
    return 'https://build.opnfv.org/ci/computer/' + slave['displayName']


def get_slave_status(slave):
    if not slave['offline'] and slave['idle']:
        return 'online / idle'
    if not slave['offline']:
        return 'online'
    return 'offline'
