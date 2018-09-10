
import os
import re
import nltk

from django.utils import timezone
from db.models import *
def addToModel(input):
    holder_of_categories = input[0]
    receiver_location = holder_of_categories[3][1]  #Gathers which data is from which part of the results array
    sender_location = holder_of_categories[4][1]
    archival_number = holder_of_categories[0][1]
    language_written = holder_of_categories[5][1]
    letter_writtenDate = holder_of_categories[2][1]
    spliced_language = ""
    index = 0
    for character in language_written:
        index = index + 1
        if character == ' ':
            spliced_language = language_written[index:(len(language_written))]
            break #Splicing the language to get rid of the correspondence part
    index = 0
    combined_location = ''.join((receiver_location, " ", sender_location))
    personInstance = Person(first_name='Test', last_name='Writer', full_name='Test Writer', date_added=timezone.now(), date_modified=timezone.now())
    locationInstance = Location(place_name_receiver=receiver_location, place_name_sender=sender_location , place_name_both=combined_location , date_modified=timezone.now(), date_added=timezone.now())

    personInstance.save()
    locationInstance.save()

    personLocaton = PersonLocation(location = locationInstance, person = personInstance)

    personLocaton.save()

    documentInstance = Document(archive_number=archival_number, date_written= letter_writtenDate, receiver=personLocaton, sender=personLocaton, document_type='diary',
        language= spliced_language , date_added=timezone.now(), date_modified=timezone.now())
    documentInstance.save()

def string_split(input_dictionary, a, b):
    count = 0
    for item in range(0, len(input_dictionary)):
        holder = list(input_dictionary[item].keys())
        holder_b = list(input_dictionary[item].values())
        for i in range(0, len(input_dictionary[item].keys())):
            a[holder[i]] = count
            b[holder_b[i]] = count
            count = count + 1
