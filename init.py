#!/usr/local/myapp2.7/bin/python

import requests, json, string, random
from lxml import html

url = 'https://strikingly-hangman.herokuapp.com/game/on'
getResult = {"sessionId":"a2c4d988f62c18f6c08ea53016afdea6", "action":"getResult"}
headers = {'content-type': 'application/json'}
l = []
lr = []

def NextWord():
    nextWord = {"sessionId":"a2c4d988f62c18f6c08ea53016afdea6", "action":"nextWord"}
    r =  requests.post(url, data=json.dumps(nextWord), headers=headers)
#    print r.json()["data"]["word"]
#    print r.json()["data"]["wrongGuessCountOfCurrentWord"]
    return r

def GuessWord():
    ranLetter = random.choice(string.ascii_uppercase)
    while True:
        if ranLetter in l:
           ranLetter = random.choice(string.ascii_uppercase)
        else:
           l.append(ranLetter)
           break
    guessWord = {"sessionId":"a2c4d988f62c18f6c08ea53016afdea6", "action":"guessWord", "guess":ranLetter}
    r = requests.post(url, data=json.dumps(guessWord), headers=headers)
    print l
    return r

def SearchWeb(word):
    str = word.replace("*", "-")
    url = 'http://www.morewords.com/'
    payload = {str:''}
    r = requests.get(url, params=payload)
    tree = html.fromstring(r.content)
    result = tree.xpath('/html/body/div/big/ul/li/a/text()')
    searchList = [ x.upper() for x in result ]
#    l1 = l[0:1]
    if l:
        for item in l:
            middleList = [ x for x in searchList if not item  in x ]
            searchList = middleList
    return searchList

def SearchWeb2(word):
    str = word.replace("*", "-")
    url = 'http://www.morewords.com/'
    payload = {str:''}
    r = requests.get(url, params=payload)
    tree = html.fromstring(r.content)
    result = tree.xpath('/html/body/div/h2/text()')
    searchList = [ x.upper() for x in result ]
    return searchList

def GuessList(SW, word, wrongCount):
    if (word.find('*') != -1):
        index = word.find('*')
        for x in SW:
            t = x[index]
            if t not in lr:
                guessList = {"sessionId":"a2c4d988f62c18f6c08ea53016afdea6", "action":"guessWord", "guess":t}
                break
            else:
                continue
#        guessList = {"sessionId":"d757441c2bccbcea7ed6e48506c195a7", "action":"guessWord", "guess":t}
        r = requests.post(url, data=json.dumps(guessList), headers=headers)
        word = r.json()["data"]["word"]
        n1 = wrongCount
        n2 = r.json()["data"]["wrongGuessCountOfCurrentWord"]
        print "n1 is " + str(n1)
        print "n2 is " + str(n2)
        if (n1 == n2) and (n2 < 10): # guess right
            lr.append(t)
#            print "before..."
#            print SW
            SW = SearchWeb(word)
#            print "after..."
#            print SW
            if not SW:
               SW = SearchWeb2(word)
            SW1 = SW
            return GuessList(SW1, word, n2)
        elif (n1 < n2) and (n2 < 10):
            l.append(t)
            print "this is t"
            print t
            print "this is l"
            print l
            SW = SearchWeb(word)
            print SW
            return GuessList(SW, word, n2)
    else:
        GetResult()

def GetResult():
    getResult = {"sessionId":"a2c4d988f62c18f6c08ea53016afdea6", "action":"guessWord"}
    r =  requests.post(url, data=json.dumps(getResult), headers=headers)
    print r.text

def ControlWord():
    n = 1
    NextWord()
    GW = GuessWord()
    print GW.json()["data"]["word"]
    wrongCount = GW.json()["data"]["wrongGuessCountOfCurrentWord"]
    print "wrongCOunt is " + str(wrongCount)
    while n < 10:
        if n == wrongCount:#guess wrong
           GW = GuessWord()
           wrongCount = GW.json()["data"]["wrongGuessCountOfCurrentWord"]
           n = n + 1
        else:# guess right
           t = l.pop()#delete last correct guess
           lr.append(t)
           word = GW.json()["data"]["word"] #string
           SW = SearchWeb(word) #return list
           wrongCount = GW.json()["data"]["wrongGuessCountOfCurrentWord"]
           GuessList(SW, word, wrongCount)
           break

ControlWord()
