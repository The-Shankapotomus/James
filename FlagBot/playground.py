#Twisted Imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

#Standard Imports
from random import randint 
import linecache

class Playground:
    
    def process(self, message):
        
        rval = None
        badWords = open('Prompts\\badWords.txt', 'r')
        promptList = open('Prompts\\promptList.txt', 'r')
        #eggList = open('eggList.txt', 'r')
        #chatScript = open('chatScript', 'r')
        
        #Check if someone curses
        for word in badWords:
    
            if word.rstrip('\n') in message:
                
                rval = 'nimc'
                break
    
        #Check if someone asks for a flag
        for prompt in promptList:
            
            if prompt.rstrip('\n') == message:
            
                i = randint(1,2)
                
                if i == 1:
                    
                    self.mathQuestion()
                    rval = 'mathQ'
                    break
                
                elif i == 2:
                    
                    self.mathQuestion()
                    rval = 'mathQ'
                    break
                    
        return rval
            
    def mathQuestion(self):

        cache = open('Locale\\cache.txt', 'a')
        
        i = randint(1, 10)
        
        question = "Solve this to get a flag: " + linecache.getline('Challenges\\mathQuestions.txt', i)
        answer = linecache.getline('Challenges\\mathAnswers.txt' , i)
        
        cache.write(question)
        cache.write(answer)
        
