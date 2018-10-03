import os
import re
import nltk
import math

from django.utils import timezone
from db.models import *

def dicitonary_split(input_dictionary, a, b):
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



def archive_number_finder(input, archive_number_holder):
    count = 0
    duplicates = []
    count_h = 0
    for item in range(1, len(input)):
        container = input[item]
        for info in container:
            if(isinstance(info[0], int) == True):
                if(info[0] == 0):
                    duplicates.insert(count, info[1])
                    count = count + 1
            if(info[0] == 'Archive code'):
                duplicates.insert(count, info[1])
                count = count + 1
    for object in duplicates:
        if Document.objects.filter(archive_number__iexact = object).exists():
            archive_number_holder.insert(count_h, object)
