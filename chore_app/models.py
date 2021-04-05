from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')

class CustomerManager(models.Manager):
    def customer_validator(self, postData):
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
        if len(postData['street']) < 1:
            errors['street'] = "Error, Please enter a valid street name."
        if len(postData['city']) < 1:
            errors['city'] = "Error, Please enter a valid city name."
        if len(postData['zip']) < 5:
            errors['zip'] = "Error, Please enter a valid zip_code."
        if len(postData['state']) < 2:
            errors['state'] = "Error, Please enter a valid state."

        return errors

    def login_validator(self, postData):
        errors = {}
        customer_check = Customer.objects.filter(email_address=postData['email_address'])
        if not customer_check:
            errors['please_register'] = "Error, Email not registered."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), customer_check[0].password.encode()):
                errors['password_wrong'] = "Error, Email and Password do not match."
        return errors
    

class DriverManager(models.Manager):
    def driver_validator(self, postData):
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
        if len(postData['street']) < 1:
            errors['street'] = "Error, Please enter a valid street name."
        if len(postData['city']) < 1:
            errors['city'] = "Error, Please enter a valid city name."
        if len(postData['zip']) < 5:
            errors['zip'] = "Error, Please enter a valid zip_code."
        if len(postData['state']) < 2:
            errors['state'] = "Error, Please enter a valid state."

        return errors

    def login_validator(self, postData):
        errors = {}
        driver_check = Driver.objects.filter(email_address=postData['email_address'])
        if not driver_check:
            errors['please_register'] = "Error, Email not registered."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), driver_check[0].password.encode()):
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




class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=150)
    phone_number = models.IntegerField()
    likes = models.IntegerField(null=True, blank=True)
    dislikes = models.IntegerField(null=True, blank=True)
    user_lvl = models.IntegerField()
    photo = models.ImageField(null=True, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    state = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = CustomerManager()


class Driver(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=150)
    phone_number = models.IntegerField()
    likes = models.IntegerField(null=True, blank=True)
    dislikes = models.IntegerField(null=True, blank=True)
    user_lvl = models.IntegerField()
    photo = models.ImageField(null=True, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.IntegerField()
    state = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = DriverManager()


class Chore(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField(max_length=80)
    price = models.IntegerField()
    completed = models.BooleanField()
    status = models.IntegerField()
    customer = models.ForeignKey(User, related_name="has_customer", on_delete=models.CASCADE)
    driver = models.ForeignKey(User, related_name="has_driven", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ChoreManager()