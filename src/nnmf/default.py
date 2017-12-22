import re # import regular expression module
import  numpy  # import numpy for matrix & array features
from numpy import *
import csv 
import os
import sys
import platform
import json

import nmf as nmf # import non negative matrix factorization algorithm
import porter as porter # import porter.py - porter stemmer algorithm
import SurveyQuestionThemes as surveythemer
# coding: utf8 

# import logging
# logging.basicConfig(filename='/var/www/htdocs/conceptquestions/nnmf/conceptquestions.log',filemode='w', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(lineno)d %(filename)s %(message)s ')
# logger=logging.getLogger(__name__)
#print "Python Working"

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    
def findthemes(nothemes,wordlist,question_responses,stop_words):
    synonym_wordlists = []
    synonym_wordlist = wordlist
    synonym_wordlists = synonym_wordlist.splitlines()
    exclude_wordlist = []
    surveyQuestionResponse = []
    favourites = []
    questionIDs = []
    
    
    for response in question_responses:
      newresp = remove_html_tags(response[0])
      
      for synliststring in synonym_wordlists:
        synlist = synliststring.split(",")
        mainsyn = synlist[0]
        for synword in synlist[1:len(synlist)]:
            newresp = newresp.replace(synword,mainsyn)
            #print newresp
      surveyQuestionResponse.append(newresp)
      favourites.append(response[1])
      questionIDs.append(response[2])
      
    listOfAllWords, listOfSurveyQuestionWords, listOfAllSurveyQuestionTitles, stemdictionary = surveythemer.getItemWords(surveyQuestionResponse,stop_words)
    wordMatrix, listOfWordsIncluded, wordCount, fc, ic = surveythemer.createWordMatrix(listOfAllWords,listOfSurveyQuestionWords)

    if (wordMatrix.shape[0] < nothemes+1):
        return '{"themesData": "Not enough data"}'
        #sys.exit("Not enough data")
    w,h = surveythemer.nndsvd(wordMatrix,nothemes,1)
    if not h.any():
        return '{"themesData": "Empty"}'
    # sys.exit("Error message")
    nmfresult = ""
    themes = ""
    
    weights,themes = nmf.nmf(wordMatrix,w,h,0.001, 10, 500)
	
    json,data = surveythemer.display_themes(weights,themes,listOfWordsIncluded,surveyQuestionResponse, stemdictionary, wordCount, favourites, questionIDs)
    # print theme_html
    returnData = '{"themesData":'+ data +', "jsonData":'+ json + '}'    
    return returnData
  
####
if __name__ == '__main__':

    if (sys.argv[1] == 'check'):
        sys.exit('true')
    else: 
        data = json.loads(sys.argv[1])
    nothemes = int(sys.argv[2])
    stop_words = sys.argv[3]
    
    question_responses = []
    # # Read the column names from the first line of the file  
    fields = ['answer','favourite','questionID']
    # print fields
    #print data
    items = ""
    count = 1
    for row in data:
    
        count = count + 1
    # Zip together the field names and values  
    
    items = zip(fields, row)  
    item = {}
    # Add the value to our dictionary  
    for (name, value) in items:  
        item[name] = re.sub('[^A-Za-z0-9]+', ' ', value.strip() )
        
    question_responses.append(item)

    returnedData = findthemes(nothemes,"",question_responses,stop_words)
    print returnedData