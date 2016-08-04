from django.apps import AppConfig


class DashboardConfig(AppConfig):
    name = 'dashboard'
    verbose_name = 'Dashboard'

    def ready(self):
        # make sure signals are loaded: https://docs.djangoproject.com/en/1.9/topics/signals/
        # import dashboard.signals.handlers # noqa
        super(DashboardConfig,self).ready()