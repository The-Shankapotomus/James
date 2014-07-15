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

    def __init__(self, nickname, swings):
        
        self.swings = swings
        self.nickname = nickname
        
    #Creates and sets a new nickname 
    def setNick(self, nickname):
        
       nickname = self.nickname
       irc.IRCClient.setNick(self, nickname)
       
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
        
        tasks = self.swings.checkQueue(user, msg, channel)
        if tasks:
            self.msg(tasks[0], tasks[1])
        else:
            pass
        
        command = self.swings.process(msg)
        
        if(command == 'nimc'):
            
            self.kick(channel, user, command)
            
        elif(command == 'mathQ'):
            
            vals = self.swings.openCache()
            
            self.msg(user, vals[0])

            self.swings.addTask(vals[1], user)

            self.swings.clearCache()
        
        if msg.startswith(self.nickname + ": "):
            
            self.msg(channel, ("Hello " +user +"! I'm FlagBot!"))
            
        elif msg.startswith("all: "):
            
            self.msg(channel, "I'm FlagBot!")
            
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
        
        
class FlagBotFactory(protocol.ClientFactory):
    
    #Constructor for FlagBotFactory
    def __init__(self, channel, nick, reactor):
        
        self.channel = channel
        self.nickname = nick
        self.reactor = reactor
        self.bot = None
        
    #Sets up bot with reactory and factory initalization
    def buildProtocol(self, addr):
        
        self.seesaw = Playground()
        self.bot = FlagBot(self.nickname, self.seesaw)
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
