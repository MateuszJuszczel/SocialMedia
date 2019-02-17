from django.apps import AppConfig


class UserAdminConfig(AppConfig):
    name = 'userAdmin'

    def ready(self):
        import userAdmin.signals