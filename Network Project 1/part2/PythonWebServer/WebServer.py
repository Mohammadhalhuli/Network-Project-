import socket
import re
import os
def decideType(request, reqType):
    words = request.split(' ')
    if(re.match(words[1],'/') or re.match(words[1],'/en')):
        reqType[0] = True
        print("sending english webpage...")
    elif(re.match(words[1],'/ar')):
        reqType[1] = True
        print("sending arabic webpage...")
    elif(re.match(words[1],'/go') or re.match(words[1],'/cn') or re.match(words[1],'/bzu')):
        reqType[3] = True
        print("sending redirect...")
    elif(re.search('.',words[1])):
        files = os.listdir('.')
        exists=False
        words[1]=words[1][1:]
        for i in files:
            if(re.match(i,words[1])):
                exists=True
                break
        if (not(exists)):
            print("requested file doesn't exist")
            return 
        filetype=words[1].split('.')[1]
        if (re.match(filetype,'html')):
            reqType[2] = True
            print("sending html file")
        elif (re.match(filetype,'css')):
            reqType[2] = True
            print("sending css file")
        elif (re.match(filetype,'png')):
            reqType[2] = True
            print("sending png image")
        elif (re.match(filetype,'jpg')):
            reqType[2] = True
            print("sending jpg image")
        else:
            print("file type is not supported")
    else:
        print("request format not recognized")
        print("sending 404 error.....")
    return words[1]

def sendPage(connection, en):
    if  (en):
        print("sending english html file")
        file = open("main_en.html", 'r')
    else:
        print("sending arabic html file")
        file = open("main_ar.html", 'r')

    data = file.read()
    connection.send(b'HTTP/1.0 200 OK\r\n\r\n')
    connection.send(data.encode())
    file.close()

def sendFile(name,connection):
    print("sending " + name)
    file=open(name,'rb')
    data=file.read()
    connection.send(data)
    file.close()
def redirect(name,connection):
    print("sending html redirect")
    if (re.match(name, '/go')):
        sendFile("google.html",connection)
    elif (re.match(name, '/cn')):
        sendFile("CNN.html", connection)
    elif (re.match(name, '/bzu')):
        sendFile("BZU.html", connection)
    else:
        error404(connection)
def error404(connection):
    print("sending error404")
    connection.send(b'HTTP/1.0 404 Not Found\r\n\r\n')
    sendFile("error404.html", connection)
def main():    
    s = socket.socket()
    print("socket successfully created\n")
    port=9000
    reqType=[False,False,False,False]     #this is an array to decide the request type; webpag english, arabic, file, redirect
    s.bind(('',port))
    s.listen(5)
    reqcounter=0
    while True:
        connection,addr = s.accept()
        request = connection.recv(1024).decode()
        print ("----------------------------------------")
        print(request)
        print ("----------------------------------------")
        if (not(request)):
            print("empty request")
        reqcounter+=1
        word = decideType(request,reqType)
        if (reqType[0] or reqType[1]):
            sendPage(connection, reqType[0])
        elif(reqType[2]):
            connection.send(b'HTTP/1.0 200 OK\r\n\r\n')
            sendFile(word, connection)
        elif(reqType[3]):
            connection.send(b'HTTP/1.0 307 Temporary Redirect \r\n\r\n')
            redirect(word, connection)
        else:
            error404(connection)

        connection.close()
        reqType = [False, False, False, False]
main()