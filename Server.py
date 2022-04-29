import socket
import threading
import os
import protocol
from time import sleep

IP = socket.gethostbyname(socket.gethostname())
c=socket.socket()
PORT = 5566
ADDR = (IP, PORT)
SIZE = 4096
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def file_recive(file_name, conn, file_size):
    """
    the function saves file.
    """
    total_recv = 0
    with open(file_name, "wb") as f:

        sleep(0.1)  # בכדי שלא יווצר מצב שהלקוח מנסה לקלוט מידע לפני שקיבל אותו

        while total_recv < file_size:  # קבלת המידע

            buffer = protocol.get_msg(c)

            if type(buffer) is not bytes:
                buffer = buffer.encode()

            total_recv += len(buffer)

            f.write(buffer)

    print(protocol.get_msg(conn.recv(4096)))



def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    client = (conn,addr)
    connected = True
    while connected:
        msg = conn.recv(4096)
        if type(msg) is not bytes:
            open(msg)
        else:
            file_recive("my-image.png", conn, file_size=int(protocol.get_msg(conn.recv(4096))) )

        if msg == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] {msg}")
        msg = f"Msg received: {msg}"

        conn.send(msg)

    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")






if __name__ == "__main__":
    main()