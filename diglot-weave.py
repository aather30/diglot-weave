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
    currentWord = re.sub('[^A-Za-z0-9.,?;:-]+', '', inputTextArray[backPointer]).lower() if re.sub('[^A-Za-z0-9]+', '', inputTextArray[backPointer]) != "I" else "I"
    
    while((currentWord in translatedWords and backPointer > 0) ):
        backPointer -= 1
        if(inputTextArray[backPointer] == "#"):
            backPointer-=1
        currentWord = re.sub('[^A-Za-z0-9.,?;:-]+', '', inputTextArray[backPointer]).lower() if re.sub('[^A-Za-z0-9]+', '', inputTextArray[backPointer]) != "I" else "I"
        
    backPointer = backPointer + 1 if backPointer !=temp else backPointer
    
    #checking neighbourhood forwards
    currentWord = re.sub('[^A-Za-z0-9.,?;:-]+', '', inputTextArray[current]).lower() if re.sub('[^A-Za-z0-9]+', '', inputTextArray[current]) != "I" else "I"
    
    while(currentWord in translatedWords and current< len(inputTextArray) - 1):
        current += 1
        
        if(inputTextArray[current] == "#"):
            current+=1
            
        currentWord = re.sub('[^A-Za-z0-9.,?;:-]+', '', inputTextArray[current]).lower() if re.sub('[^A-Za-z0-9]+', '', inputTextArray[current]) != "I" else "I" 
        
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
        f = open(argv[5], 'w', encoding="utf8", errors="ignore")
        f.write('' + translatedStr.replace('# ', ''))



#Runner

#making an array to keep track of the translated words
translatedWords = []
#initializing output text str ---
translatedStr = ''

headStart = int(argv[3])
skippedWords = 0

dictionary = {}

br = False

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

            translatedPhrase = ''
        
            if phrase not in dictionary:
                dictionary[phrase] = translate(phrase)

            translatedPhrase = dictionary[phrase]
       
            #[11,12,13]
            insertStrArray = translatedPhrase.split(" ")

           

            #removal
            translatedTextArray = translatedTextArray[0:backPointer] + translatedTextArray[frontPointer:]

            #insertion
            for insertWord in insertStrArray[::-1]:
                translatedTextArray.insert(backPointer, insertWord)
            
            translatedStr = ' '.join(translatedTextArray)    
            # print("phrase:",phrase)
            # print("translatedPhrase:", translatedPhrase)
            # print("insertStrArray:",insertStrArray)
            # print(translatedStr)

            translatedTextArray = translatedStr.split(' ')
            # print("translated text array", translatedTextArray)
            # print("f: ", frontPointer)
            # print("b: ", backPointer)
            
            if len(translatedPhrase.split(' ')) > len(phrase.split(' ')):
                diff = len(translatedPhrase.split(' ')) - len(phrase.split(' ')) 
                
                for count in range(diff):
                    inputTextArray.insert(backPointer, '#')
                    i+=1
                    
            elif len(translatedPhrase.split(' ')) < len(phrase.split(' ')):
                diff = len(phrase.split(' ')) - len(translatedPhrase.split(' ')) 
                
                for count in range(diff):
                    translatedTextArray.insert(backPointer, '#')     
        
            if int(frontPointer) == len(inputTextArray):
                br = True
                break
        
        i += 1
        
        if br == True:
            break
        
        print(len(inputTextArray) - i,"  ", end='\r')
        
    print()
        
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