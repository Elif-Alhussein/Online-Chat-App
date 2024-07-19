import threading
import socket
import customtkinter as ctk
from tkinter import simpledialog, messagebox

HOST = '127.0.0.1'
PORT = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except Exception as e:
    print(f"Connection error: {e}")
    exit()


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("Chat Application")
window.geometry("400x500")

def get_nickname():
    nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=window)
    if not nickname:
        messagebox.showerror("Error", "Nickname is required!")
        window.quit()
    return nickname

nickname = get_nickname()

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                chat_area.configure(state="normal")
                chat_area.insert(ctk.END, message + '\n')
                chat_area.configure(state="disabled")
                chat_area.yview(ctk.END)
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break

def write():
    message = f'{nickname}: {message_entry.get()}'
    client.send(message.encode('utf-8'))
    message_entry.delete(0, ctk.END)

def on_closing():
    client.close()
    window.destroy()

chat_area = ctk.CTkTextbox(window, state="disabled", wrap="word", font=("Arial", 12))
chat_area.pack(padx=20, pady=10, fill="both", expand=True)

input_frame = ctk.CTkFrame(window)
input_frame.pack(padx=20, pady=5, fill="x")

message_entry = ctk.CTkEntry(input_frame, width=300, font=("Arial", 12))
message_entry.pack(side="left", fill="x", padx=5)

send_button = ctk.CTkButton(input_frame, text="Send", command=write)
send_button.pack(side="right", padx=5)

window.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

window.mainloop()

