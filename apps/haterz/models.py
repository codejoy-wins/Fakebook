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

class Post(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, related_name="posts")
    liked_by = models.ManyToManyField(User, related_name="liked_posts")
    location = models.ForeignKey(User, related_name="posts_for_me", null = True) 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, related_name="comments")
    author = models.ForeignKey(User, related_name="written_comments")
    liked_by = models.ManyToManyField(User, related_name="liked_comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)