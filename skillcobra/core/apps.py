import contextlib

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "skillcobra.core"
    def ready(self):
        with contextlib.suppress(Exception):
            from skillcobra.ml.dataset import save_training_model
            save_training_model()
