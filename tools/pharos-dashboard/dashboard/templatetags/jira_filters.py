from django.template.defaultfilters import register

from django.conf import settings


@register.filter
def jira_issue_url(issue):
    return settings.JIRA_URL + '/browse/' + str(issue)
