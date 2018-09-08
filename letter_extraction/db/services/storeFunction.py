
import os
import re
import nltk

from django.utils import timezone
from db.models import *
def addToModel(input):
    for i in range(0, len(input-1)):
        holder_of_categories = input[0]
        receiver_location = holder_of_categories[3][1]  #Gathers which data is from which part of the results array
        sender_location = holder_of_categories[4][1]
        archival_number = holder_of_categories[0][1]
        language_written = holder_of_categories[5][1]
        letter_writtenDate = holder_of_categories[2][1]
        spliced_language = ""
        for character, index in enumerate(language_written):
            if character == '':
                spliced_language = language_written[index:len(language_written-1)]  #Splicing the language to get rid of the correspondence part
        combined_location = ''.join((receiver_location, " ", sender_location))
        personInstance = Person(first_name='Unknown', last_name='Unknown', full_name='Test Writer', date_added=timezone.now(), date_modified=timezone.now())
        locationInstance = Location(place_name_receiver=receiver_location, place_name_sender=sender_location , place_name_both=combined_location , date_modified=timezone.now(), date_added=timezone.now())

    personInstance.save()
    locationInstance.save()

    personLocaton = PersonLocation(location = locationInstance, person = personInstance)

    personLocaton.save()

    documentInstance = Document(archive_number=archival_number, date_written= letter_writtenDate, receiver=personLocaton, sender=personLocaton, document_type='diary',
        language= spliced_language , date_added=timezone.now(), date_modified=timezone.now())
    documentInstance.save()
