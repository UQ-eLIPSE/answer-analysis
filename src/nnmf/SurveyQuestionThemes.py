import re # import regular expression module
from numpy import * # import numpy for matrix & array features
from numpy.linalg import svd
from numpy.linalg import norm
#import nnmf # import non negative matrix factorization algorithm
import porter # import porter.py - porter stemmer algorithm
import json

##
# A collection of functions for using Non Negative Matrix Factorization to find themes in open ended survey questions

##
# Utility function to return a list of all words that are have a length greater than a specified number of characters.
# @param text The text that must be split in to words.
# @param minWordReturnSize The minimum no of characters a word must have to be included.
def separatewords(text,minWordReturnSize):
  #splitter=re.compile('\\W*')
  splitter=re.compile('[^a-zA-Z0-9_\\+\\-]')
  return [singleWord.lower() for singleWord in splitter.split(text) if len(singleWord)>minWordReturnSize]

##
# Utility function to sort a dictionary by Value in decending order
# Not the most efficient implementation - may need to refactor if speed becomes an issue
# @param dictionary The dictionary data structure.
# @return list A list of keys sorted by their value.
def sortDictionaryByValues(dictionary):
    """ Returns the keys of dictionary d sorted by their values """
    items=dictionary.items()
    backitems=[ [v[1],v[0]] for v in items]
    backitems.sort()
    backitems.reverse()
    return [ backitems[i][1] for i in range(0,len(backitems))]

##
# Utility function to remove stop words that are present in a list of words
# @param wordlist Unfiltered list of words
# @param stopwordlist List of stops words
# @return list Filtered list of words
def removeStopWords(wordlist,stopwordlist):
    return [word for word in wordlist if word not in stopwordlist]

##
# This function returns a list of all words that are have a length greater than a specified number of characters.
# @param text The text that must be split in to words.
# @param minWordReturnSize The minimum no of characters a word must have to be included.
def getItemWords(list_of_words,stop_words):
  stemmer=porter.PorterStemmer()
  allwords={}
  itemwords=[]
  itemtitles=[]
  ec=0
  stemlist = {}
  # Loop over every item in list_of_words
  for item in list_of_words:
      words=separatewords(item,1)
      words = removeStopWords(words,stop_words)
      itemwords.append({})
      itemtitles.append("Response " + str(ec+1))
      # Increase the counts for this word in allwords and in articlewords
      for word in words:
        unstemmedword = word
        word=stemmer.stem(word,0,len(word)-1)
	if word in stemlist:
		temp = stemlist[word]
 		try:
        		temp.index(unstemmedword)
   		except ValueError:
			temp.append(unstemmedword)
			stemlist[word] = temp
	else:
		temp = []
		temp.append(unstemmedword)
		stemlist[word] = temp	
        allwords.setdefault(word,0)
        allwords[word]+=1
        itemwords[ec].setdefault(word,0)
        itemwords[ec][word]+=1
      ec+=1
  return allwords,itemwords,itemtitles,stemlist


##
# Returns the document (row) and words (columns) matrix and the list of words as a vector
def createWordMatrix(all_words,words_inItems):
    #print all_words
    #print words_inItems
    wordvector=[]
    # Only take words that are common but not too common
    for w,c in all_words.items():
        wordvector.append(w)
        #if c<len(words_inItems)*0.6: #*0.2
    # Create the word matrix
    cols = len(wordvector)
    rows = len(words_inItems)
   
    l1=[[(wrd in f and f[wrd] or 0) for wrd in wordvector] for f in words_inItems]
    wordMatrix = array(l1)
    wordCount = []
    sum = 0
    for c in range(0, cols):
        for r in range(0, rows):
            sum += wordMatrix[r][c]
        wordCount.append(sum)
        sum = 0
    return wordMatrix, wordvector, wordCount, cols, rows

def make_highlight(txt,wordlist,alt):
    if (txt=="+"):
      search_txt = "+"
      display_txt = "Positive"
    elif (txt=="-"):
      search_txt = "-"
      display_txt = "Negative"
    else:
      display_txt = txt #",".join(wordlist)
      title_txt = ",".join(wordlist)
      search_txt = txt.upper()

    highlight = "<button class=\"btn btn-sm btn-default theme theme-text\" title=\"" + title_txt + "\" class=\"theme theme-text\" data-searchtext="+ search_txt +" href=\"javascript:void(0);\">" + display_txt + " [" + alt + "]</button>"
    return highlight

