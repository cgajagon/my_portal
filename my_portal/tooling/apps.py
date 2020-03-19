from django.apps import AppConfig

class ToolingConfig(AppConfig):
    name = 'my_portal.tooling'

    def ready(self):
        try:
            import my_portal.tooling.signals  # noqa F401
        except ImportError:
            pass
