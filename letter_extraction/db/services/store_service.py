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

    for item in range(1, len(input)):
        holder_of_categories = input[item]
        archival_number = holder_of_categories[0][1]
        letter_writtenDate = holder_of_categories[2][1]
        receiver_first_name = holder_of_categories[3][1]
        receiver_location = holder_of_categories[4][1]
        sender_first_name = holder_of_categories[5][1]
        sender_location = holder_of_categories[6][1]    #Probably not the best way to do this
        language_written = holder_of_categories[7][1]
        notes_written = holder_of_categories[8][1]
        spliced_language = ""
        if language_written == 'None':
            spliced_language = ""
        else:
            if len(language_written) == 1:
                spliced_langauge = language_written
            else:
                # print(language_written)
                if(',' in language_written):
                    spliced_language = language_written.split(',')[1].strip()
                elif ('.' in language_written):
                    spliced_language = language_written.split('.')[1].strip()
        receiver_last_name = ''
        sender_last_name = ''
        receiver_full_name = ''.join((receiver_first_name, receiver_last_name))
        sender_full_name= ''.join((sender_first_name, sender_last_name))
        if Person.objects.filter(full_name = receiver_full_name).exists():
            receiver = Person.objects.filter(full_name=receiver_full_name).first()
        else:
            receiver = Person(first_name= receiver_first_name, last_name= receiver_last_name, full_name=receiver_full_name, date_added=timezone.now(), date_modified=timezone.now())
            # print(receiver)
            receiver.save()
        if Person.objects.filter(full_name = sender_full_name).exists():
            sender = Person.objects.filter(full_name =sender_full_name).first()
        else:
            sender = Person(first_name=sender_first_name , last_name=sender_last_name, full_name=sender_full_name, date_added=timezone.now(), date_modified=timezone.now())
            sender.save()
        if Location.objects.filter(place_name=receiver_location).exists():
            location_receiver = Location.objects.filter(place_name=receiver_location).first()
        else:
            location_receiver = Location(place_name= receiver_location, date_added=timezone.now(), date_modified=timezone.now())
            location_receiver.save()
        if Location.objects.filter(place_name=sender_location).exists():
            location_sender = Location.objects.filter(place_name=sender_location).first()
        else:
            location_sender = Location(place_name=sender_location, date_modified=timezone.now(), date_added=timezone.now())
            location_sender.save()


        person_location_receiver = PersonLocation(location=location_receiver, person=receiver)
        person_location_sender = PersonLocation(location=location_sender, person=sender)

        person_location_receiver.save()
        person_location_sender.save()


        documentInstance = Document(archive_number=archival_number, date_written= letter_writtenDate, receiver=person_location_receiver, sender=person_location_sender, document_type='diary',
            language= spliced_language , date_added=timezone.now(), date_modified=timezone.now(), uploaded_by=user, notes = notes_written)
        documentInstance.save()

