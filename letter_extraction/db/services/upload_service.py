# reading metadata from docx and storing in array
# need to download docx, pandas, re, nltk module first
# i.e. $pip install --pre python-docx

import os
import docx
import nltk
import re
import pandas as pd

#Xlsx and xls scanner function
def xlscanner(filename):
    wb = pd.ExcelFile(filename)
    #headers = ['archive code','addressee','language']
    headlist = []
    totalsheet = len(wb.sheet_names)
    archcol = 0
    wholedoc=[]

    #Goes thru each worksheet
    for ws in range(totalsheet):
        p = 0
        headstart = -1
        letters = []
        sheet = pd.read_excel(wb,wb.sheet_names[ws],header=None,index_col=None)
        #Stores header names
        for i in range (sheet.shape[0]):
            each = []
            for j in range (sheet.shape[1]):
                content = sheet.iloc[i,j]
                if(headstart == -1):
                    if(not pd.isnull(content)):
                        each.append((j,content))
                j=j+1
            #content storage
            if(headstart != -1):
                for xx in range(headlist[ws][0][0],len(headlist[ws])+headlist[ws][0][0]):
                    content = sheet.iloc[i,xx]
                    if (pd.isnull(content)):
                        content = 'None'
                    each.append((headlist[ws][xx-headlist[ws][0][0]][1],content))
            
            if (headstart == -1): #Finding header
                m = 0
                for k in each:
                    if(type(k[1]) == str):
                        if (k[1].lower()=='archive code'):
                            archcol = m
                            headstart = i
                            headlist.append(each)
                            break
                    m=m+1

            #Only adds non-empty list to letters
            #Does not add data with no archive number
            if(not each):
                continue
            if (pd.isnull(each[archcol][1])):
                continue
            if(not all(s[1] == 'None' for s in each)):
                letters.append(each)
            i = i+1
        wholedoc.append(letters)
    #error handling
    if (not headlist):
        wholedoc=[]
    return wholedoc

#Fills in non-given metadata as empty string
def filler(myletter):
    indicator = [0,1,2,3,4,5,6,7,8,9]
    for i in myletter:
        for j in indicator:
            if (i[0] == j):
                indicator.remove(j)
    #Adds empty string for non-given metadata
    for m in indicator:
        myletter.append( (m, "None") )

