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
        
    def getQueue(self):
        
        queue = open('Locale\\queue.txt', 'r')
        vals = queue.readlines()
        
        queue.close()

        return vals
        
    def clearQueue(self):
        
        open('Locale\\queue.txt', 'w').close()
        
    def clearCache(self):
    
        open('Locale\\cache.txt', 'w').close()
        
    def openCache(self):
        
        cache = open('Locale\\cache.txt', 'r')
        
        vals = []
        
        for line in cache:
            
            vals.append(line)
        
        cache.close() 
          
        return vals
    
    def addTask(self, task, user = None):
        
        queue = open('Locale\\queue.txt', 'a')
        
        queue.write(user + ' ' + task)
        
        print ("[Task '%s %s' added to queue.]" % (user, task.rstrip('\n')) )
        
        queue.close()
        
    def removeTask(self, task):

        vals = self.getQueue()
        queue = open('Locale\\queue.txt', 'w')

        for line in vals:
            
            if line == task:
                
                print ("[Task '%s' removed from queue.]" % task.rstrip('\n'))
                
            elif line != task:
                
                queue.write(line)
        
        queue.close()
        
    def checkQueue(self, user, msg, channel):
        
        queue = open('Locale\\queue.txt', 'r')
        eggStatus = []
        
        for task in queue:
            
                if user in task and msg in task:

                    eggStatus.extend([user, "Good Job. Egg here."])
                    self.removeTask(task)
                    print ("[Egg given to: %s]" %user)
                    break
                
                elif user in task and msg not in task:

                    eggStatus.extend([user, "Sorry charlie."])
                    self.removeTask(task)
                    break
                
                else:
                    pass
                
        queue.close()
                
        return eggStatus

        

        
