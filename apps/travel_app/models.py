from django.db import models
import re, bcrypt
from datetime import datetime

class UserManager(models.Manager):
    # Register function
    def register(self, postData):
        valid = {
            "is_valid": True,
            "user": None,
            "errors": {}
        }
        # validations
        if len(postData['name'])<1:
            valid['errors']['name'] = "Name is required!"
        elif len(postData['name'])<2:
            valid['errors']['name'] = "Name must be at least 2 characters!"
       
        if len(postData['username'])<1:
            valid['errors']['username'] = "Username is required!"
        elif len(postData['username'])<2:
            valid['errors']['username'] = "Username must be at least 2 characters!"
        else:
            valid['user'] = User.objects.filter(username=postData['username'])
            if len(valid['user']) > 0:
                valid['errors']['username'] = "Username already exists!"

        if len(postData['password'])<1:
            valid['errors']['password'] = "Password is required!"
        elif len(postData['password'])<8:
            valid['errors']['password'] = "Password must be at least 8 characters!"
        if len(postData['password_confirm'])<1:
            valid['errors']['password_confirm'] = "Password confirm is required!"
        elif postData['password'] != postData['password_confirm']:
            valid['errors']['password_confirm'] = "Passwords must match!"

        # Success if all validations pass
        if len(valid['errors']) == 0:
            valid["user"] = User.objects.create(
                name=postData["name"],
                username=postData["username"],
                password=bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt()).decode()
            )
        else:
            valid["is_valid"] = False
        
        return valid

    # Login function
    def login(self, postData):
        valid= {
            "is_valid": True,
            "user": None,
            "errors": {}
        }
        # validations
        if len(postData['username'])<1:
            valid['errors']['username'] = "Username is required!"
        else:
            valid['user'] = User.objects.filter(username=postData['username'])
            if len(valid['user']) == 0:
                valid['errors']['username'] = "Unknown username"
        
        if len(postData['password'])<1:
            valid['errors']['password'] = "Password is required!"
        elif len(postData['password'])<8:
            valid['errors']['password'] = "Password must be at least 8 characters!"
        
        # Success if all validations pass
        if len(valid['errors']) == 0:
            valid['user'] = valid['user'][0]
            check = bcrypt.checkpw(postData['password'].encode(), valid['user'].password.encode())
            # No matching information
            if not check:
                valid["is_valid"] = False
                valid["errors"]["password"] = "Invalid login information."
        
        return valid
        
class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class TravelManager(models.Manager):
    def add(self, postData, uid):
        errors = []
        # validations
        if len(postData['place']) < 1:
            errors.append('place is required.')

        if len(postData['startdate']) < 1:
            errors.append('Starting date is required')
        if len(postData['enddate']) < 1:
            errors.append('Ending date is required')

        if len(postData['plan']) < 1:
            errors.append('A plan is required')
            
        # Success if all validations pass
        matches = Travel.objects.filter(place=postData['place']).filter(startdate=postData['startdate'])
        if len(matches) > 0:
            errors.append(f"{postData['place']} already exists!")
        if len(errors) == 0:
            return Travel.objects.create(place=postData['place'], startdate=postData['startdate'], enddate=postData['enddate'], plan=postData['plan'], poster_id=uid) #because we added _id, we don't have to pass User object
        else:
            return errors
        
class Travel(models.Model):
    place = models.CharField(max_length=45)
    startdate = models.DateField()
    enddate = models.DateField()
    plan = models.CharField(max_length=255)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="travels")
    joined = models.ManyToManyField(User, related_name="joined")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TravelManager()
