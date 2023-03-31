
import socket
import threading
import time
import struct
import os

if os.name == 'nt':
    import msvcrt

CRDP = 5000
BUFFER_SIZE = 1024

class ChatClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_name = ""
        self.connected_to_server = False
        self.chat_mode = False
        self.chat_rooms = {}

    def connect_to_server(self):
        self.client_socket.connect(("localhost", CRDP))
        self.connected_to_server = True

    def receive_messages(self, chat_room_socket, multicast_group, server_address):
        while self.chat_mode:
            message = chat_room_socket.recv(BUFFER_SIZE).decode()
            print(message)
            time.sleep(0.1)

    def send_messages(self, chat_room_socket, multicast_group, server_address):
        while self.chat_mode:
            message = input()
            chat_room_socket.sendto((self.chat_name + ": " + message).encode(), (multicast_group, server_address))
    

    def chat(self, chat_room_name):
        if chat_room_name not in self.chat_rooms:
            print("Chat room not found.")
            return

        multicast_group, server_address = self.chat_rooms[chat_room_name]
        chat_room_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        chat_room_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

        # Enable SO_REUSEADDR before binding
        chat_room_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the chat_room_socket to the multicast address and port
        chat_room_socket.bind(("", server_address))

        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        chat_room_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.chat_mode = True
        print("Entering chat mode. Press Ctrl+C to exit.")

        recv_thread = threading.Thread(target=self.receive_messages, args=(chat_room_socket, multicast_group, server_address), daemon=True)
        recv_thread.start()

        try:
            while self.chat_mode:
                if os.name == 'nt':
                    if msvcrt.kbhit():
                        message = input()
                        if self.chat_name:
                            message = f"{self.chat_name}: {message}"
                        chat_room_socket.sendto(message.encode(), (multicast_group, server_address))
        except KeyboardInterrupt:
            self.chat_mode = False
            print("\nExiting chat mode.")

        chat_room_socket.close()

    def start(self):
        while True:
            command = input("\nEnter a command:\nconnect\nbye\nname <chat name>\nchat <room name>\ngetdir\nmakeroom <chat room name> <address> <port>\ndeleteroom <chat room name>\n\n")
            if not self.connected_to_server and command != "connect":
                print("Not connected to the server.")
                continue

            args = command.split()

            if args[0] == "connect":
                self.connect_to_server()
                print("Connected to the server.")

            elif args[0] == "bye":
                self.connected_to_server = False
                self.client_socket.close()
                print("Disconnected from the server.")
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            elif args[0] == "name":
                self.chat_name = args[1]
                print(f"Chat name set to: {self.chat_name}")

            elif args[0] == "chat":
                self.chat(args[1])

            else:
                self.client_socket.send(command.encode())
                response = self.client_socket.recv(BUFFER_SIZE).decode()
                if args[0] == "getdir":
                    self.chat_rooms = eval(response)
                    print(self.chat_rooms)
                else:
                    print(response)

if __name__ == "__main__":
    client = ChatClient()
    client.start()
