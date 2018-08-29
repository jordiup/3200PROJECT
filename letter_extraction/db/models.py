from django.db import models
from django import forms
# Create your models here.
from django.db.models import CharField


class Person(models.Model):
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    full_name = models.CharField(max_length=49)
    date_added = models.DateTimeField('date added')
    date_modified = models.DateTimeField('date modified')

    def __str__(self):
        return self.full_name



class Location(models.Model):
    place_name = models.CharField(max_length=64)
    date_added = models.DateTimeField('date added')
    date_modified = models.DateTimeField('date modified')

    def __str__(self):
        return str(self.place_name)


class PersonLocation(models.Model): # this is just a table to denote a many-to-many relationship between Persons and Locations
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Document(models.Model):
    archive_number = models.CharField(max_length=100)
    date_written = models.DateTimeField('date written')
    receiver = models.ForeignKey(PersonLocation, related_name='receiver', on_delete=models.CASCADE)
    sender = models.ForeignKey(PersonLocation, related_name='sender', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=16)
    language = models.CharField(max_length=16)
    date_added = models.DateTimeField('date added', null=True, default=None)
    date_modified = models.DateTimeField('date modified')

    def __str__(self):
        return str(self.archive_number)

class UploadFileForm(forms.Form):
    file = forms.FileField()
    
class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64) # want to hash as 64 character string. CURRENTLY STORED AS PLAINTEXT !!!!!
    email = models.EmailField(max_length=100) # in case they want to add registration
    active = models.BooleanField('active', default=False) # is the user active
    permission_level = models.IntegerField('permission', default=1) # we want to make a list of permissions, 1 lowest level, 2 next highest, etc. Devs are 0
    date_joined = models.DateTimeField('date joined')
    hello = models.CharField(max_length = 32)

    def __str__(self):
        return self.username

def metadata_extraction():
    members = [attr for attr in dir(User) if not callable(getattr(User, attr)) and not attr.startswith("__") and not attr.startswith("_")]
    previous = ""
    comparison_string = ""
    for items in members[:]:
        if items == 'id' or items == 'objects' or items == 'pk' or items == 'receiver' or items == 'sender' :
            members.remove(items)
    for before in members:
        previous = members.index(before)
        if(previous != 0):
            comparison_string = members[previous-1] + "_id"
        if comparison_string == before:
            members.remove(before)
    dictionary_holder = {k: 0 for k in members}
    return dictionary_holder




# feel free to add more fields. To add these to the database, use python(3) manage.py makemigrations; and then python(3) manage.py migrate
