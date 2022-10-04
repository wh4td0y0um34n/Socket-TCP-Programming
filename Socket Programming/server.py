# modules(library) threading dan socket
import threading
import socket

# mensetting host ip dan port untuk server berjalan
host = '127.0.0.1' # kita ambil ip dari localhost
port = 12000 # di sini kita harus berhati-hati untuk tidak memilih papan yang dipesan sehingga untuk menampilkan semua port yang terbuka dengan cara klik bash tulis netstat setelah itu akan muncul ip dan port yang aktif, jadi saya memilih 12000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket (family, type[proto])
server.bind((host, port)) # kita perlu mengikat server ke Host dan port, dan hati-hati di sini perlu meletakkan Tuple di dalam Tuple jika tidak, akan mendapatkan pesan kesalahan
server.listen() # selanjutnya mengaktifkan mode mendengarkan untuk setiap koneksi masuk ke server 
clients = [] # membuat daftar untuk klien yang akan menjadi daftar kosong 
aliases = [] # membuat daftar untuk alias atau nama panggilan 

def broadcast(message): # membuat function untuk mengirim pesan dari server ke client yang terhubung dan dibutuhkan parameter yaitu message 
    for client in clients: # membuat sebuah for loop untuk mengulangi daftar client 
        client.send(message) # client perlu mengirim pesan ini 

def handle_client(client): # membuat function yang menangani koneksi setiap client dengan 1 parameter dengan nama client
    while True: # membuat sebuah while loop 
        try: # membuat sebuah try untuk penerimaan pesan 
            message = client.recv(1024) # dengan jumlah bytes 1024 (maximum)
            broadcast(message) # penyiaran pesan  
        except: # menagkap dari try 
            index = clients.index(client) # index ini akan sama dengan index titik daftar client dan metode index di sini mencari Tuple untuk nilai yang ditentukan dan mengembalikan posisinya dalam kasus kami yaitu clients 
            clients.remove(client) # jika ingin menghapus client asumsikan dengan fungsi remove ()
            client.close() # menutup koneksi dengan client 
            alias = aliases[index] # kita perlu melakukan hal yang sama untuk alias karena kita perlu menghapus alias ini dari klien tertentu dari daftar alias itu dan di sini kami telah menimpa nilai alias itu
            broadcast(f'{alias} has left'.encode('utf-8')) # kami dapat mengirim pesan melalui function broadcast yang mengatakan bahwa alice ini telah meninggalkan ruang obrolan dan jangan lupa untuk menyandikannya karena kita tidak ingin mengirim pesan semacam ini yang dalam bentuk string tidak akan berfungsi kita perlu mengirimnya dalam bentuk byte itulah mengapa kita perlu menyandikan kode 
            aliases.remove(alias) # dan kita perlu menghapus alias itu
            break # berhenti 

def receive(): # main function untuk menerima koneksi dari client 
    while True: # while loop 
        print('Server is running and listening ...') # mulai dengan pesan server sedang running dan listening 
        client, address = server.accept() # server siap menerima koneksi masuk apapun sehingga kita akan mengatur client di alamat server 
        print(f'Connection is established with {str(address)}') # pesan untuk mengatakan bahwa koneksi sedang dibuat dan kami akan mengembalikan alamatnya 
        client.send('alias?'.encode('utf-8')) # mengirimkan pesan kepada client untuk memberi tahu nama client tersebut dengan sebutan alias 
        alias = client.recv(1024) # untuk menerima informasi berdasarkan dari client 
        aliases.append(alias) # untuk mengambil atau menambahkan alias ke daftar list alias 
        clients.append(client) # untuk mengambil atau menambahkan client ke daftar list client
        print(f'The alias of this client is {alias}'.encode('utf-8')) # untuk menampilkan pesan di server dan mengembalikan kepada client 
        broadcast(f'{alias} has connected'.encode('utf-8')) # untuk menampilkan pesan di server bahwasannya alamat ip dan port client sudah terhubung ke dalam server 
        client.send('You are now connected'.encode('utf-8')) # untuk memberikan pesan kepada client bahwa client sudah terkoneksi dengan server  
        thread = threading.Thread(target = handle_client, args=(client,)) # pemanggilan perintah thread untuk function handle_client 
        thread.start() # start function dari thread 
if __name__ == "__main__": # pemanggilan function receive 
    receive()