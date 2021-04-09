import socket
import sys
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

# A simple P2P chat program between two peers.
#
# Amela Aganovic
# CIS 457
# W2021

HOST = '127.0.0.1'
PORT = 1234

class Client:

    def __init__(self, host, port):
    
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # 2nd peer code
            self.sock.connect((host, port))
        except:
            # 1st peer code
            print("Waiting for friend to connect...")
            self.sock.bind((HOST, PORT))
            self.sock.listen()
            peer, address = self.sock.accept()
            self.sock = peer
        
        msg = tkinter.Tk()
        msg.withdraw()
        
        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)
        
        self.gui_done = False
        self.running = True
        
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        
        gui_thread.start()
        receive_thread.start()
        
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="#A4C1DB")
        self.win.title("Chatroom")
        
        self.chat_label = tkinter.Label(self.win, text="Chat", bg="#A4C1DB")
        self.chat_label.config(font=("Arial", 16))
        self.chat_label.pack(padx=20, pady=5)
        
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win, font=("Arial", 12))
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')
        
        self.msg_label = tkinter.Label(self.win, text="Message", bg="#A4C1DB")
        self.msg_label.config(font=("Arial", 16))
        self.msg_label.pack(padx=20, pady=5)
        
        self.input_area = tkinter.Text(self.win, height=3, font=("Arial", 12))
        self.input_area.pack(padx=20, pady=5)
        
        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 16))
        self.send_button.pack(padx=20, pady=5)
        
        self.exit_button = tkinter.Button(self.win, text="Exit", command=self.stop)
        self.exit_button.config(font=("Arial", 16))
        self.exit_button.pack(padx=20, pady=5)
        
        self.gui_done = True
        
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        
        self.win.mainloop()
        
    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')
        
        self.text_area.config(state='normal')
        self.text_area.insert('end', message)
        self.text_area.yview('end')
        self.text_area.config(state='disabled')
        
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)
        
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break
                
client = Client(HOST, PORT)
