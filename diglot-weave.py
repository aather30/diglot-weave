import googletrans
import time
import re
import sys

#getting correct command line parameters
if len(sys.argv) != 6:
    print('Run the program with such parameters: "python diglot-weave.py <list.txt> <gameofthrones.txt> <es> <5> <10>')
    exit()

argv = sys.argv[1:]

#reading list of words from a file and converting the list in an array
wordList = open(argv[0], 'r').read().split('\n')
#removing the last character from the array
wordList.pop()

#reading the file that has to be translated
inputText = open(argv[1], 'r').read()
inputTextArray = inputText.split(' ')
inputTextArray.append(" ")

translatedTextArray = inputTextArray

#method which checks if the neighbours of the current word from the input file are translated or not
def checkNeighbourhood(current):
    temp = current
    
    #checking neighbourhood backwards
    currentWord = re.sub('[^A-Za-z0-9.]+', '', inputTextArray[current]).lower()
    
    while((currentWord in translatedWords and current > 0) ):
        current -= 1
        if(inputTextArray[current] == "#"):
            current-=1
        currentWord = re.sub('[^A-Za-z0-9.]+', '', inputTextArray[current]).lower() 
        
    backPointer = current + 1 if current !=temp else current
    current = temp
    
    #checking neighbourhood forwards
    currentWord = re.sub('[^A-Za-z0-9.]+', '', inputTextArray[current]).lower()
    
    while(currentWord in translatedWords and current< len(inputTextArray) - 1):
        current += 1
        
        if(inputTextArray[current] == "#"):
            current+=1
            
        currentWord = re.sub('[^A-Za-z0-9.]+', '', inputTextArray[current]).lower()  
        
    frontPointer = current
    
    if currentWord.replace('.', '') in translatedWords:
        frontPointer += 1
        
    phrase = ' '.join(inputTextArray[backPointer: frontPointer])
    
    return backPointer, frontPointer, phrase

#method which takes in the text to be translated, calls the API and returns the translated text
def translate(text):
    #adding a wait of 2 seconds to ovoid exceeding translation limit
    time.sleep(0.2)
    
    #translating the text into given language
    translator = googletrans.Translator()
    #'des' equals to the language in which the text has to be translated
    translatedText = translator.translate(text, src='en', dest=argv[2]).text
    
    return translatedText

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
    
    #Optimization 2   
    dictFlag = True

    i = skippedWords
    while i < len(inputTextArray):    
 
        if word == re.sub('[^A-Za-z0-9]+', '', inputTextArray[i]).lower():

            if dictFlag:
                dictionary[word] = translate(word)
                dictFlag = False


            backPointer, frontPointer, phrase = checkNeighbourhood(i)  

            translatedPhrase = ''

            if frontPointer - backPointer == 1:
                translatedPhrase = re.sub('[A-Za-z0-9]+', dictionary[word], phrase)
            else:
                translatedPhrase = translate(phrase)
            
            translatedStr = ' '.join(translatedTextArray)    
            
            #[11,12,13]
            insertStrArray = translatedPhrase.split(" ")

            #removal
            translatedTextArray = translatedTextArray[0:backPointer] + translatedTextArray[frontPointer:]
            
            #insertion
            for insertWord in insertStrArray[::-1]:
                translatedTextArray.insert(backPointer, insertWord)
            
            translatedStr = ' '.join(translatedTextArray)    

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
        
    if headStart < 1:
        printArray = translatedStr.replace('# ', '').split(' ')
        
        printStr = ' '.join(printArray[skippedWords:skippedWords+int(argv[4])])

        if printStr != '':
            print(printStr + ' ', end='')
        skippedWords += int(argv[4])
        
    headStart -= 1
    
    if(headStart >= 0):
        print(headStart)

f = open('translatedText.txt', 'w')
print("\nFinal String:")
print(translatedStr.replace('# ', ''))
f.write('' + translatedStr.replace('# ', ''))