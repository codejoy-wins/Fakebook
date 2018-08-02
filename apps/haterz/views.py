# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import datetime
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
    return render(request, "haterz/index.html")

def main(request):
    print 'main method'
    if not 'user_id' in request.session:
        messages.error(request, "must be logged on first")
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        "jay": "silent bob",
        "users2": User.objects.exclude(id=user.id),
        "records": Record.objects.exclude(haters = user),
        "hated": user.hated_records.all(),
        "user": user,
        "users": User.objects.all()
    }
    return render(request, "haterz/main.html", context)

def register(request):
    error = False
    if request.POST['password'] != request.POST['confirm_password']:
        error = True
        messages.error(request, "Passwords must match")
    if len(request.POST['first_name']) < 2:
        error = True
        messages.error(request, "First name must be longer than 2 characters")
    if len(request.POST['last_name']) < 2:
        error = True
        messages.error(request, "Last name must be longer than 2 characters")
    if len(request.POST['password']) < 8:
        error = True
        messages.error(request, "Password must be 8 or more characters")
    if len(User.objects.filter(email = request.POST['email'])) > 0:
        error = True
        messages.error(request, "Email already taken")
    if not EMAIL_REGEX.match(request.POST['email']):
        error = True
        messages.error(request, "Email in an invalid format")
    if len(request.POST['dob']) == 0:
        error = True
        messages.error(request, "Must provide date of birth")
    else:
        my_bday = datetime.strptime(request.POST['dob'], "%Y-%m-%d")
        if my_bday > datetime.today():
            error = True
            messages.error(request,"Time Traveler")
    if error:
        return redirect('/')
    print "Made it through all validations!"
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed_pw, dob = my_bday)
    request.session['user_id'] = user.id
    # validated data, encrypted password, converted datetime string to datetime time, created user, added user.id to session
    print user.id
    print request.session['user_id']
    # redirect to main page and have context retrieve the user from database who matches session
    return redirect('/main')

def login(request):
    if not request.POST:
        print "wtf"
        return redirect('/')
    if len(request.POST['email']) == 0:
        messages.error(request,'Must have email to log on')
    if len(request.POST['password']) ==0:
        messages.error(request,'Must enter password to log on')
    print "logging on"
    try:
        print "trying"
        user = User.objects.get(email = request.POST['email'])
        # check pw
        request.session['user_id'] = user.id
    except:
        messages.error(request, "Invalid Email or Password ")
        return redirect('/')
    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request,"Email or Password Invalid")
        return redirect('/')
    if user.email != request.POST['email']:
        messages.error(request,"Email or Password Invalid")
        return redirect('/')

    return redirect('/main')

def add(request):
    if not "user_id" in request.session:
        messages.error(request,"stop it")
        return redirect('/')
    print "adding"
    print request.POST
    # validate add record form data and create record with user in session as uploader
    error = False
    if len(request.POST['artist'])==0:
        error = True
        messages.error(request, "cmon dude")
    if len(request.POST['album'])==0:
        error = True
        messages.error(request, "cmon dude")
    if len(request.POST['label'])==0:
        error = True
        messages.error(request, "cmon dude")
    if error:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    Record.objects.create(artist=request.POST['artist'], album=request.POST['album'], label = request.POST['label'], uploader = user)
    return redirect('/main')

def logout(request):
    request.session.clear()
    return redirect('/')

def destroy(request, record_id):
    if not 'user_id' in request.session:
        messages.error(request, "knock it off")
        return redirect ('/')
    print "destroying"
    print record_id
    Record.objects.get(id=record_id).delete()
    return redirect ('/main')


# def update where we prepopulate the form

def edit(request, record_id):
    if not 'user_id' in request.session:
        messages.error(request, "knock it off")
        return redirect ('/')
    print "editing"
    print record_id
    record = Record.objects.get(id=record_id)
    print record.artist
    context = {
        "jay": "silent bob",
        "record": record,
    }
    return render (request, 'haterz/edit.html', context)

# use many to many to hate records

def hate(request, record_id):
    if not 'user_id' in request.session:
        messages.error(request, "knock it off")
        return redirect ('/')
    print "hating"
    print record_id
    record = Record.objects.get(id=record_id)
    user = User.objects.get(id=request.session['user_id'])
    #error
    user.hated_records.add(record)
    return redirect ('/main')

def update(request, record_id):
    print "updating"
    print "record_id"
    record = Record.objects.get(id=record_id)
    record.artist = request.POST['artist']
    record.album = request.POST['album']
    record.label = request.POST['label']
    record.save()
    return redirect('/main')

def wall(request, wall_id):
    main_user = User.objects.get(id=request.session['user_id'])
    print "walling"
    print "wall_id"
    print wall_id
    user = User.objects.get(id = wall_id)
    print user
    print user.first_name
    try:
        x = Post.objects.all()
    except:
        x = ['linkin', 'park']
    # location = 
    context = {
        "main_user": main_user,
        "user": user,
        "posts": x,
        "my_posts": Post.objects.filter(location=user),
        "comments": Comment.objects.all(),
        # likers: 
        #p = Post.objects.get(id=8)
        #p.liked_by.all().count()
        #max = User.objects.get(id=4)
        #max.liked_posts.all()
    }
    return render(request, "haterz/wall.html", context)

def post(request, wall_id):
    loc = User.objects.get(id=wall_id)
    # print "posting"
    # print request.POST['content']
    # print "on"
    print wall_id
    user = User.objects.get(id=request.session['user_id'])
    # print 'from'
    # print user.id
    post = Post.objects.create(content=request.POST['content'], author = user, location = loc)
    # print post.author.first_name
    # print post.location.first_name

    return redirect('/wall/'+ wall_id)

def like(request, post_id):
    post = Post.objects.get(id=post_id)
    wall = post.location
    user = User.objects.get(id=request.session['user_id'])
    print post
    print wall
    print "liking"
    print post_id
    post.liked_by.add(user)
    print "added liked by"
    x = str(wall.id)
    # work on concatening strings, dude.
    return redirect('/wall/' + x)
    # redirect to /main/wall_id where wall_id = post.location.id

def comment(request, post_id):
    post = Post.objects.get(id=post_id)
    wall = post.location
    author = User.objects.get(id=request.session['user_id'])
    print post.author.first_name
    print wall.first_name
    print "commenting"
    print post_id
    Comment.objects.create(content=request.POST['content'], post = post, author = author)
    x = str(wall.id)
    return redirect('/wall/' + x)

def custom(request):
    print "customizing"
    return redirect('/main')

def odell(request):
    return HttpResponse("odell catches everything")
