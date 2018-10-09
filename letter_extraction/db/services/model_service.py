from db.models import Person, PersonLocation, Document, Location
from django.db.models import Q
from db.services.entities.query_entity import DocumentEntity

def get_metadata_labels():
    document = Document.objects.first()
    result_list = [format_label_as_viewable(x) for x in list(document.__dict__.keys()) if 'id' not in x and x is not '_state']
    f = open('labels.py', 'r')
    for line in f:
        result_list.append(line.split('=')[0])
    return result_list

def format_label_as_viewable(label):
    new_label = label[0].upper()
    for i in range(1, len(label)):
        if label[i-1] == '_':
            new_label += label[i].upper()
        elif label[i] == '_':
            new_label += ' '
        else:
             new_label += label[i]    
    return new_label

def format_label_as_storeable(label):
    new_label = label[0].lower()
    for i in range(1, len(label)):
        if label[i] == ' ':
            new_label += '_'
        else:
             new_label += label[i].lower()    
    return new_label

def add_metadata_label(label):
    f = open("labels.py", 'a+')
    f.write(format_label_as_storeable(label) + ' = models.CharField(max_length=64)\n')