#Docx scanner function
def docxscanner(filename):
    doc = docx.Document(filename)
    wholedoc = []
    #lists of every letter data
    letters = []
    summary = ''
    npages = ''
    letterdata = []
    headername = [(0,'Reference Code'),(1,'Archive Collection'),(2,'Date written'),(3,'Author'),(4,'Author Location'),
    (5,'Recipient'),(6,'Recipient Location'),(7,'Types and Language'),(8,'Summary'),(9,'Physical Description')]
    letters.append(headername)
    #regex for splitting \n and \t
    regex = re.compile(r'[\n\r\t]')

    #Stores each paragraph in a list
    for para in doc.paragraphs:
        wholedoc.append(para.text)
    k = 1 #initialise index letter
    j = 0 #initialise receiver and sender indicator
    count = 0
    nlines = 0
    #Give each words a named entity
    for sentence in wholedoc:
        count = count+1
        sentence = regex.sub("",sentence)
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        #Finds the Word Index header
        #For each new header, it will initialise a list to store all its data
        if (len(tagged) == 1):
            if(tagged[0][0] == str(k)):
                if(k!=1):
                    #Check if summary and npages is not empty
                    if( not not summary ):
                        letterdata.append((8,summary))
                    if (not not npages):
                        letterdata.append((9,npages))
                    filler(letterdata)
                    letterdata = sorted(letterdata)
                    if(letterdata[0][1] != "None"):
                        letters.append(letterdata)
                summary=''
                npages=''
                nlines = 0
                j=0
                k = k+1
                letterdata = []

            #Finds letter reference number (0)
            elif (tagged[0][1] == "JJ"):
                letterdata.append((0,sentence))

            #Finds Archive Collection (1)
            elif (tagged[0][1] == "NN"):
                letterdata.append((1,sentence))

        #Finds Letter Sender
        if (len(tagged) > 2 and len(tagged) < 10 and nlines < 8):
            #Dates (2) in (Day, Date Month Year) or (Day, Month Date Year)
            if ( (tagged[2][1] == "CD" or tagged[len(tagged)-1][1] == "CD") and ( tagged[1][1] == 'NNP' or tagged[2][1] == 'NNP' or tagged[3][1] == "NNP") and ((tagged[1][1] == ",") or (tagged[1][1] == "NNP") or (tagged[1][1] == ":") or (tagged[1][1] == ".") or (tagged[3][1] == ","))):
                letterdata.append((2,sentence))

            #Sender (3) and its' location (4)
            #Addresse (5) and its' location (6)
            elif( len(letterdata) < 7):        
                if ( (tagged[len(tagged)-1][0] == "]" or tagged[len(tagged)-1][0] == ")" or tagged[len(tagged)-1][1] == "." or tagged[len(tagged)-1][1] == "NNP")and ((tagged[0][1] == "NNP") or tagged[0][1] == "JJ") ):
                    if (j == 0):
                        sentence = sentence.split(',',1)
                        if ( len(sentence) == 1):
                            sentence = sentence[0].split(';',1)
                            if ( len(sentence) == 1): 
                                continue
                        #data cleaning
                        if(re.match(r'[\[ \]]',sentence[0].strip())):
                            letterdata.append((3,sentence[0].strip(' [ ] ( ) ?')+' inferred'))
                        else:
                            letterdata.append((3,sentence[0].strip(' [ ] ( ) ?')))
                        if(re.match(r'[\[ \]]',sentence[1].strip())):
                            letterdata.append((4,sentence[1].strip(' [ ] ( ) ?')+' inferred'))
                        else:
                            letterdata.append((4,sentence[1].strip(' [ ] ( ) ?')))
                        j = j+1
                        continue
                    else:
                        sentence = sentence.split(',',1)
                        if ( len(sentence) == 1):
                            sentence = sentence[0].split(';',1)
                            if ( len(sentence) == 1): 
                                continue
                        #data cleaning
                        if(re.match(r'[\[ \]]',sentence[0].strip())):
                            letterdata.append((5,sentence[0].strip(' [ ] ( ) ?')+' inferred'))
                        else:
                            letterdata.append((5,sentence[0].strip(' [ ] ( ) ?')))
                        if(re.match(r'[\[ \]]',sentence[1].strip())):
                            letterdata.append((6,sentence[1].strip(' [ ] ( ) ?')+' inferred'))
                        else:
                            letterdata.append((6,sentence[1].strip(' [ ] ( ) ?')))
                        j = j-1
                        continue
            #Finds Types of letters (7)
            if ((tagged[0][1] == "NN" or tagged[0][1] == "NNP") and (tagged[len(tagged)-1][1] == "JJ" or tagged[len(tagged)-1][0] == "English") and ((tagged[1][1] == ",") or (tagged[1][1] == ".") or (tagged[2][1] == ",") or (tagged[2][1] == "."))):
                letterdata.append((7,sentence))
        #ASSUME it is the letter summary if it is longer than 15 words
        #Summary of letters in (8)
        if(len(tagged) > 15):
            summary = summary+sentence

        #amount pages (9)
        if (len(tagged) > 2 and nlines > 4):
            if(((tagged[0][1] == "(") or (tagged[0][1] == ".")) and ((tagged[2][1] == "NNS") or (tagged[2][1] == "NN") or (tagged[1][1] == "$"))):
                npages = sentence

        #Last letter of the document
        if(len(wholedoc) == count):
            #letterdata.append((8,summary))
            if( not not summary ):
                letterdata.append((8,summary))
            if (not not npages):
                letterdata.append((9,npages))
            filler(letterdata)
            letterdata = sorted(letterdata)
            if(letterdata[0][1] != "None"):
                letters.append(letterdata)
        nlines = nlines+1
    #Checks if document is a correct format or not
    if(k==1):
        letters = []
        return letters
    return letters

def main(filename):
    #currently only for .docx and .xlsx and .xls files
    if (filename.name.endswith('.docx')):
        return docxscanner(filename)
    elif ((filename.name.endswith('.xlsx')) or (filename.name.endswith('.xls'))):
        return xlscanner(filename)
    else:
        print('Only accept .docx and .xls files')
