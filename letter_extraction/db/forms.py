from django import forms
from .models import *

class documentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['archive_number', 'date_written', 'document_type', 'language']

    def save_form(self):
        if self.is_valid():
            document = self.save()
            document.save()


class personLocationForm(forms.ModelForm):
    class Meta:
        model = PersonLocation
        fields = '__all__'


class personForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'full_name']

class locationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['place_name']
