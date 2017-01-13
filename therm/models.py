from __future__ import unicode_literals

from django.db import models
from thermo.chemical import Chemical

class Chems(models.Model):
    name = models.CharField(max_length = 100)
    chemnum = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

