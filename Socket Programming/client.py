# modules(library) threading dan socket
import threading
import socket

alias = input('Choose an aliass >>>') # client menginputkan nama atau alias client 
client= socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ocket (family, type[proto])
client.connect(('127.0.0.1', 12000)) # mengikat client dengan server dan bisa dihubungkan dengan servver 

def client_receive(): # function untuk menerima pesan dari other client 
    while True: # while loop 
        try: # method try 
            message = client.recv(1024).decode('utf-8') # unutk menerima pesan 
            if message == "alias?": # jika object message = alias yang telah didefinisikan di dalam server 
                client.send(alias.encode('utf-8')) # client .send merupakan input di sini 
            else : 
                print(message) # menampilkan pesan 
        except: # method except untuk menangani segala eror yang ada di try  
            print('Error!') # jika terjadi eror maka akan mucul pesan Error!  
            client.close() # untuk menutup connection dari client 
            break # break 

def client_send(): # function untuk mengirim pesan 
    while True: # while loop 
        message = f'{alias}: {input("")}' # untuk menginputkan pesan yang ingin disampaikan kepada different person di dalam server 
        client.send(message.encode('utf-8')) # client .send merupakan input disini 

receive_thread = threading.Thread(target = client_receive) # pemanggilan perintah thread untuk function client_receive yang berarti menerima pesan  
receive_thread.start() # start function dari thread 

send_thread = threading.Thread(target = client_send) # pemanggilan perintah thread untuk function client_receive yang berarti menerima pesan 
send_thread.start() # start function dari thread