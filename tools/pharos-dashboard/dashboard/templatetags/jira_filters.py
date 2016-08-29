from django.template.defaultfilters import register

from pharos_dashboard import settings


@register.filter
def jira_issue_url(issue):
    return settings.JIRA_URL + '/browse/' + str(issue)
