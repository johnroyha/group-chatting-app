import socket
import threading

CRDP = 5000
BUFFER_SIZE = 1024
IP_MULTICAST_RANGE = ("239.0.0.0", "239.255.255.255")

class ChatRoomDirectoryServer:
    def __init__(self):
        self.chat_rooms = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", CRDP))
        self.server_socket.listen(5)
        print("Chat Room Directory Server is listening on port", CRDP)

    def handle_client(self, client_socket, addr):
        while True:
            command = client_socket.recv(BUFFER_SIZE).decode()
            if not command:
                break
            args = command.split()
            cmd = args[0]

            if cmd == "getdir":
                response = str(self.chat_rooms)
            elif cmd == "makeroom" and len(args) == 4:
                room_name, address, port = args[1], args[2], int(args[3])
                if room_name not in self.chat_rooms:
                    self.chat_rooms[room_name] = (address, port)
                    response = "Chat room created."
                else:
                    response = "Chat room already exists."
            elif cmd == "deleteroom" and len(args) == 2:
                room_name = args[1]
                if room_name in self.chat_rooms:
                    del self.chat_rooms[room_name]
                    response = "Chat room deleted."
                else:
                    response = "Chat room not found."
            else:
                response = "Invalid command."
            client_socket.send(response.encode())
        client_socket.close()

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr} established.")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_thread.start()

if __name__ == "__main__":
    crds = ChatRoomDirectoryServer()
    crds.start()
