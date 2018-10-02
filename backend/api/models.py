from __future__ import unicode_literals

from django.db import models
from django.core.validators import *

from django.contrib.auth.models import User, Group

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
import base64

class Event(models.Model):
    eventtype = models.CharField(max_length=1000, blank=False)
    timestamp = models.DateTimeField()
    userid = models.CharField(max_length=1000, blank=True)
    requestor = models.GenericIPAddressField(blank=False)

    def __str__(self):
        return str(self.eventtype)


def validate_number(value):
    if 0 >= value >= 6:
        raise ValidationError(
            _('%(value)s is not an number btw 1...5'),
            params={'value': value},
        )

class Breed(models.Model):

    SIZE =(
        ('T', 'Tiny'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=50, blank=False)
    size = models.CharField(max_length=1, choices=SIZE, default='M',)
    friendlyness = models.IntegerField(validators=[validate_number])
    trainability = models.IntegerField(validators=[validate_number])
    sheddinamount = models.IntegerField(validators=[validate_number])
    excerciseneeds = models.IntegerField(validators=[validate_number])

    def __str__(self):
        return str(self.name)

class Dog(models.Model):
    name = models.CharField(max_length=30, blank=False)
    age = models.IntegerField()
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, default=1)
    gender = models.CharField(max_length=6, blank=False)
    color = models.CharField(max_length=10, blank=False)
    favoritefood = models.CharField(max_length=20, blank=False)
    favoritetoy = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return str(self.name)

class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = '__all__'

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'

class EventAdmin(admin.ModelAdmin):
    list_display = ('eventtype', 'timestamp')

class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')

class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'size')

class ApiKey(models.Model):
    owner = models.CharField(max_length=1000, blank=False)
    key = models.CharField(max_length=5000, blank=False)

    def __str__(self):
        return str(self.owner) + str(self.key)

class ApiKeyAdmin(admin.ModelAdmin):
    list_display = ('owner','key')
