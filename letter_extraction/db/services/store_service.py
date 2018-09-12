import os
import re
import nltk

from django.utils import timezone
from db.models import *

#Gathers which data is from which part of the results array
def addToModel(input):
    if input == {}: 
        return
    holder_of_categories = input[1]
    archival_number = holder_of_categories[0][1]
    language_written = holder_of_categories[5][1]
    letter_writtenDate = holder_of_categories[2][1]
    receiver_info = re.findall(r'[^,;]+', holder_of_categories[3][1])
    sender_info = re.findall(r'[^,;]+', holder_of_categories[4][1])
    spliced_language = language_written.split(',')[1].strip()
    receiver = Person(first_name=receiver_info[0].strip(), last_name='', full_name=receiver_info[0].strip(), date_added=timezone.now(), date_modified=timezone.now())
    sender = Person(first_name=sender_info[0].strip(), last_name='', full_name=sender_info[0].strip(), date_added=timezone.now(), date_modified=timezone.now())
    location_receiver = Location(place_name=receiver_info[1].strip(), date_added=timezone.now(), date_modified=timezone.now())
    location_sender = Location(place_name=sender_info[1].strip(), date_modified=timezone.now(), date_added=timezone.now())

    receiver.save()
    sender.save()
    location_receiver.save()
    location_sender.save()

    person_location_receiver = PersonLocation(location=location_receiver, person=receiver)
    person_location_sender = PersonLocation(location=location_sender, person=sender)

    person_location_receiver.save()
    person_location_sender.save()


    documentInstance = Document(archive_number=archival_number, date_written= letter_writtenDate, receiver=person_location_receiver, sender=person_location_sender, document_type='diary',
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
