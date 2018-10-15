# Metadata extraction function
# Need to download docx, pandas, re, nltk module beforehand

import docx
import nltk
import re
import pandas as pd

#storing archive number/code of the letter
#returns this as an error message to indicate which letter has an error
errindex = ''

#Xlsx and xls scanner function
def xlscanner(filename):
    global errindex
    wb = pd.ExcelFile(filename)
    totalsheet = len(wb.sheet_names)
    headlist = []
    wholedoc = []

    #Iterate through each worksheet
    for ws in range(totalsheet):
        p = 0
        headstart = -1 #Indicate that header row is not found yet
        archcol = 0
        letters = []
        sheet = pd.read_excel(wb,wb.sheet_names[ws],header=None,index_col=None)
        #Append each non-empty row content
        for i in range (sheet.shape[0]):
            each = []
            for j in range (sheet.shape[1]):
                content = sheet.iloc[i,j]
                if(headstart == -1):
                    if(not pd.isnull(content)):
                        each.append((j,content))
                j=j+1
            #Assumes it is the content once the header row is found (i.e. headstart != -1)
            if(headstart != -1):
                for xx in range(headlist[ws][0][0],len(headlist[ws])+headlist[ws][0][0]):
                    content = sheet.iloc[i,xx]
                    #Set an empty cell to "None"
                    if (pd.isnull(content)):
                        content = 'None'
                        each.append((headlist[ws][xx-headlist[ws][0][0]][1],content))
                    #Data cleaning and storing
                    elif(type(content)!= int and re.match(r'[\[ \]]',content)):
                        each.append((headlist[ws][xx-headlist[ws][0][0]][1],content.strip(' [ ] ( ) ?')+' inferred'))
                    else:
                        each.append((headlist[ws][xx-headlist[ws][0][0]][1],content))
            
            #Finding header row
            if (headstart == -1):
                m = 0
                for k in each:
                    if(type(k[1]) == str):
                        #Assumes it is a header row if it has 'Archive Code' or 'Archive number' as one of the cell content
                        if (k[1].lower()=='archive code' or k[1].lower()=='archive number'):
                            archcol = m
                            headstart = i #Indicates that the header row is found
                            headlist.append(each)
                            #stores archive number of a letter for error handling message
                            errindex = each[archcol][1]
                            break
                    m=m+1
            #Only adds non-empty list to letters
            #Does not add row with no archive number
            if( (not each) or (headstart == -1)):
                continue
            if (pd.isnull(each[archcol][1]) or each[archcol][1] == 'None'):
                continue
            if(not all(s[1] == 'None' for s in each)):
                letters.append(each)
            i = i+1
        wholedoc.append(letters)
    #error handling
    if (not headlist):
        wholedoc=[]
    #returns the letters as an array
    return wholedoc

#Fills in non-given metadata as an empty string (for word document only)
def filler(myletter):
    #indicator is the amount of header categories in the word document
    indicator = [0,1,2,3,4,5,6,7,8,9]
    for i in myletter:
        for j in indicator:
            if (i[0] == j):
                indicator.remove(j)
    #Adds empty string for non-given metadata
    for m in indicator:
        myletter.append( (m, "None") )

#Miscellenaous function
def shorten_summary(summary):
    result = ''
    for i in range(0,200):
        try:
            result += summary[i]
        except IndexError:
            break
    result += ' ...'
    return result

