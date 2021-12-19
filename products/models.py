# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120)
    text = models.TextField()

    data = models.CharField(max_length=10)

    def __str__(self):
        return self.name

