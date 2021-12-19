# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Product(models.Model):
    GENDER_CATEGORIES= [
        ('Male', 'Мужчина'),
        ('Female', 'Женщина'),     
    ]
    name = models.CharField('имя',max_length=20)
    secondname = models.CharField('фамилия',max_length=120)
    manid = models.IntegerField('ID')
    gender = models.CharField(max_length=50, choices= GENDER_CATEGORIES)

    data = models.CharField(max_length=10)

    def __str__(self):
        return self.name

