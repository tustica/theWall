from django.db import models
import re

from django.db.models.deletion import CASCADE
import bcrypt
from datetime import datetime, timedelta, tzinfo, timezone


#User Manager for validating the registration and login
class UserManager(models.Manager):
    def registration_validator(request, postData):
        errors = {}
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex, postData['email'])):
            errors['email'] = "Invalid email"
        user = User.objects.filter(email=postData['email'])
        if user:
            errors['email'] = "Email already in use"
        else:
            print('this is a new user')
        if len(postData['first_name'])<2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name'])<2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if len(postData['password'])<8:
            errors['password'] = "Password must be longer than 8 characters"
        if postData['password']!= postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match"
        if postData['birthday'] > str(datetime.now() - timedelta(days=3*365)):
            errors['birthday'] = "This website is COPPA compliant?"
            
        return errors
    


# User Model

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

#Posts Model

class Post(models.Model):
    post_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE, default=None, null=True)

#comments Model

class Comment(models.Model):
    comment_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=CASCADE, default=None, null=True)
    user = models.ForeignKey(User, related_name="commenter", on_delete=models.CASCADE, default=None, null=True)