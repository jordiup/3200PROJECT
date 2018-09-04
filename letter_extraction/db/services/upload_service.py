# reading metadata from docx and storing in array
# need to download docx module first
# i.e. $pip install --pre python-docx

import os
import docx
import nltk
import xlrd
import re
import pandas as pd

#Excel scanner function
def xlscanner(filename):
    wb = pd.ExcelFile(filename)
    headers = ['archive code','addressee','language']
    totalsheet = len(wb.sheet_names)
    archcol = 0
    wholedoc=[]
    headstart = -1

    #Goes thru each worksheet
    for ws in range(totalsheet):
        letters = []
        sheet = pd.read_excel(wb,wb.sheet_names[ws],header=None,index_col=None)
        #Finds the data header // Goes thru each row
        for i in range (sheet.shape[0]):
            each = []
            for j in range (sheet.shape[1]):
                content = sheet.iloc[i,j]
                each.append(content)
                j=j+1

            if (headstart == -1): #Finding header
                m = 0
                for k in each:
                    if(type(k) == str):
                        if (k.lower()=='archive code'):
                            archcol = m-1
                            headstart = i
                            break
                        m = m+1
            #Only adds non-empty list to letters
            #Does not add data with no archive number

            if(not all(pd.isnull(s) for s in each)):
                letters.append(each)
            i = i+1
        wholedoc.append(letters)
    return wholedoc


#Docx scanner function
def docxscanner(filename):
    doc = docx.Document(filename)
    wholedoc = []
    #lists of every letter data
    letters = []
    summary = ''
    letterdata = []
    #regex for splitting \n and \t
    regex = re.compile(r'[\n\r\t]')

    #Stores each paragraph in a list
    for para in doc.paragraphs:
        wholedoc.append(para.text)
    k = 1 #initialise index letter
    j = 0 #initialise receiver and sender indicator
    count = 0
    #Give each words a named entity
    for sentence in wholedoc:
        count = count+1
        sentence = regex.sub("",sentence)
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        #Finds the Word Index header
        #For each new header, it will initialise a list to store all its data
        #print(sentence, wholedoc[count-1])
        if (len(tagged) == 1):
            if(tagged[0][0] == str(k)):
                if(k!=1):
                    letterdata.append(summary)
                    letters.append(letterdata)
                summary=''
                k = k+1
                letterdata = []

            #Finds letter reference number
            elif (tagged[0][1] == "JJ"):
                letterdata.append(sentence)

            #Finds Letter Sender
            elif (tagged[0][1] == "NN"):
                letterdata.append(sentence)

        #Finds Letter Sender
        if (len(tagged) > 2):
            #Detail letter pages
            if(((tagged[0][1] == "(") or (tagged[0][1] == ".")) and ((tagged[2][1] == "NNS") or (tagged[2][1] == "NN") or (tagged[1][1] == "$"))):
                letterdata.append(sentence)

            elif ( (tagged[2][1] == "CD") and ((tagged[1][1] == ",") or (tagged[1][1] == "NNP") or (tagged[1][1] == ":") or (tagged[1][1] == ".") or (tagged[3][1] == ","))):
                letterdata.append(sentence)

            elif ( (tagged[2][1] == "NNP") and ((tagged[1][1] == ",") or (tagged[1][1] == ":") or (tagged[1][1] == ".")  or (tagged[3][1] == ","))):
                if (j == 0):
                    letterdata.append(sentence)
                    j = j+1
                else:
                    letterdata.append(sentence)
                    j = j-1

            #Finds Types of letters
            elif ((tagged[0][1] == "NN") and (tagged[1][1] == ",")):
                letterdata.append(sentence)

        #ASSUME it is the letter summary if it is longer than 10
        if(len(tagged) > 10):
            summary = summary+sentence

        if(len(wholedoc) == count):
            #print(wholedoc[count-1], k-1, summary)
            letterdata.append(summary)
            letters.append(letterdata)
    return letters

def main(filename):
    #currently only for .docx and .xlsx files
    if filename.name.endswith('.docx'):
        return docxscanner(filename)
    elif filename.name.endswith('.xlsx'):
        return xlscanner(filename)
    else:
        print('Only accept .docx and .xls files')
