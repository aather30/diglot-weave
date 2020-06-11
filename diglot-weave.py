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
wordList = open(argv[0], 'r', encoding="utf8").read().split('\n')
#removing the last character from the array
wordList.pop()

#reading the file that has to be translated
inputText = open(argv[1], 'r', encoding="utf8").read()
inputTextArray = inputText.split(' ')
inputTextArray.append(" ")

translatedTextArray = inputTextArray

#method which checks if the neighbours of the current word from the input file are translated or not
def checkNeighbourhood(current):
    temp = current
    
    #checking neighbourhood backwards
    currentWord = re.sub('[^A-Za-z0-9.,?;:-]+', '', inputTextArray[current]).lower()
    
    while((currentWord in translatedWords and current > 0) ):
        current -= 1
        if(inputTextArray[current] == "#"):
            current-=1
        currentWord = re.sub('[^A-Za-z0-9.,?;:-]+', '', inputTextArray[current]).lower() 
        
    backPointer = current + 1 if current !=temp else current
    current = temp
    
    #checking neighbourhood forwards
    currentWord = re.sub('[^A-Za-z0-9.,?;:-]+', '', inputTextArray[current]).lower()
    
    while(currentWord in translatedWords and current< len(inputTextArray) - 1):
        current += 1
        
        if(inputTextArray[current] == "#"):
            current+=1
            
        currentWord = re.sub('[^A-Za-z0-9.,?;:-]+', '', inputTextArray[current]).lower()  
        
    frontPointer = current
    
    if re.sub('[.,?;:-]+', '', currentWord) in translatedWords:
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
        f = open(argv[5], 'w')
        f.write('' + translatedStr.replace('# ', ''))



#Runner

#making an array to keep track of the translated words
translatedWords = []
#initializing output text str ---
translatedStr = ''

headStart = int(argv[3])
skippedWords = 0

dictionary = {}

for word in wordList:
    #Optimization 1
    if skippedWords > len(inputTextArray):
        break

    translatedWords.append(word)

    print('\nNumber of words left: ')

    i = skippedWords
    while i < len(inputTextArray):    
 
        if word == re.sub('[^A-Za-z0-9]+', '', inputTextArray[i]).lower():

            backPointer, frontPointer, phrase = checkNeighbourhood(i)  

           
            translatedPhrase = ''

            filteredPhrase = re.sub('[^A-Za-z0-9# ]+', '', phrase)
        
            if filteredPhrase not in dictionary:
                dictionary[filteredPhrase] = translate(filteredPhrase)

            translatedPhrase = re.sub('[A-Za-z0-9# ]+', dictionary[filteredPhrase], phrase)
       
            #[11,12,13]
            insertStrArray = translatedPhrase.split(" ")

           

            #removal
            translatedTextArray = translatedTextArray[0:backPointer] + translatedTextArray[frontPointer:]

            #insertion
            for insertWord in insertStrArray[::-1]:
                translatedTextArray.insert(backPointer, insertWord)
            
            translatedStr = ' '.join(translatedTextArray)    
            # print("phrase:",phrase)
            # print("filteredPhrase:",filteredPhrase)
            # print("translatedPhrase:", translatedPhrase)
            # print("insertStrArray:",insertStrArray)
            #print(translatedStr)

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
        
    print()
        
    if headStart < 1:
        printArray = translatedStr.replace('# ', '').split(' ')
        
        printStr = ' '.join(printArray[skippedWords:skippedWords+int(argv[4])])

        if printStr != '':
            print(printStr + '\t\t', end='')
        skippedWords += int(argv[4])
        
    headStart -= 1
    
f = open(argv[5], 'w')
print("\nFinal String:")
print(translatedStr.replace('# ', ''))
f.write('' + translatedStr.replace('# ', ''))