def generate_graphml(ThemeDictionary,DocDictionary,TermDictionary,DocInTheme,TermInTheme):
    #Generate graphml
    graphML = '<?xml version="1.0" encoding="UTF-8"?>\n'
    graphML = graphML + '<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
    graphML = graphML + 'xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n'
    graphML = graphML + '<graph id="G" edgedefault="directed">\n'
    # Generate the nodes
        
    for node in ThemeDictionary:
        graphML += '<node type="theme" id="' + node + '" order="1" name="' + ThemeDictionary[node] +'"/>\n' 
            
    for node in DocDictionary:
        graphML += '<node type="document" id="' + node + '" order="1" name="' + DocDictionary[node] +'"/>\n' 
            
    for node in TermDictionary:
        graphML += '<node type="term" id="' + node + '" order="1" name="' + ",".join(TermDictionary[node]) +'"/>\n' 

    # Generate the edges (ie links between nodes)
    for noderel in DocInTheme:
        #print noderel
        fromToArray = noderel.split("_")
        #print fromToArray
        graphML += '<edge source="' + fromToArray[0] + '" target="' + fromToArray[1] + '" count="' + str(5) + '"/>' + '\n' #DocInTheme[relationship]
            
    for noderel in TermInTheme:
        #print relationship
        fromToArray = noderel.split("_")
        #print fromToArray
        graphML += '<edge source="' + fromToArray[0] + '" target="' + fromToArray[1] + '" count="' + str(2) + '"/>' + '\n' #TermInTheme[relationship]

    graphML += '</graph>\n'
    graphML += '</graphml>\n'
    return graphML

def generate_json(ThemeDictionary,DocDictionary,TermDictionary,DocInTheme,TermInTheme):
    #Generate json graph structure
    json = '{\n'
    # Generate the nodes
    
    json += '"nodes":{\n'
    for node in ThemeDictionary:
        json += '"' + node + '":{"color":"#d44c5e", "shape":"dot", "alpha":1, "label":"' + ThemeDictionary[node] + '"},\n' 
    
    termCount = 1
    for node in TermDictionary:
        json += '"' + node + '":{"color":"#005793", "shape":"rectangle", "alpha":1, "label":"' + node + '"}\n'  
        if termCount < len(TermDictionary) :
            json += ", "
        termCount = termCount + 1
    json += '},\n' 

    json += '"edges":{'
   
    # Generate the edges (ie links between nodes)
    # First need to collact on a dictionary
    ThemeNodeDict = {};
    for noderel in TermInTheme:
        #print relationship
        fromToArray = noderel.split("_")
	if (not ThemeNodeDict.has_key(fromToArray[0])):
		#print fromToArray
		fromToList = []
		fromToList.append(fromToArray[1])
		ThemeNodeDict[fromToArray[0]] = fromToList;
		#print ThemeNodeDict[fromToArray[0]]
		#print "\n"
	else:
		fromToList = ThemeNodeDict[fromToArray[0]]
		fromToList.append(fromToArray[1])
		#print fromToList
		#print "\n"
		ThemeNodeDict[fromToArray[0]] = fromToList;
		#print ThemeNodeDict[fromToArray[0]]
		#print "\n"
    
    ThemeNodeCount = 1
    
    for node in ThemeNodeDict:
        fromNode = node
        connectingNodes = ThemeNodeDict[node]
        json += '"' + node + '":{\n'  #t2,T1
        nodeCount = 1
        for subnode in connectingNodes:
            json += '"' + subnode + '":{"length":2.5,"weight":4}' 
            if (nodeCount < len(connectingNodes)):
                json += ", " 

            nodeCount = nodeCount + 1
    
        json += '}\n' 
        if (ThemeNodeCount < len(ThemeNodeDict)):
            json += ", "
        ThemeNodeCount = ThemeNodeCount + 1
    json += '}}\n'
    return json


