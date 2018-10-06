from db.models import Person, PersonLocation, Document, Location
from django.db.models import Q
from db.services.entities.query_entity import DocumentEntity

date_added = "date_added"
date_modified = "date_modified"
receiver_id ="receiver_id"
sender_id = "sender_id"
id = "id"

def analyze_query_request(search_type, query_value):
    results = []
    if search_type == 'document':
        documents = process_archive_number(query_value)
    if search_type == 'author':
        documents = process_author(query_value)
    if search_type == 'location':
        documents = process_location(query_value)
    if search_type == 'date':
        documents = process_date(query_value)
    return_document_model(results, documents)
    return results

def process_archive_number(query_value):
    documents = Document.objects.filter(archive_number__icontains=query_value)
    return documents

def process_author(query_value):
    count = 0
    authors = Person.objects.filter(Q(first_name__iexact=query_value) | Q(last_name__iexact=query_value)
                                | Q(full_name__iexact=query_value))
    person_locations = []
    for author in authors:
        person_locations.extend(PersonLocation.objects.filter(person=author))
    documents = []
    for pl in person_locations:
        documents.extend(Document.objects.filter(sender=pl))
    return documents

def process_location(query_value):
    objects = Location.objects.all()
    locations = objects.filter(place_name__iexact=query_value)
    person_locations = []
    for location in locations:
        person_locations.extend(PersonLocation.objects.filter(location=location))
    documents = []
    for pl in person_locations:
        documents.extend(Document.objects.filter(Q(sender=pl) | Q(receiver=pl)))
    return documents

def process_date(query_value):
    objects = Document.objects.all()
    documents = []
    try:
        int(query_value)
    except ValueError:
        return
    for oj in objects:
        date_written = oj.date_written.split()
        if query_value in date_written:
            documents.append(oj)
    return documents

def return_document_model(results, documents):
    for d in documents:
        place_written = d.sender.location.place_name
        sender_name = d.sender.person.full_name
        receiver_name = d.receiver.person.full_name
        result = [d.archive_number, d.date_written, d.document_type, d.language, place_written, sender_name, receiver_name]
        results.append(result)
