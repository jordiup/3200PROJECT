import os
import re
import nltk
import math

from django.utils import timezone
from db.models import *

#Gathers which data is from which part of the results array
def addToModel(input, user):
    if input == {}:
        return
    holder_of_categories = input[0]
    archival_number = holder_of_categories[0][1]
    language_written = holder_of_categories[5][1]
    letter_writtenDate = holder_of_categories[2][1]
    sender_info = re.findall(r'[^,;]+', holder_of_categories[3][1])
    receiver_info = re.findall(r'[^,;]+', holder_of_categories[4][1])
    spliced_language = language_written.split(',')[1].strip()
    receiver_first_name = receiver_info[0].strip()
    receiver_last_name = ''
    sender_first_name = sender_info[0].strip()
    sender_last_name = ''
    receiver_full_name = ''.join((receiver_first_name, receiver_last_name))
    sender_full_name= ''.join((sender_first_name, sender_last_name))
    receiver = Person(first_name= receiver_first_name, last_name= receiver_last_name, full_name=receiver_full_name, date_added=timezone.now(), date_modified=timezone.now())
    sender = Person(first_name=sender_first_name , last_name=sender_last_name, full_name=sender_full_name, date_added=timezone.now(), date_modified=timezone.now())
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
        language= spliced_language , date_added=timezone.now(), date_modified=timezone.now(), uploaded_by=user)
    documentInstance.save()

def addToModel_xlsx(input, user):
    if input == {}:
        return
    holder_of_categories = input[0][0]
    list_of_things = {"archive code": 0 , "addressee" : 0 , "language": 0,  "date": 0, "place":0}
    count = 0
    i = 0

    trigger_one = False
    container = list(list_of_things)
    while i != len(list_of_things): # checking excel file for headings similiar to the ones in list_of_things
        holder = container[i]
        i = i + 1
        for item in holder_of_categories:
            if(isinstance(item[1], str) == False):
                if(math.isnan(item[1]) == True) and trigger_one == False:
                    count = count + 1
            string_holder = str(item[1])
            string_holder = string_holder.lower()
            if string_holder == holder:
                list_of_things[holder] = 1
        trigger_one = True
    item_holder = input[0]

    for a in range(0, len(input)):
        item_holder = input[a]
        for item in range(1, len(item_holder)):

            if list_of_things["archive code"] == 1 and (isinstance(item_holder[item][count][1], float) == False):
                archival_number = item_holder[item][count][1].split(',')
            else:
                archival_number = ''
            if list_of_things["addressee"] == 1 and (isinstance(item_holder[item][count+1][1], float) == False):
                if item_holder[item][count+1][1]:
                    receiver_full_name = item_holder[item][count+1][1].split(',')
            else:
                receiver_full_name = ''
            if list_of_things["language"] == 1 and (isinstance(item_holder[item][count+2][1], float) == False):
                if item_holder[item][count+2][1]:
                    spliced_language = item_holder[item][count+2][1].split(',')
            else:
                spliced_language = ''
            if list_of_things["date"] == 1:
                if item_holder[item][count+3][1] and (isinstance(item_holder[item][count+3][1], float) == False):
                    date_written = item_holder[item][count+3][1].split(',')
                else:
                    date_written = ''
            if list_of_things["place"] == 1:
                if item_holder[item][count+4][1] and  (isinstance(item_holder[item][count+4][1], float) == False):
                    receiver_location = item_holder[item][count+4][1].split(',')
                else:
                    receiver_location = ''

            receiver = Person(first_name= '', last_name= '', full_name= receiver_full_name, date_added=timezone.now(), date_modified=timezone.now())
            sender = Person(first_name= ''  , last_name= '', full_name= 'N/A', date_added=timezone.now(), date_modified=timezone.now())
            location_receiver = Location(place_name=receiver_location, date_added=timezone.now(), date_modified=timezone.now())
            location_sender = Location(place_name= 'N/A', date_modified=timezone.now(), date_added=timezone.now())

            receiver.save()
            sender.save()
            location_receiver.save()
            location_sender.save()

            person_location_receiver = PersonLocation(location=location_receiver, person=receiver)
            person_location_sender = PersonLocation(location=location_sender, person=sender)

            person_location_receiver.save()
            person_location_sender.save()

            documentInstance = Document(archive_number=archival_number, date_written= date_written, receiver=person_location_receiver, sender=person_location_sender, document_type='diary',
                language= spliced_language , date_added=timezone.now(), date_modified=timezone.now(), uploaded_by=user)
            documentInstance.save()
def string_split(input_dictionary, a, b):
    count = 0
    switch = 0
    for item in range(0, len(input_dictionary)):
        if (item%5 == 0 and item>=5):
            switch = 0
        holder = list(input_dictionary[item].keys())
        holder_b = list(input_dictionary[item].values())
        switch = switch + 0.5
        for i in range(0, len(input_dictionary[item].keys())):
            if switch == 2.5:
                a[ holder[i]] = count
                b[holder_b[i]] = count
                count = count + 1
                continue
            if (switch == 0.5 or switch == 1):
                a[''.join(("sender" , "_" , holder[i]))] = count
                b[holder_b[i]] = count
                count = count + 1
            else:
                a[''.join(("receiver" , "_" , holder[i]))] = count
                b[holder_b[i]] = count
                count = count + 1
