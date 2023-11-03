#Client
from socket import * 
from threading import *
from tkinter import *

from tkinter import filedialog

client = socket(AF_INET, SOCK_STREAM)

ip = '10.100.5.221'
port = 55555

client.connect((ip, port))

pencere = Tk()
pencere.title('Bağlandı :' + ip + ":" + str(port))

messages = Text(pencere, width=50)
messages.grid(row=0, column=0, padx=10, pady=10)

yourMessage = Entry(pencere, width=50)
yourMessage.insert(0, 'Isminiz')
yourMessage.grid(row=1, column=0, padx=10, pady=10)
yourMessage.focus()
yourMessage.selection_range(0, END)

def sendFile():
    file_path = filedialog.askopenfilename()  
    if file_path:  
        with open(file_path, "rb") as file:
            file_data = file.read()
            client.sendall(file_data) 
            messages.insert(END, '\nDosya gönderildi: ' + file_path)

bsendFile = Button(pencere, text="Dosya Seç ve Gönder", width=20, command=sendFile)
bsendFile.grid(row=2, column=1, padx=5, pady=10)

def onEnter(event):
    sendMessage()

yourMessage.bind("<Return>", onEnter)

def sendMessage():
    clientMessage = yourMessage.get()
    messages.insert(END, '\n' + 'Sen: ' + clientMessage)
    client.send(clientMessage.encode('utf8'))
    yourMessage.delete(0, END)

bmessageGonder = Button(pencere, text='Gönder', width=20, command=sendMessage)
bmessageGonder.grid(row=2, column=0, padx=10, pady=10)

def recvMessage():
    while True:
        serverMessage = client.recv(1024).decode('utf8')
        messages.insert(END, '\n' + serverMessage)

recvThread = Thread(target=recvMessage)
recvThread.daemon = True
recvThread.start()

pencere.mainloop()