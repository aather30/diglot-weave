import googletrans
import time
import re
import sys

#getting correct command line parameters
if len(sys.argv) != 7:
    print('\nRun the program with such parameters: "python diglot-weave.py <list.txt> <gameofthrones.txt> <es> <5> <10> <translatedFilename>')
    exit()

argv = sys.argv[1:]

#reading list of words from a file and converting the list in an array
phraseList = open(argv[0], 'r', encoding="utf8").read().split('\n')
#removing the last character from the array
phraseList.pop()

#reading the file that has to be translated
inputText = open(argv[1], 'r', encoding="utf8").read()

#making \n as an individual 
inputText = inputText.replace("\n", " \n ")

inputTextArray = inputText.split(' ')
inputTextArray.append(" ")

translatedTextArray = inputTextArray

#method which checks if the neighbours of the current word from the input file are translated or not
def checkNeighbourhood(backPointer, current):
    
    #checking neighbourhood backwards
    
    currentWord = inputTextArray[current].lower() if re.sub('[^A-Za-z0-9]+', '', inputTextArray[current]) != "I" else inputTextArray[current]
    currentWord = re.sub('[^A-Za-z0-9.?]+', '', currentWord)

    #print("current word:", currentWord)
    while((currentWord in translatedWords and current > 0) ):
        current -= 1
        if(inputTextArray[current] == "#"):
            current-=1
        currentWord = inputTextArray[current].lower() if re.sub('[^A-Za-z0-9]+', '', inputTextArray[current]) != "I" else inputTextArray[current]
        currentWord = re.sub('[^A-Za-z0-9.?]+', '', currentWord)

    backPointer = current + 1 if current !=temp else current
    current = temp
    
    #checking neighbourhood forwards
    currentWord = inputTextArray[current].lower() if re.sub('[^A-Za-z0-9]+', '', inputTextArray[current]) != "I" else inputTextArray[current]
    currentWord = re.sub('[^A-Za-z0-9.?]+', '', currentWord)

    while(currentWord in translatedWords and current< len(inputTextArray) - 1):
        current += 1
        
        if(inputTextArray[current] == "#"):
            current+=1
        currentWord = inputTextArray[current].lower() if re.sub('[^A-Za-z0-9]+', '', inputTextArray[current]) != "I" else inputTextArray[current]
        currentWord = re.sub('[^A-Za-z0-9.?]+', '', currentWord)   

    frontPointer = current

    if re.sub('[.?]+', '', currentWord) in translatedWords:
        frontPointer += 1
        
    phrase = ' '.join(inputTextArray[backPointer: frontPointer])
    
    return backPointer, frontPointer, phrase

#method which takes in the text to be translated, calls the API and returns the translated text
def translate(text):
    #adding a wait of 2 seconds to ovoid exceeding translation limit
    #time.sleep()
    
    try:
        #translating the text into given language
        translator = googletrans.Translator()
        #'des' equals to the language in which the text has to be translated
        translatedText = translator.translate(text, src='en', dest=argv[2]).text
        
        return translatedText

    except:
        print("\nThere was an error in connection. We saved the text that was translated uptil this point.\n\n")
        f = open(argv[5], 'w', encoding="utf8", errors="ignore")
        f.write('' + translatedStr.replace('# ', ''))
        exit()



#Runner

#making an array to keep track of the translated words
translatedWords = []
#initializing output text str ---
translatedStr = ''

headStart = int(argv[3])
skippedWords = 0

dictionary = {}

for word in phraseList:

    #Optimization 1
    if skippedWords > len(inputTextArray):
        break
    
    #splitting a phrase into words
    words = word.split(' ') 

    translatedWords.append(word)

    print('\nNumber of words left: ')

    i = skippedWords
    while i < len(inputTextArray):

        phraseFlag = False 
        temp = 0
        backPointer = i
        for j, w in enumerate(words):
            if w == re.sub('[^A-Za-z0-9]+', '', inputTextArray[i]).lower() or (w == re.sub('[^A-Za-z0-9]+', '', inputTextArray[i]) == "I"):
                i+=1
                temp+=1
                
            else:
                i -= temp
                break
            
            if temp == len(words) - 1:
                phraseFlag = True

 
        if phraseFlag:

            backPointer, frontPointer, phrase = checkNeighbourhood(backPointer, i)  

        #edge case for I
        inputWord = inputTextArray[i].lower() if word!="I" else inputTextArray[i]     
        inputWord = re.sub('[^A-Za-z0-9]+', '', inputWord)

        if word == inputWord:
            #print("Input word:", inputWord)

            backPointer, frontPointer, phrase = checkNeighbourhood(i)  
            #print("phrase:",phrase, backPointer, frontPointer)
            
            translatedPhrase = ''
        
            if phrase not in dictionary:
                dictionary[phrase] = translate(phrase).lower()

            translatedPhrase = dictionary[phrase]
            #print("translatedPhrase:", translatedPhrase)
            
            #[11,12,13]
            insertStrArray = translatedPhrase.split(" ")


            #removal
            translatedTextArray = translatedTextArray[0:backPointer] + translatedTextArray[frontPointer:]

            #insertion
            for insertWord in insertStrArray[::-1]:
                translatedTextArray.insert(backPointer, insertWord)
            
            translatedStr = ' '.join(translatedTextArray)    

            # print("translatedPhrase:", translatedPhrase)
            # print("insertStrArray:",insertStrArray)
            # print(translatedStr)

            translatedTextArray = translatedStr.split(' ')
            
            if len(translatedPhrase.split(' ')) > len(phrase.split(' ')):
                diff = len(translatedPhrase.split(' ')) - len(phrase.split(' ')) 
                
                for count in range(diff):
                    inputTextArray.insert(backPointer, '#')
                    i+=1
                    
            elif len(translatedPhrase.split(' ')) < len(phrase.split(' ')):
                diff = len(phrase.split(' ')) - len(translatedPhrase.split(' ')) 
                
                for count in range(diff):
                    translatedTextArray.insert(backPointer, '#')     
         
        i += 1
        
        print(len(inputTextArray) - i,"  ", end='\r')
        
        
    if headStart < 1:
        printArray = translatedStr.replace('# ', '').split(' ')
        
        printStr = ' '.join(printArray[skippedWords:skippedWords+int(argv[4])])

        if printStr != '':
            print(printStr.replace(" \n ", "\n") + '\t\t', end='')
        skippedWords += int(argv[4])
        
    headStart -= 1
    
f = open(argv[5], 'w', encoding="utf8", errors="ignore")
print("\nFinal String:")
print(translatedStr.replace('# ', '').replace(" \n ", "\n"))
f.write('' + translatedStr.replace('# ', '').replace(" \n ", "\n"))