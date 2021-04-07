import socket
import select
import errno
import time
from tkinter import *
from tkinter.scrolledtext import ScrolledText

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
#my_username = input("Username: ")
#my_username = "" #FIXME

# create socket and connect
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

# sign-in GUI
sign_in = Tk()
sign_in.title("Sign In")

user_label = Label(sign_in, text="Username: ", font=("Arial", 16))
user_label.pack()

user_entry = Entry(sign_in, width=50)
user_entry.pack()

confirm_button = Button(sign_in, text="Confirm", command=lambda: button_click("Confirm"))
confirm_button.pack()

cancel_button = Button(sign_in, text="Cancel", command=lambda: button_click("Cancel"))
cancel_button.pack()

def button_click(button):
    if button == "Cancel":
        sign_in.destroy()
    elif button == "Confirm":
        my_username = user_entry.get()
        username = my_username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(username_header + username)
        print("Username: " + my_username)
        sign_in.destroy()

my_username = user_entry.get()
     
# create socket and connect
#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect((IP, PORT))
#client_socket.setblocking(False)

# send username and header to server
#username = my_username.encode('utf-8')
#username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
#client_socket.send(username_header + username)

sign_in.mainloop() #FIXME?

# chat window GUI
window = Tk()
window.title("Chatroom")
window.configure(bg="#A4C1DB")

chat_title = Label(window, text="Chatroom", bg="white", font=("Arial", 14))
chat_title.pack(padx=20, pady=5)

chatbox = ScrolledText(window)
chatbox.pack(padx=20, pady=5)
chatbox.config(state='disabled')

msg_label = Label(window, text="Message: ", bg="white", font=("Arial", 14))
msg_label.pack(padx=20, pady=5)

input_field = Text(window, height=3)
input_field.pack(padx=20, pady=5)

send_button = Button(window, text="Send", font=("Arial", 14), command=lambda: press("Send"))
send_button.pack()

#TODO add exit button

#window.protocol("WM_DELETE_WINDOW", 

def press(button):

    #message = input(f'{my_username} > ') # for terminal only
    
    if button == "Send":
        message = f"{my_username}: {input_field.get('1.0', 'end')}"
        input_field.delete('1.0', 'end')
        chatbox.config(state='normal')
        chatbox.insert('end', message)
        chatbox.yview('end')
        chatbox.config(state='disabled')
        
        # if message is not empty, send it
        if message:
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)

try:
        # loop over received messages and print them
    while True:
        username_header = client_socket.recv(HEADER_LENGTH)

        # if no data received, connection was terminated
        if not len(username_header):
            print('Connection closed by the server')
            sys.exit()

        # receive username
        username_length = int(username_header.decode('utf-8').strip())
        username = client_socket.recv(username_length).decode('utf-8')

        # receive message and decode it
        message_header = client_socket.recv(HEADER_LENGTH)
        message_length = int(message_header.decode('utf-8').strip())
        message = client_socket.recv(message_length).decode('utf-8')

        # display message
        print(f'{username} > {message}') #FIXME for terminal only, delete later?
        message = f"{username}: {message}"
        chatbox.config(state='normal')
        chatbox.insert('end', message)
        chatbox.yview('end')
        chatbox.config(state='disabled')

except IOError as e:
    # error checking
    if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
        print('Reading error: {}'.format(str(e)))
        sys.exit()

    # if nothing was received...
    #continue

except Exception as e:
    print('Reading error: '.format(str(e)))
    sys.exit()
        
#sign_in.mainloop() #FIXME?
window.mainloop()
