import dashboard.jenkins.jenkins_adapter as jenkins
import re


def parse_slave_data(slave_dict, slave):
    slave_dict['status'] = get_slave_status(slave)
    slave_dict['status_color'] = get_status_color(slave)
    slave_dict['slaveurl'] = get_slave_url(slave)
    job = jenkins.get_jenkins_job(slave['displayName'])
    if job is not None:
        slave_dict['last_job'] = parse_job(job)


def parse_job(job):
    result = parse_job_string(job['lastBuild']['fullDisplayName'])
    result['url'] = job['url']
    result['color'] = get_job_color(job)
    if job['lastBuild']['building']:
        result['blink'] = 'class=blink_me'
    return result


def parse_job_string(full_displayname):
    job = {}
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


# TODO: use css
def get_job_color(job):
    if job['lastBuild']['building'] is True:
        return '#646F73'
    result = job['lastBuild']['result']
    if result == 'SUCCESS':
        return '#33cc00'
    if result == 'FAILURE':
        return '#FF5555'
    if result == 'UNSTABLE':
        return '#EDD62B'


# TODO: use css
def get_status_color(slave):
    if not slave['offline'] and slave['idle']:
        return '#C8D6C3'
    if not slave['offline']:
        return '#BEFAAA'
    return '#FAAAAB'


def get_slave_url(slave):
    return 'https://build.opnfv.org/ci/computer/' + slave['displayName']


def get_slave_status(slave):
    if not slave['offline'] and slave['idle']:
        return 'online / idle'
    if not slave['offline']:
        return 'online'
    return 'offline'
