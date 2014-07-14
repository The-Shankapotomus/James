badWords = open('C:\\temp\\badWords.txt', 'r')
x = "fuck your mother"
for word in badWords:
    print word
    if word in x:
        print "it worked"
