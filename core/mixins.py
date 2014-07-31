from django.db import models


class LoggingMixin(models.Model):

    class Meta:
        abstract = True
