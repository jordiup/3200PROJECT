from db.models import *
from django.db.models import Q

def analyzeQueryRequest(search_type, query_value):
    results = []
    if search_type == 'document':
        objects = Document.objects.all()
        document = objects.filter(archive_number__iexact=query_value)
        if document is not None:
            results.append([x for x in document])
    elif search_type == 'author':
        objects = Person.objects.all()
        author = objects.filter(Q(first_name__iexact=query_value) | Q(last_name__iexact=query_value)
                                | Q(full_name__iexact=query_value))
        if author is not None:
            results.append([x for x in author])
    elif search_type == 'location':
        objects = Location.objects.all()
        location = objects.filter(place_name__iexact=query_value)
        if location is not None:
            results.append([x for x in location])
    else:  # date
        objects = Document.objects.all()
        request_date = query_value.split('-')
        document = None
        if request_date.__len__() == 1:
            document = objects.filter(date_written__year=request_date[0])
        if document is not None:
            results.append([x for x in document])
