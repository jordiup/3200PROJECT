from django.db import models

# Create your models here.
from django.db.models import CharField


class Person(models.Model):
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    full_name = models.CharField(max_length=49)
    date_added = models.DateTimeField('date added')

    def __str__(self):
        return self.full_name


class Location(models.Model):
    place_name = models.CharField(max_length=64)

    def __str__(self):
        return self.place_name


class PersonLocation(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    date_added = models.DateTimeField('date added')


class Document(models.Model):
    archive_number = models.CharField(max_length=100)
    date_written = models.DateTimeField('date written')
    receiver = models.ForeignKey(PersonLocation, related_name='receiver', on_delete=models.CASCADE)
    sender = models.ForeignKey(PersonLocation, related_name='sender', on_delete=models.CASCADE)
    document_type = models.CharField(max_length=16)
    language = models.CharField(max_length=16)

    def __str__(self):
        return str(self.archive_number)


