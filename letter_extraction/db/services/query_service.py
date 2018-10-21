from db.models import Person, PersonLocation, Document, Location
from django.db.models import Q
from db.services.entities.query_entity import DocumentEntity

date_added = "date_added"
date_modified = "date_modified"
receiver_id ="receiver_id"
sender_id = "sender_id"
id = "id"

def analyze_query_request(search_type, query_value, isBrowse, user):
    results = []
    if isBrowse is False:
        if search_type == 'document':
            documents = process_archive_number(query_value)
        if search_type == 'person':
            search_value = query_value.split('::')
            if len(search_value) == 1:
                search_filter = 'both'
            else:
                search_filter = search_value[1]
            documents = process_person(search_value[0], search_filter)
        if search_type == 'location':
            search_value = query_value.split('::')
            if len(search_value) == 1:
                search_filter = 'both'
            else:
                search_filter = search_value[1]
            documents = process_location(search_value[0], search_filter)
        if search_type == 'date':
            documents = process_date(query_value)
        if search_type == 'document_type':
            documents = process_document_type(query_value)
        if search_type == 'language':
            documents = process_language(query_value)
        return_document_model(results, documents, user)
    else:
        documents = []
        documents.extend(Document.objects.order_by('?')[:5])
        return_document_model(results, documents, user)
    return results

def process_archive_number(query_value):
    if query_value[0] == '\"' and query_value[len(query_value)-1] == '\"':
        search_val = query_value[1:len(query_value)-1]
        documents = Document.objects.filter(archive_number__iexact=search_val)
    else: 
        documents = Document.objects.filter(archive_number__icontains=query_value)
    return documents

def process_person(query_value, search_filter):
    authors = Person.objects.filter(Q(first_name__iexact=query_value) | Q(last_name__iexact=query_value)
                                | Q(full_name__iexact=query_value))
    person_locations = []
    for author in authors:
        person_locations.extend(PersonLocation.objects.filter(person=author))
    documents = []
    for pl in person_locations:
        if search_filter == 'author':
            documents.extend(Document.objects.filter(sender=pl))
        elif search_filter == 'receiver':
            documents.extend(Document.objects.filter(receiver=pl))
        elif search_filter == 'both':
            documents.extend(Document.objects.filter(Q(receiver=pl) | Q(sender=pl)))
        else:
            return
    return documents

def process_location(query_value, search_filter):
    objects = Location.objects.all()
    locations = objects.filter(place_name__iexact=query_value)
    person_locations = []
    for location in locations:
        person_locations.extend(PersonLocation.objects.filter(location=location))
    documents = []
    for pl in person_locations:
        if search_filter == 'author':
            documents.extend(Document.objects.filter(sender=pl))
        elif search_filter == 'receiver':
            documents.extend(Document.objects.filter(receiver=pl))
        elif search_filter == 'both':
            documents.extend(Document.objects.filter(Q(receiver=pl) | Q(sender=pl)))
        else:
            return
    return documents


def process_date(query_value):
    documents = []
    objects = Document.objects.all()
    split_dates = query_value.split("-")
    if len(split_dates) == 2:
        try:
            int(split_dates[0])
            int(split_dates[1])
        except ValueError:
            return
        for obj in objects:
            if split_dates[0] >= split_dates[1]:
                return
            date_written = obj.date_written
            numeric_date = ''.join(c for c in date_written if c.isdigit())[-4:]
            if numeric_date == '' or numeric_date is None:
                continue
            try:
                int(numeric_date)
            except ValueError:
                continue
            if numeric_date >= split_dates[0] and numeric_date <= split_dates[1]:
                documents.append(obj)
    elif len(split_dates) == 1:
        try:
            int(query_value)
        except ValueError:
            return
        for obj in objects:
            date_written = obj.date_written
            numeric_date = ''.join(c for c in date_written if c.isdigit())[-4:]
            if numeric_date == '' or numeric_date is None:
                continue
            try:
                int(numeric_date)
            except ValueError:
                continue
            if numeric_date == split_dates[0]:
                documents.append(obj)
    else: 
        return
    return documents

def process_document_type(query_value):
    documents = []
    documents.extend(Document.objects.filter(document_type__iexact=query_value))
    return documents

def process_language(query_value):
    documents = []
    documents.extend(Document.objects.filter(language__iexact=query_value))
    return documents


def return_document_model(results, documents, user):
    for d in documents:
        place_written = d.sender.location.place_name
        sender_name = d.sender.person.full_name
        receiver_name = d.receiver.person.full_name
        place_received = d.receiver.location.place_name
        # if d.uploaded_by != user.id:
        #     continue
        result = [d.archive_number, d.date_written, d.document_type, d.language, place_written, sender_name, place_received, receiver_name, d.pk]
        results.append(result)

# def get_pks(values):
#     keys = []
#     for v in values:
#         key = v[0]
#         keys.append(key)
#         v.remove(key)
#     return keys
