from django.utils import timezone
from db.models import *

l = Location(place_name='Perth', date_modified=timezone.now(), date_added=timezone.now())
l.save()
p = Person(first_name='Test', last_name='Writer', full_name='Test Writer', date_added=timezone.now(), date_modified=timezone.now())
pl = PersonLocation(location=l, person=p)
d = Document(archive_number='test', date_written=timezone.now(), receiver=pl, sender=pl, document_type='diary', 
    language='java', date_added=timezone.now(), date_modified=timezone.now())
u = User(username='devtest', password='cits3200groupo', email='dev@test.com', active=True, permission_level=0, date_joined = timezone.now())