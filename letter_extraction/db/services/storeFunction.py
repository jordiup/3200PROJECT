
import os
import re
import nltk
from upload_service import docxscanner


def addToModel():
    test_list = [] 
    test_list = docxscanner("C:\\Users\\nic\\Documents\\GitHub\\3200PROJECT\\letter_extraction\\db\\services\\test.docx")
    print(test_list)


addToModel()
