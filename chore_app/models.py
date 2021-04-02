from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        email_check = User.objects.filter(email_address=postData['email_address'])
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Error, First Name must be longer than 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Error, Last Name must be longer than 2 characters."
        if len(postData['password']) < 8:
            errors['password'] = "Error Password must be longer than 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['password_match'] = "Error, your Passwords must match."
        if len(postData['email_address']) < 5:
            errors['email_short'] = "Error, Email must be longer than 4 characters."
        elif not EMAIL_REGEX.match(postData['email_address']):
            errors['email_valid'] = "Error, Please enter a valid email."
        elif email_check:
            errors['email_in_use'] = "Error, Email Address is already registered."
        return errors

    def login_validator(self, postData):
        errors = {}
        user_check = User.objects.filter(email_address=postData['email_address'])
        if not user_check:
            errors['please_register'] = "Error, Email not registered."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), user_check[0].password.encode()):
                errors['password_wrong'] = "Error, Email and Password do not match."
        return errors
    

class ChoreManager(models.Manager):

    def chore_validator(self, postData):
        errors = {}
        if len(postData['name']) < 5:
            errors['name'] = "Error, Name must be at least 5 characters."
        if len(postData['description']) < 10:
            errors['description'] = "Error, Description must be at least 10 characters."
        if len(postData['price']) < 1:
            errors['price'] = "Error, you must enter a price."
        return errors

class AddressManager(models.Manager):
    def address_validator(self, postData):
        if len(postData['street']) < 1:
            errors['street'] = "Error, Please enter a valid street name."
        if len(postData['city']) < 1:
            errors['city'] = "Error, Please enter a valid city name."
        if len(postData['zip']) < 5:
            errors['zip'] = "Error, Please enter a valid zip_code."
        if len(postData['state']) < 2:
            errors['state'] = "Error, Please enter a valid state."
            return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=150)
    phone_number = models.IntegerField()
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    user_lvl = models.IntegerField()
    photo = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = UserManager()


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    state = models.CharField(max_length=2)
    user_address = models.ForeignKey(User, related_name="has_address", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AddressManager()

class Chore(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey(Address, related_name="has_location", on_delete=models.CASCADE)
    deliver_to = models.ForeignKey(Address, related_name="has_deliver_to", on_delete=models.CASCADE)
    due_date = models.DateField(max_length=80)
    price = models.IntegerField()
    completed = models.BooleanField()
    status = models.IntegerField()
    lister = models.ForeignKey(User, related_name="has_listed", on_delete=models.CASCADE)
    worker = models.ForeignKey(User, related_name="has_worked", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ChoreManager()

