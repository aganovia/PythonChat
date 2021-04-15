import socket
import sys
import threading
#import tkinter
from tkinter import *
import tkinter.scrolledtext
from tkinter import simpledialog
#from PIL import ImageTk, Image

# A simple P2P chat program between two peers.
# Adapted from code by NeuralNine.
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
        
        #gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        
        #gui_thread.start()
        receive_thread.start()
        self.gui_loop()
        
        
    def gui_loop(self):
        #self.win = tkinter.Tk()
        #self.win = Tk()
        self.win = tkinter.Toplevel()
        self.win.configure(bg="#A4C1DB")
        self.win.title("Chatroom")
        
        self.chat_label = tkinter.Label(self.win, text="Chat", bg="#A4C1DB")
        self.chat_label.config(font=("Arial", 16))
        self.chat_label.grid(row=0, column=0)
        
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win, font=("Arial", 12))
        self.text_area.grid(row=1, column=0)
        self.text_area.config(state='disabled')
        
        # area that displays an emoji image
        self.emoji_label = tkinter.Label(self.win, text="Your friend sent you:", font=("Arial", 12), bg="#A4C1DB")
        self.emoji_label.grid(row=2, column=0)

        # load up the images
        self.blank_image = tkinter.PhotoImage(file='no-emoji.png')
        self.smiling_image = tkinter.PhotoImage(file='face-smiling.png')
        self.frowning_image = tkinter.PhotoImage(file='frowning-face.png')
        self.joy_image = tkinter.PhotoImage(file='tears-of-joy.png')
        self.tear_image = tkinter.PhotoImage(file='smiling-tear.png')
        
        # set image as blank by default
        self.image_label = tkinter.Label(self.win, image=self.blank_image)
        self.image_label.grid(row=3, column=0)
        
        # message label
        self.msg_label = tkinter.Label(self.win, text="Message", bg="#A4C1DB")
        self.msg_label.config(font=("Arial", 16))
        self.msg_label.grid(row=4, column=0)
        
        # input area
        self.input_area = tkinter.Text(self.win, height=3, font=("Arial", 12))
        self.input_area.grid(row=5, column=0)
        
        # emoji buttons
        
        self.smile_button = tkinter.Button(self.win, text=":^)", command= lambda: self.send_emoji("smile"))
        self.smile_button.config(font=("Arial", 16))
        self.smile_button.grid(row=6, column=0)
        
        # frame for send and exit buttons
        self.sendexit_frame = tkinter.Frame(self.win, bg="#A4C1DB")
        self.sendexit_frame.grid(row=7, column=0)

        self.send_button = tkinter.Button(self.sendexit_frame, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 16))
        self.send_button.pack(padx=20, pady=5, side = LEFT)
        
        self.exit_button = tkinter.Button(self.sendexit_frame, text="Exit", command= self.stop)
        self.exit_button.config(font=("Arial", 16))
        self.exit_button.pack(padx=20, pady=5, side = RIGHT)
        
        # finish GUI and run it
        
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
        
        self.image_label.config(image=self.blank_image)
            
    def send_emoji(self, emoji):
        self.sock.send(emoji.encode('utf-8'))
        print("Emoji sent")
        
        # TODO update emoji display for this screen?
        
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        sys.exit(0)
        
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        if message == "smile":
                            print("Smile received") #TODO delete later
                            self.image_label.config(image=self.smiling_image)
                        else:
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
