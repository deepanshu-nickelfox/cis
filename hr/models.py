from django.contrib.auth.models import Group
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=65)
    department = models.ForeignKey(Group, null=True, blank=True)

    class Meta:
        unique_together = (
            ('name', 'department'),
        )
        permissions = (
            ("read_position", "Can read position"),
        )
