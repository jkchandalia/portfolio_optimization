from django.db import models
import re


# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        first_name = postData['first_name']
        last_name = postData['last_name']
        if not((len(first_name) >2 ) & str.isalpha(first_name)):
            errors["first_name"] = "First name should be all alphabetical and have at least 2 characters"
        if not(len(last_name) > 2  & str.isalpha(last_name)):
            errors["last_name"] = "Last name should be all alphabetical and have at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Email address is invalid!")
            
        if len(postData['password'])<8:
            errors["password"] = "Password must be at least 8 characters long"
        if postData['password']!=postData['password_confirm']:
            errors["password_confirm"] = "Password and confirmation do not match"

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
