
import os
import re
import nltk
from upload_service import docxscanner


def addToModel():
    test_list = []
    test_list = docxscanner("C:\\Users\\nic\\Documents\\GitHub\\3200PROJECT\\letter_extraction\\db\\services\\test.docx")
    print(len(test_list))
    print(test_list[1])
    for i in range(0, len(test_list-1)):
        print(input[i])
    tester = test_list[0]
    holder_of_categories = []
    start_index = 0
    end_index = 0
    count = 0
    print(tester[2][0])
    for index, character in enumerate(tester):
        print(character)

addToModel()
