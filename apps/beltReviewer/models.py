# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def loginValidation(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        users = self.filter(email = postData['email'])

        if len(users) < 1:
            results['status'] = False
        else:
            if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
                results['user'] = users[0]
            else:
                results['status'] = False
        return results

    def validate(self, postData):
        results = {'status': True, 'errors': []}
        if len(postData['first_name'].strip()) < 3: #spaces are not allowed in name
            results['errors'].append('Your first name is too short!')
            results['status'] = False
        if len(postData['last_name'].strip()) < 3:
            results['errors'].append('Minimum 3 characters!')
            results['status'] = False
        if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            results['errors'].append('Invalid email!')
            results['status'] = False
        if postData['password'] != postData['c_password']:
            results['errors'].append('Passwords must match!')
            results['status'] = False
        if len(postData['password'].strip()) < 5:
            results['errors'].append('Password must contain 5 characters!')
            results['status'] = False
        if len(self.filter(email = postData['email'])) > 0:
            results['errors'].append('User already exists!')
            results['status'] = False
        return results

    def creator(self, postData):
        user = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], alias = postData['alias'], email = postData['email'], password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
        return user

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email =  models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    rate = models.IntegerField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name = 'books')

class Review(models.Model):
    comment = models.TextField()
    book = models.ForeignKey(Book, related_name = 'books')
    writer = models.ForeignKey(User, related_name = 'reviews')
