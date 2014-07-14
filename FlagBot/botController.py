#Twisted Imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

#Standard Imports
from xml.dom import minidom

#Bot Factory Import
from flagBot import FlagBotFactory

class Command:
    
    #Constructor for Command and Control class
    def __init__(self, reactor):
        
        setup = self.settings()
        
        self.factory = FlagBotFactory(str(setup['Channel']), str(setup['Nickname']), reactor)
        reactor.connectTCP(setup['Server'], int(setup['Port']) , self.factory)
    
    #Imports settings from an XML file
    def settings(self):
        
        presets = minidom.parse("Locale\\settings.xml")

        values = {'Nickname': None, 'Server': None, 'Port': None, 'Channel': None}
        
        for key in values:
            
            val = presets.getElementsByTagName(key)
            values[key] = val[0].firstChild.nodeValue
        
        return values
    
if __name__ == "__main__":
    
    alpha = Command(reactor)
    reactor.run()
