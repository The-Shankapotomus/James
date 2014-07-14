from xml.dom import minidom

a = minidom.parse("C:\\temp\\party.xml")

b = a.getElementsByTagName('party')

c = b[0].firstChild.nodeValue

print c 
