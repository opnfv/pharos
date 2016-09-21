##############################################################################
# Copyright (c) 2016 Max Breitenfeldt and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################


from django.template.defaultfilters import register


@register.filter
def jenkins_job_color(job_result):
    if job_result == 'SUCCESS':
        return '#5cb85c'
    if job_result == 'FAILURE':
        return '#d9534f'
    if job_result == 'UNSTABLE':
        return '#EDD62B'
    return '#646F73'  # job is still building


@register.filter
def jenkins_status_color(slave_status):
    if slave_status == 'offline':
        return '#d9534f'
    if slave_status == 'online':
        return '#5cb85c'
    if slave_status == 'online / idle':
        return '#5bc0de'


@register.filter
def jenkins_job_blink(job_result):
    if job_result == '':  # job is still building
        return 'class=blink_me'