##
# Display themes, top six words in a theme and associated documents in theme.
def display_themes(weights_matrix, themes_matrix, list_Of_Included_Words, item_Titles, stemdictionary, wordCount, favourites, questionIDs):
    # Data structures for Graph Representation
    ThemeDictionary = {}
    DocDictionary = {}
    TermDictionary = {}
    # Data structures to represent relationships
    DocInTheme = {}
    TermInTheme = {}
    # Start of NMF interpretation
    norows,nocols = shape(themes_matrix)
    noarticles,nofeatures = shape(weights_matrix)
    d1={}
    count = 1
    # theme_html = ""
    tr_class = ""
    remark_title = ""
    remark = ""
    remark_class = ""
    jsonTheme = '{\n'
    # Generate the nodes
    
    for row in range(norows):
        ThemeDictionary["T" + str(count)] = "Theme " + str(count)
        div_id = "content-area" #"theme_responses_" + str(count)
        # theme_html = theme_html + "<div class=\"panel panel-default\">"
        # theme_html = theme_html + "<div class=\"panel-heading panel-sm theme-panel \">Theme " + str(count) + "</div>"
        # theme_html = theme_html + "<div class=\"panel-body\"><div class=\"theme-words\">"
        #jsonTheme["theme" + str(count)] = "Theme " + str(count)
        jsonTheme += '"Theme' + str(count) +'":{\n'
        
        for col in range(nocols):
            d1[list_Of_Included_Words[col]] = themes_matrix[row,col]
        themes_list_in_order = sortDictionaryByValues(d1)
        noOfWords = 6 if len(d1) > 6 else len(d1)
        wordListCount = 1
        jsonTheme += '"words":{'
        for it in themes_list_in_order[0:6]:
            jsonTheme += '"word'+str(wordListCount)+'":{\n'
            jsonTheme += '"word":"'+ it +'",\n'
            jsonTheme += '"wordlist":["'+ '","'.join(stemdictionary[it]) +'"],\n'
            jsonTheme += '"wordweight":"'+ str("%.2f" % d1[it]) +'"\n'
            #jsonTheme['txt' + str(count)] = it
            #jsonTheme['wordlist' + str(count)] = stemdictionary[it]
            #jsonTheme['alt' + str(count)] = str("%.2f" % d1[it])
            # theme_html = theme_html + make_highlight(it,stemdictionary[it],str("%.2f" % d1[it])) + " "
            word_index = list_Of_Included_Words.index(it)
            TermDictionary[it] = stemdictionary[it]
            TermInTheme["T" + str(count) + "_" + it] = str("%.2f" % d1[it])
            
            jsonTheme += "},\n" if noOfWords > wordListCount  else "}"
            wordListCount += 1
            
        # theme_html = theme_html + "</div>" 
        jsonTheme += '},'
        # Print articles/items/survey responses that map to Theme/Feature
        articlesInTheme = {}
        articleweights=[]
        #  print len(range(noarticles))
        for article in range(noarticles):
           
          if (weights_matrix[article,row] > 0.05):
              articlesInTheme[article] = weights_matrix[article,row]
              articleweights.append(weights_matrix[article,row])
              DocDictionary["D" + str(article)] = "Doc" + str(article)
              DocInTheme["T" + str(count) + "_D" + str(article)] = str("%.2f" % weights_matrix[article,row])
          else:
              # Capture all non attached documents
              DocDictionary["D" + str(article)] = "Doc" + str(article)
        if articleweights:
            max_weight_val = max(articleweights)
            min_weight_val = min(articleweights)
            jsonTheme += '"maxweight":"'+ ("%.2f" % max_weight_val) +'",\n'
            jsonTheme += '"minweight":"'+ ("%.2f" % min_weight_val) +'",\n'
            jsonTheme += '"responses":{'
            articles_In_Theme_Order = sortDictionaryByValues(articlesInTheme)
            article_count = 1
            countArticle = len(articles_In_Theme_Order)
            for article_no in articles_In_Theme_Order:
              jsonTheme += '"response'+str(article_count)+'":{"weight":"'+ ("%.2f" % weights_matrix[article_no,row]) +'",'
              jsonTheme += '"response":"'+ item_Titles[article_no] +'",'
              jsonTheme += '"questionID":"'+ questionIDs[article_no] +'",'
              jsonTheme += '"remark":"'+ str(favourites[article_no]) +'"}'
                
              if (article_count<countArticle) :
                  jsonTheme += ",\n"
            
              article_count += 1 
            jsonTheme += '}'
        else:
            print "empty"

        jsonTheme += "}"
        
        if (count<norows) :
            jsonTheme += ","
        count = count + 1
        
    jsonTheme += "}"  
    json = generate_json(ThemeDictionary,DocDictionary,TermDictionary,DocInTheme,TermInTheme)
    
    return json, jsonTheme
