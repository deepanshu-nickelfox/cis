from django.db import models
from django_extensions.db.models import TimeStampedModel
from core.mixins import LoggingMixin
from locations.models import Location


class Item(TimeStampedModel):
    location = models.ForeignKey(Location)


class ItemLog(Item, LoggingMixin):
    pass

