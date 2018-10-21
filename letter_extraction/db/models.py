from django.db import models
from django import forms
from django.contrib.auth.models import User
# Create your models here.
from django.db.models import CharField


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    date_added = models.DateTimeField('date added')
    date_modified = models.DateTimeField('date modified')

    def __str__(self):
        return self.full_name


class Location(models.Model):
    place_name = models.CharField(max_length=128, default = "Unknown")
    date_added = models.DateTimeField('date added')
    date_modified = models.DateTimeField('date modified')

    def __str__(self):
        return str(self.place_name)


class PersonLocation(models.Model): # this is just a table to denote a many-to-many relationship between Persons and Locations
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Document(models.Model):
    archive_number = models.CharField(max_length=300)
    date_written = models.CharField(max_length=150)
    receiver = models.ForeignKey(PersonLocation, related_name='receiver', on_delete=models.CASCADE)
    sender = models.ForeignKey(PersonLocation, related_name='sender', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=16)
    language = models.CharField(max_length=64)
    date_added = models.DateTimeField('date added', null=True, default=None)
    date_modified = models.DateTimeField('date modified')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.CharField(max_length = 1500)

    def __str__(self):
        return str(self.archive_number)

class Privileges(models.Model):

    class Meta:

        managed = False

        permissions = (
            ('can_upload', 'User has the ability to upload a document.'),
            ('can_search', 'User has the ability to search for documents.'),
            ('can_edit', 'User has the ability to edit document data.'),
        )

# feel free to add more fields. To add these to the database, use python(3) manage.py makemigrations; and then python(3) manage.py migrate