def addToModel_xlsx(input, user):
    if input == {}:
        return
    holder_of_categories = input[0][0]
    list_of_things = {"archive code": 0 , "addressee" : 0 , "language": 0,  "date": 0, "place":0, "responded by" : 0, "notes": 0 }
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
            if (isinstance(item_holder[item][count][1], float) == False) and ',' in item_holder[item][count][1]:
                archival_number = item_holder[item][count][1].split(',')
            elif item_holder[item][count][1] != "None":
                archival_number = item_holder[item][count][1]
                if '[' in archival_number or  "\\'" in archival_number or ']' in archival_number:
                    newstr = archival_number.replace("[", "").replace("]","").replace("//'", "")
                    archival_number = newstr
            else:
                archival_number = ''

            if list_of_things["addressee"] == 1 and (isinstance(item_holder[item][count+1][1], float) == False):
                if item_holder[item][count+1][1] != "None":
                    receiver_full_name = item_holder[item][count+1][1]
                    if '[' in receiver_full_name or  "\\'" in receiver_full_name or ']' in receiver_full_name:
                        newstr = receiver_full_name.replace("[", "").replace("]","").replace("//'", "")
                        receiver_full_name = newstr
            else:
                receiver_full_name = ''

            if list_of_things["language"] == 1 and (isinstance(item_holder[item][count+2][1], float) == False):
                if item_holder[item][count+2][1] != "None":
                    spliced_language = item_holder[item][count+2][1]
                    if '[' in spliced_language or  "\\'" in spliced_language or ']' in spliced_language:
                        newstr = spliced_language.replace("[", "").replace("]","").replace("//'", "")
                        spliced_language = newstr
            else:
                spliced_language = ''

            if list_of_things["date"] == 1:
                if item_holder[item][count+3][1] != "None" and (isinstance(item_holder[item][count+3][1], float) == False):
                    date_written = item_holder[item][count+3][1]
                    if '[' in date_written or  "\\'" in date_written or ']' in date_written:
                        newstr = date_written.replace("[", "").replace("]","").replace("//'", "")
                        date_written = newstr
                else:
                    date_written = ''

            if list_of_things["place"] == 1:
                if item_holder[item][count+4][1] != "None" and  (isinstance(item_holder[item][count+4][1], float) == False):
                    receiver_location = item_holder[item][count+4][1]
                    if '[' in receiver_location or  "\\'" in receiver_location or ']' in receiver_location:
                        newstr = receiver_location.replace("[", "").replace("]","").replace("//'", "")
                        receiver_location = newstr
                else:
                    receiver_location = ''

            if list_of_things["responded by"] == 1:
                if item_holder[item][count+6][1] != "None" and  (isinstance(item_holder[item][count+6][1], float) == False):
                    sender_full_name = item_holder[item][count+6][1]
                    if '[' in sender_full_name  or  "\\'" in sender_full_name  or ']' in sender_full_name :
                        newstr = sender_full_name .replace("[", "").replace("]","").replace("//'", "")
                        sender_full_name  = newstr
                else:
                    sender_full_name = ''

            if list_of_things["notes"] == 1:
                print(item_holder[item][count+7][1])
                if item_holder[item][count+7][1] != "None" and  (isinstance(item_holder[item][count+7][1], float) == False):
                    notes_one = item_holder[item][count+7][1]
                    if '[' in notes_one  or  "\\'" in notes_one  or ']' in  notes_one :
                        newstr =  notes_one.replace("[", "").replace("]","").replace("//'", "")
                        notes_one  = newstr
                else:
                    notes_one = ''

            if Person.objects.filter(full_name = receiver_full_name).exists():
                receiver = Person.objects.filter(full_name=receiver_full_name).first()
            else:
                receiver = Person(first_name= '', last_name= '', full_name=receiver_full_name, date_added=timezone.now(), date_modified=timezone.now())
                receiver.save()
            if Person.objects.filter(full_name = sender_full_name).exists():
                sender = Person.objects.filter(full_name=sender_full_name).first()
            else:
                sender = Person(first_name= ''  , last_name= '', full_name= sender_full_name , date_added=timezone.now(), date_modified=timezone.now())
                sender.save()
            if Location.objects.filter(place_name=receiver_location).exists():
                location_receiver = Location.objects.filter(place_name=receiver_location).first()
            else:
                location_receiver = Location(place_name= receiver_location, date_added=timezone.now(), date_modified=timezone.now())
                location_receiver.save()

            if Location.objects.filter(place_name='N/A').exists():
                location_sender = Location.objects.filter(place_name='N/A').first()
            else:
                location_sender = Location(place_name= 'N/A', date_modified=timezone.now(), date_added=timezone.now())
                location_sender.save()

            print("WHAT")

            person_location_receiver = PersonLocation(location=location_receiver, person=receiver)
            person_location_sender = PersonLocation(location=location_sender, person=sender)

            person_location_receiver.save()
            person_location_sender.save()
            print("WHAT")
            
            documentInstance = Document(archive_number=archival_number, date_written= date_written, receiver=person_location_receiver, sender=person_location_sender, document_type='diary',
                language= spliced_language , date_added=timezone.now(), date_modified=timezone.now(), uploaded_by=user, notes = notes_one)
            documentInstance.save()



def deleteReplicates(input):
    for item in input:
        Document.objects.filter(archive_number__iexact=item).delete()