#Docx and doc (word document) function
def docxscanner(filename):
    global errindex
    doc = docx.Document(filename)
    wholedoc = [] #Contains every letter
    letters = [] #Contains a letter
    summary = ''
    npages = ''
    letterdata = [] 
    headername = [(0,'Reference Code'),(1,'Archive Collection'),(2,'Date written'),(3,'Author'),(4,'Author Location'),
    (5,'Recipient'),(6,'Recipient Location'),(7,'Types and Language'),(8,'Summary'),(9,'Physical Description')]
    letters.append(headername)
    #regex for splitting \n and \t
    regex = re.compile(r'[\n\r\t]')

    #Stores each sentence in an array
    for para in doc.paragraphs:
        wholedoc.append(para.text)
    k = 1 #initialise index letter
    j = 0 #initialise receiver and sender indicator
    count = 0
    nlines = 0

    #Goes through the array of sentences and give each word a named entity via NLTK
    #The purpose is to determine what information that a sentence holds
    #Such that appropriate storing can be done
    for sentence in wholedoc:
        count = count+1
        sentence = regex.sub("",sentence)
        tokens = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        
        #Assume it is the delimiter if it has a length of 1
        if (len(tagged) == 1):
            if(tagged[0][0] == str(k)):
                #Storing n-1 letters, where n is the delimiter
                if(k!=1):
                    #Check if summary and npages is not empty
                    if( not not summary ):
                        letterdata.append((8,summary))
                        #shortened_summary = shorten_summary(summary)
                        #letterdata.append((8,shortened_summary))
                    if (not not npages):
                        letterdata.append((9,npages))
                    filler(letterdata) #Fills empty metadata as None
                    letterdata = sorted(letterdata)
                    if(letterdata[0][1] != "None"):
                        letters.append(letterdata) #Stores the letter into an array of letters
                #Reset variables
                summary=''
                npages=''
                nlines = 0
                j=0
                k = k+1
                letterdata = []

            #Finds letter archive number/code (0)
            # i.e. reference number with format similar to 2-2244A/14.001
            # Assume a archive number/code contains a digit
            elif (tagged[0][1] == "JJ" or tagged[0][1] == "CD" or (tagged[0][1] == "NN" and any((c in "[]-/()") for c in tagged[0][0]))):
                if (any((c in "[]-/") for c in sentence) and any(d.isdigit() for d in sentence)):
                    letterdata.append((0,sentence))
                    errindex = sentence

            #Finds Archive Collection Name (1)
            #Assume Archive name is length of 1
            elif ( (tagged[0][1] == "NN" or tagged[0][1] == "NNS" or tagged[0][1] == "VBG")and (not any((c in ",") for c in sentence))):
                letterdata.append((1,sentence))

        #Finds letter reference number (0) 
        # Assume a archive number/code contains a digit
        # This line of code ensures that archive number/code that has a length of more than 1 and less than 5
        # i.e. reference number with format similar to NN 2234A-13-363 
        elif( len(tagged) >=2 and len(tagged) < 5):
            if (tagged[0][1] == "JJ" or tagged[0][1] == "NNP" or tagged[1][1] == "JJ"):
                if (any((c in "[]-/()") for c in sentence) and any(d.isdigit() for d in sentence)):
                    letterdata.append((0,sentence))
                    errindex = sentence

        #Finds Letter Sender and Receiver; Assumes the first instance of [Name, Place] is the sender
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

        #ASSUME it is the letter summary if it is longer than 10 words
        #Summary of letters indicated by (8)
        if(len(tagged) > 10):
            summary = summary+sentence

        #amount pages (9)
        if (len(tagged) > 2 and nlines > 4):
            if(((tagged[0][1] == "(") or (tagged[0][1] == ".")) and ((tagged[2][1] == "NNS") or (tagged[2][1] == "NN") or (tagged[1][1] == "$"))):
                npages = sentence

        #Stores last letter of the document
        if(len(wholedoc) == count):
            if( not not summary ):
                letterdata.append((8,summary))

                # UNCOMMENTING THE BELOW TWO LINES AND COMMENTING THE ABOVE LINE WILL SHORTEN THE SUMMARIES
                # IN ORDER TO MAKE THE PREVIEW MORE READABLE. HOWEVER, THIS WILL MESS WITH THE EDIT FEATURE.
                # R.M

                #shortened_summary = shorten_summary(summary)
                #letterdata.append((8,shortened_summary))
            if (not not npages):
                letterdata.append((9,npages))
            filler(letterdata)
            letterdata = sorted(letterdata)
            if(letterdata[0][1] != "None"):
                letters.append(letterdata)
        nlines = nlines+1
    #Error handling; Checks if the word document is in the right format
    #This is done by checking the archive number/code
    #Does not store anything if it does not contain any
    if(k==1):
        letters = []
    return letters

def main(filename):
    global errindex
    errmsg = ''
    #Process word document
    if (filename.name.endswith('.docx')):
        try:
            errindex = ''
            return docxscanner(filename), errmsg
        except:
            # Returns error message on error
            # Sends letter reference number to the user to let user know
            errmsg = 'There is a formatting issue in letter with reference number: '+ errindex
            errindex = ''
            return [],errmsg

    #Process excel document
    elif ((filename.name.endswith('.xlsx')) or (filename.name.endswith('.xls'))):
        try:
            errindex = ''
            return xlscanner(filename), errmsg
        except:
            if(errindex == ''):
                errmsg = 'There is a formatting issue '
            else:
                errmsg = 'There is a formatting issue in letter with reference number: '+ errindex
            errindex = ''
            return [], errmsg
    else:
        #Sends an error message
        print('Only accept .docx and .xls files')
