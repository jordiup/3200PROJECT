# reading metadata from docx and storing in array
# need to download docx module first
# i.e. $pip install --pre python-docx

import os
import docx
import nltk 

def docxscanner(filename):
    if os.path.exists(filename): #If file exists
        f = open(filename, 'r')
        doc = docx.Document(filename)
        wholedoc = []
        
        #Stores each paragraph in a list
        for para in doc.paragraphs:
            wholedoc.append(para.text)
        f.close()

        k = 1 #initialise index letter
        j = 0 #initialise receiver and sender indicator
        #Give each words a named entity
        for sentence in wholedoc:
            tokens = nltk.word_tokenize(sentence)
            tagged = nltk.pos_tag(tokens)
            #print(tagged)

            #Finds the Word Index header
            if (len(tagged) == 1):
                if(tagged[0][0] == str(k)):
                    print('Word letter index',sentence)
                    k = k+1
                            
                #Finds letter reference number
                if (tagged[0][1] == "JJ"):
                    print('Letter Reference Number: ',sentence)

                #Finds Letter Sender
                if (tagged[0][1] == "NN"):
                    print('Sender: ',sentence)

            #Finds Letter Sender
            if (len(tagged) > 3):
                if ( (tagged[2][1] == "CD") and ((tagged[1][1] == ",") or (tagged[1][1] == ":") or (tagged[1][1] == ".") or (tagged[3][1] == ","))):
                    print('Written on: ', sentence)

                if ( (tagged[2][1] == "NNP") and ((tagged[1][1] == ",") or (tagged[1][1] == ":") or (tagged[1][1] == ".")  or (tagged[3][1] == ","))):
                    if (j == 0):
                        print('Receiver and Location: ', sentence)
                        j = j+1
                    else:
                        print('Sender and Location: ', sentence)
                        j = j-1
                        
                #Finds Correspondence
                if ((tagged[0][1] == "NN") and (tagged[1][1] == ",")):
                    print('Correspondence: ',tagged[2][0])            

            #ASSUME it is the letter summary if it is longer than 10 
            if(len(tagged) > 10):
                print(sentence)

            #For drawing named entity tree
            #namedEnt = nltk.ne_chunk(tagged, binary=True)
            #namedEnt.draw()
        
    else: #If file is not found
        print('The file called', filename + ' cant be found')
        
def main():
    filename = input("Enter the file name wished to be scanned:")
    #currently only for .docx files
    if filename.endswith('.docx'):
        docxscanner(filename)
    else:
        print('Only accept .docx and .xls files')
main()
