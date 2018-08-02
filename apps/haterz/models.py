# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    dob = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Record(models.Model):
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, related_name= "uploads")
    haters = models.ManyToManyField(User, related_name="hated_records")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)