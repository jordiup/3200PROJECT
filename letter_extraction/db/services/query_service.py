from db.models import *
from django.db.models import Q


def analyze_query_request(search_type, query_value):
    results = []
    if search_type == 'document':
        documents = Document.objects.filter(archive_number__iexact=query_value)
        results.extend([x for x in documents])
    if search_type == 'author':
        authors = Person.objects.filter(Q(first_name__iexact=query_value) | Q(last_name__iexact=query_value)
                                | Q(full_name__iexact=query_value))
        person_locations = []
        for author in authors:
            person_locations.extend(PersonLocation.objects.filter(person=author))
        documents = []
        for pl in person_locations:
            documents.extend(Document.objects.filter(sender=pl))
        results.extend([x for x in documents])
    if search_type == 'location':
        objects = Location.objects.all()
        locations = objects.filter(place_name__iexact=query_value)
        person_locations = []
        for location in locations:
            person_locations.extend(PersonLocation.objects.filter(location=location))
        documents = []
        for pl in person_locations:
            documents.extend(Document.objects.filter(Q(sender=pl) | Q(receiver=pl)))
        results.extend([x for x in documents])
    if search_type == 'date':  # date
        objects = Document.objects.all()
        request_date = query_value.split('-')
        documents = objects.filter(date_written__year=request_date[0])
        results.extend([x for x in documents])
    return results
