from django.utils import timezone
from db.models import *
from django.contrib.auth.models import User

l = Location(place_name='Perth', date_modified=timezone.now(), date_added=timezone.now())
l.save()
p = Person(first_name='Test', last_name='Writer', full_name='Test Writer', date_added=timezone.now(), date_modified=timezone.now())
p.save()
pl = PersonLocation(location=l, person=p)
pl.save()
u = User.objects.first()
d = Document(archive_number='test', date_written=timezone.now(), receiver=pl, sender=pl, document_type='diary', 
    language='java', date_added=timezone.now(), date_modified=timezone.now(), uploaded_by=u)
d.save()