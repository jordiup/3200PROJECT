from db.models import *
from django.db.models import Q


def analyze_query_request(search_type, query_value):
    results = []
    if search_type == 'document':
        process_archive_number(results, query_value)
    if search_type == 'author':
        process_author(results, query_value)
    if search_type == 'location':
        process_location(results, query_value)
    if search_type == 'date':
        process_date(results, query_value)
    return results

def process_archive_number(results, query_value):
    documents = Document.objects.filter(archive_number__iexact=query_value)
    results.extend([x for x in documents])

def process_author(results, query_value):
    authors = Person.objects.filter(Q(first_name__iexact=query_value) | Q(last_name__iexact=query_value)
                                | Q(full_name__iexact=query_value))
    person_locations = []
    for author in authors:
        person_locations.extend(PersonLocation.objects.filter(person=author))
    documents = []
    for pl in person_locations:
        documents.extend(Document.objects.filter(sender=pl))
    results.extend([x for x in documents])

def process_location(results, query_value):
    objects = Location.objects.all()
    locations = objects.filter(place_name__iexact=query_value)
    person_locations = []
    for location in locations:
        person_locations.extend(PersonLocation.objects.filter(location=location))
    documents = []
    for pl in person_locations:
        documents.extend(Document.objects.filter(Q(sender=pl) | Q(receiver=pl)))
    results.extend([x for x in documents])


def process_date(results, query_value):
    objects = Document.objects.all()
    documents = []
    try:
        int(query_value)
    except:
        return
    documents.extend(objects.filter(date_written__year=query_value))
    results.extend([x for x in documents])