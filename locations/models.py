from django.db import models
from django_extensions.db.models import TimeStampedModel


class Service(TimeStampedModel):
    name = models.CharField(max_length=65, unique=True)


class Location(TimeStampedModel):

    net_addr = models.CharField(max_length=15, null=True, blank=True)
    vlan = models.CharField(max_length=65, null=True, blank=True)
    services = models.ManyToManyField(Service, null=True, blank=True)
