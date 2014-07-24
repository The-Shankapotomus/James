#Twisted Imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

#Standard Imports
from random import randint 
import linecache
import time
from ConfigParser import ConfigParser

class Playground:
    
    def process(self, message):
        
        rval = None
        badWords = open('Prompts\\badWords.txt', 'r')
        promptList = open('Prompts\\promptList.txt', 'r')
        
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
                    
                    self.physicalTask()
                    rval = 'phyTask'
                    break
                """
                elif i == 3:
                    #add task
                    
                elif i == 4
                    #add task
                
                elif i == 5
                    #add task
                """
        badWords.close()
        promptList.close()          
        return rval
    
    def chat(self, user, origMsg, nick):
        
        m= origMsg.replace(nick, '')
        message = " ".join(m.split())
        msg = ""
        
        symbols = open('Prompts\\symbols.txt', 'r')
        
        for char in symbols:
            
            if char.rstrip('\n') in message:
                
                msg = message.replace(char.rstrip('\n'), "")
                message = " ".join(msg.split())
                
        symbols.close() 
        
        script = ConfigParser()
        script.read("Prompts\\chatScript.ini")
        
        sections = script.sections()
        response = ""
        
        for section in sections:
            
            for option in script.options(section):

                val = script.get(section, option)
                
                # 'in' or '==' dont know how to handle perfectly just yet
                if val == message:
                    
                    response = self.respond(section)
                
        if response == "":
            
            response = self.respond('unknown')
            
        return response
                
    def respond(self, section):
        
        script = ConfigParser()
        script.read("Prompts\\responseScript.ini")
        
        i = randint(1, len(script.options(section)))
        response = script.get(section, str(i))
             
        return response
           
    def mathQuestion(self):

        cache = open('Locale\\cache.txt', 'a')
        
        i = randint(1, 10)
        
        question = "Solve this to get a flag: " + linecache.getline('Challenges\\mathQuestions.txt', i)
        answer = linecache.getline('Challenges\\mathAnswers.txt' , i)
        
        cache.write(question)
        cache.write(answer)
        cache.close()
        
    def physicalTask(self):
        
        cache = open('Locale\\cache.txt', 'a')
        
        i = randint(1,5)
        
        question = "Do the task within 5 minutes. Josh or Fox will give you a flag once its done. Task: " + linecache.getline('Challenges\\phyTasks.txt', i)
        answer = 'Manual'
        
        cache.write(question)
        cache.write(answer)
        cache.close()
        
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
        
        #eggList = open('eggList.txt', 'r')
        queue = open('Locale\\queue.txt', 'r')
        eggStatus = []
        
        for task in queue:
                
                if task == 'Manual':
                    
                    eggStatus.extend([user, "Finish the job to get the egg."])
                    self.removeTask(task)
                    break
                
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