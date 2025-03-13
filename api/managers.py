from django.db import models


class DefaultManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class VisibleObjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class NonVisibleObjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_visible=False)