##
# Strange way to determine if NaN in Python?
def isNaN(x):
    return (x == x) == False



def pos(A):
    Ap = (A>=0)*A
    return Ap

def neg(A):
    Am = (A<0)*(-A);
    return Am

def nndsvd(A,k,flag):
    #size of input matrix
    m, n = A.shape
    #the matrices of the factorization
    W = zeros([m, k])
    H = zeros([k, n])
   
    #1st SVD --> partial SVD rank-k to the input matrix A.
    U,S,V = svd(A,k)
    c = array(U)
    #print "S1",S[0]
    #print "U",U
    #print "c[0][:]",c[:][1]
    #print "c[:][1]",c[0,:]
    #choose the first singular triplet to be nonnegative
    Utemp = zeros([m]);
    
    for i in range(0, m):
       
        Utemp[i] = U[i][0]
    #print "Utemp",Utemp
   
    Wtemp = sqrt(S[0]) * abs(Utemp)
    
    for i in range(0, k+1):

        W[i][0] = Wtemp[i]
    Htemp = sqrt(S[0]) * abs(V[:][0].T)
    for i in range(0, n):
        H[0][i] = Htemp[i]

    #print "Wtemp", Wtemp
    #print "W", W
    #print "Htemp", Htemp
    #print "H", H

    # second SVD for the other factors (see table 1 in our paper)
    # AB - check on k-1
    for i in range(1, k):
            #print "in loop", i
            uuTemp = zeros([m]);
            for l in range(0, m):
                uuTemp[l] = U[l][i]
            #print "uuTemp",uuTemp
            uu = uuTemp
            #print "uu",uu
            vv = V[:][i]
            print "vv",len(vv)
            uup = pos(uu)
            uun = neg(uu)
            vvp = pos(vv)
            vvn = neg(vv)
            n_uup = norm(uup)
            n_vvp = norm(vvp)
            n_uun = norm(uun)
            n_vvn = norm(vvn)
            termp = n_uup*n_vvp
            termn = n_uun*n_vvn
            #print "termp",termp
            #print "termn",termn
            #print "S[i]",S[i]
            if (termp >= termn):
                #print "termp >= termn"
                W1temp = sqrt(S[i]*termp)*uup/n_uup
                #print "W1temp",W1temp
                for j in range(0, k):
                    W[j][i] = W1temp[j]
                H1temp = sqrt(S[i]*termp)*vvp.T/n_vvp
                #print "H1temp",H1temp
                for j in range(0, n):
                    H[i][j] = H1temp[j]
                #print "W1temp",
                #print W1temp
                #print "H1temp",
                #print H1temp
                #W[:][i] = sqrt(S[i][i]*termp)*uup/n_uup
                #H[i][:] = sqrt(S[i][i]*termp)*vvp.T/n_vvp
            else:
                #print "termp < termn"
                W1temp = sqrt(S[i]*termn)*uun/n_uun
                #print "W1temp",W1temp
                #print "uun",uun
                for j in range(0, k):
                    W[j][i] = W1temp[j]
                H1temp = sqrt(S[i]*termn)*vvn.T/n_vvn
                #print "H1temp",H1temp
                for j in range(0, n):
                    H[i][j] = H1temp[j]
                #print "W1temp",
                #print W1temp
                #print "H1temp",
                #print H1temp
                #W[:][i] = sqrt(S[i][i]*termn)*uun/n_uun
                #H[i][:] = sqrt(S[i][i]*termn)*vvn.T/n_vvn

    #actually these numbers are zeros
    if (flag==1):
        ArrayAverage = mean(A[:][:])

    #actually these numbers are zeros
    for i in range(0, m):
        for j in range(0, k):
            if (W[i][j]<0.0000000001):
                if (flag==0):
                    W[i][j] = 0
                elif  (flag==1):
                    W[i][j] = ArrayAverage

    for i in range(0, k):
        for j in range(0, n):
            if (H[i][j]<0.0000000001):
                if (flag==0):
                    H[i][j] = 0
                elif (flag==1):
                    H[i][j] = ArrayAverage

    return (W, H)
