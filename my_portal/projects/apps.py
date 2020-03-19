from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'my_portal.projects'

    def ready(self):
        try:
            import my_portal.projects.signals  # noqa F401
        except ImportError:
            pass