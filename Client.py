from socket import *
from select import *
from tkinter import *
from tkinter.ttk import *
import threading
import sys

def GUI():
    def ubah_nama():
        def ubah():
            if len(entri.get())>0:
                nama_klien.insert(0, entri.get()+"\n")
                messagebox.showinfo("Pemberitahuan","Nama berhasil diubah")
            else:
                messagebox.showwarning("Pemberitahuan","Nama tidak boleh kosong")
        top = Toplevel()
        entri = Entry(top, width = 50)
        entri.pack()
        Button(top, text = "Ubah", command = ubah).pack()
        top.mainloop()
        
    def keluar():
        sock.close()
        sys.exit()
        #root.destroy()        
    def kirim():
        data = ent_penerima.get()+": "+entri.get()
        if len(data)>0:
            b = sock.send(str.encode(data+"\n"))
        text.insert(END, data+"\n")
        text.see(END)
    def pilih_chat(event):
        pilih=lbox.curselection()
        value = lbox.get(pilih[0])
        ent_penerima.delete(0, END)
        ent_penerima.insert(0, value)
    def tutup():
        data = "_keluar_"
        b = sock.send(str.encode(data+"\n"))
        sock.close()

    global text, lbox
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", tutup)

    #----------------------------------------------------------------------------------------
    scrollbar = Scrollbar(root, orient=VERTICAL)
    scrollbar.grid(row=0, column=1, sticky=NS)
    #----------------------------------------------------------------------------------------
    frame = Canvas(root, yscrollcommand=scrollbar.set)
    frame.grid(row=0, column=0)
    scrollbar.config(command=frame.yview)
    frame2 = Frame(root)
    frame2.grid(row=1, column=0)
    frame3 = Frame(root)
    frame3.grid(row=2, column=0)
    lbox = Listbox(frame3, width=45, height=15)
    lbox.grid(row=1, column=0, padx=10, pady=3)
    lbox.bind("<Double-Button-1>", pilih_chat)
    text = Text(frame, width = 40, height = 20)
    text.grid()
    ent_penerima = Entry(frame2)
    ent_penerima.grid(row=0, column=0)
    entri = Entry(frame2, width = 15)
    entri.grid(row=0, column=1)
    Button(frame2, text = "Kirim", command = kirim).grid()
    Button(frame2, text = "Keluar", command = keluar).grid()
    ent_get = entri.get()

    menubar = Menu(root)
    file = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="User", menu = file)
    file.add_command(label = "Hapus percakapan")
    file.add_command(label = "Tinggalkan percakapan")
    file.add_command(label = "Ubah nama pengguna", command = ubah_nama)
    file.add_separator()
    file.add_command(label = "Keluar")

    nama_klien = ["Klien 1 \n"]
    
    root.config(menu = menubar)
    root.mainloop()

pro = threading.Thread(None, GUI)
pro.setDaemon(1)
pro.start()

HOST = "localhost"
PORT = 33110

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((HOST, PORT))


while(True):
    read, write, error = select([sock],[],[],1)
    if(len(read)):
        try:
            #pass#sock.send(str.encode("test"))
            data = bytes.decode(sock.recv(1024))
            if data[0] != "[":
                text.insert(END, data+"\n")
                text.see(END)
            else:
                lbox.delete(0,END)
                a = -2
                for i in range(len(data)//3):
                    a+=3
                    lbox.insert(END, data[a] )
	            	
        except:
            sys.exit()
    #pesan = input("Masukan pesan: ")
    #sock.send(str.encode(pesan))
    #data = bytes.decode(sock.recv(1024))
                
