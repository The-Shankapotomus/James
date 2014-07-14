#Twisted Imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

#Standard Imports
import time
import sys
import string
import random

#Playgorund Import
from playground import Playground

log.startLogging(sys.stdout)

class FlagBot(irc.IRCClient):
    
    def __init__(self, swings):
        
        self.swings = swings
        
    #Creates and sets a new nickname 
    def setNick(self, nickname):
        
        nickname = self.id_generator()
        irc.IRCClient.setNick(self, nickname)
        
    
    #Generates a random id for bots
    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        
        return ''.join(random.choice(chars) for x in range(size))
      
    #Called once connection is established
    def connectionMade(self):
        
        irc.IRCClient.connectionMade(self)
        print "Connection Established with Network."
    
    #Called if connection is severed
    def connectionLost(self, reason):
        
        irc.IRCClient.connectionLost(self, reason)
        print "Connection Severed."
        
    #Called once bot is in a channel
    def joined(self, channel):
        
        print("[I have joined %s]" %channel)
        
    #Called once bot is in a server
    def signedOn(self):
        
        print "Connection Established with Server."
        nick = self.nickname
        self.nickChanged(nick)
        self.join(self.factory.channel)
        
    #Called when nickname has been changed
    def nickChanged(self, nick):
        
        irc.IRCClient.nickChanged(self, nick)
        print "[New Nick: %s]" %nick
    
    #Called to alter a nickname if name already exists
    def alterColliededNick(self, nickname):
        
        return nickname + '^'
    
    #Called when private message is recieved
    def privmsg(self, user, channel, msg):
        
        origMsg = msg
        
        user = user.split('!', 1)[0]
        print ("<%s> %s" %(user, msg))
        
        self.checkQueue(user, msg, channel)
        command = self.swings.process(msg)
        
        if(command == 'nimc'):
            
            self.kick(channel, user, command)
            
        elif(command == 'mathQ'):
            
            vals = self.openCache()
            
            self.msg(user, vals[0])
            self.msg(user, vals[1])
        
            self.addTask(vals[2], user)
            print vals[2]
            queue = open('queue.txt', 'r')
            x = queue.readlines()
            print x
            self.clearCache()
        
        if msg.startswith(self.nickname + ": "):
            
            self.say(("Hello " +user +"! I'm FlagBot!"), channel)
            
        elif msg.startswith("all: "):
            
            self.say("I'm FlagBot!", channel, user)
            
    #Send a message to current channel
    def say(self, m, channel):
        
        irc.IRCClient.say(self, channel, m)
    
    def msg(self, user, message, length = None):
    
        irc.IRCClient.msg(self, user, "%s" %(message))
        
    #Bounces back into channel after being kicked
    def kickedFrom(self, channel, kicker, message):
        
        print "\nKicked From: " + channel + "\nKicked by: " + kicker + "\nReason: " + message
        self.join(channel)
        msg = self.nickname + " denied your kick. Get on my lvl m8."
        self.say(msg, channel, kicker)
        print("[Attempting to rejoin %s]" %channel)
    
    #Kicks user on prompt and pms them with a message
    def kick(self, channel, user, reason = None):
        
        if(reason == 'nimc'):
            self.say("No cursing in my channel, you lil' fucking cunt.", channel)
            
        irc.IRCClient.kick(self, channel, user, reason)
        
    def openCache(self):
        
        cache = open('cache.txt', 'r')
        
        vals = []
        
        for line in cache:
            
            vals.append(line)
            
        return vals
    
    def clearCache(self):
    
        open('cache.txt', 'w').close()
        
    def addTask(self, task, user = None):
        
        queue = open('queue.txt', 'a')
        
        queue.write(user + ' ' + task)
        
    def removeTask(self, task):
        
        vals = self.getQueue()
        queue = open('queue.txt', 'w')
        print vals
        for line in vals:
            
            if line == task:
                
                print ("Task (" + task + ") removed from queue.")
                
            elif line != task:
                
                queue.write(line)
        
        queue.close()
        
    def getQueue(self):
        
        queue = open('queue.txt', 'r')
        vals = queue.readlines()
        print vals
        queue.close()
        
    def clearQueue(self):
        
        open('queue.txt', 'w').close()
        
    def checkQueue(self, user, msg, channel):
        
        queue = open('queue.txt', 'r')
        
        for task in queue:
            
            try:
            
                if user in task and msg in task:

                    self.msg(user, "Good Job, egg egg")
                    self.removeTask(task)
                    print "Egg given to: " +user
                    break
                
                elif user in task and msg not in task:

                    self.msg(user, "Sorry charlie,")
                    self.removeTask(task)
                    break
                    
            except IndexError:
                
                pass
        
class FlagBotFactory(protocol.ClientFactory):
    
    #Constructor for FlagBotFactory
    def __init__(self, channel, reactor):
        
        self.channel = channel
        self.reactor = reactor
        self.bot = None
        
    #Sets up bot with reactory and factory initalization
    def buildProtocol(self, addr):
        
        self.seesaw = Playground()
        self.bot = FlagBot(self.seesaw)
        self.bot.factory = self
        self.bot.reactor = self.reactor
        
        return self.bot
    
    #Called if the client losses connection to server
    def clientConnectionLost(self, connector, reason):
        
        print "Connection Lost: " + str(reason)
        connector.connect()
    
    #Called if the client fails to connec to server
    def clientConnectionFailed(self, connector, reason):
        
        print "Connection Failed: " + str(reason)        