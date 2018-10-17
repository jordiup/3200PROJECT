from django import forms
from .models import *
from django.db.models import Q

class documentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = (#'archive_number', 
        'date_written', 'document_type', 'language')

    def save_form(self):
        if self.is_valid():
            document = self.save()
            document.save()
            return True


class personLocationForm(forms.ModelForm):
    class Meta:
        model = PersonLocation
        fields = '__all__'

    def save_form(self):
        if self.is_valid():
            person_location = self.save()
            person_location.save()
            return True


class personForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'full_name']

    def save_form(self):
        if self.is_valid():
            person = self.save()
            person.save()
            return True

class locationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['place_name']

    def save_form(self):
        if self.is_valid():
            location = self.save()
            location.save()
            return True


def get_forms_by_document(request, id):
    forms = []
    document = Document.objects.filter(pk=id).first()
    sender_pl = PersonLocation.objects.filter(pk=document.sender.pk).first()
    receiver_pl = PersonLocation.objects.filter(pk=document.sender.pk).first()
    sender_person = Person.objects.filter(pk=sender_pl.person.pk).first()
    sender_location = Location.objects.filter(pk=sender_pl.location.pk).first()
    receiver_person = Person.objects.filter(pk=receiver_pl.person.pk).first()
    receiver_location = Location.objects.filter(pk=receiver_pl.location.pk).first()

    document_form_post = documentForm(request.POST, instance=document)
    forms.append(document_form_post)
    document_form = documentForm(instance=document)
    forms.append(document_form)
    sender_form = personForm(instance=sender_person)
    forms.append(sender_form)
    receiver_form = personForm(instance=receiver_person)
    forms.append(receiver_form)
    sender_location_form = locationForm(instance=sender_location)
    forms.append(sender_location_form)
    receiver_location_form = locationForm(instance=receiver_location)
    forms.append(receiver_location_form)

    return forms



