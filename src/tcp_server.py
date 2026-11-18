import socket
import threading
from protocol import recv_msg, send_msg

HOST, PORT = "127.0.0.1", 9000

def handle(conn, addr):
    print(f"[+] {addr} connected")
    try:
        with conn:
            while True:
                msg = recv_msg(conn)
                if msg is None:
                    break
                print(f"[{addr[1]}] {msg}")
                send_msg(conn, {"ack": msg.get("seq"), "status": "ok"})
    except (ValueError, ConnectionError) as e:
        print(f"[!] {addr}: {e}")
    print(f"[-] {addr} disconnected")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"Listening on {HOST}:{PORT}")
        while True:
            conn, addr = srv.accept()
            threading.Thread(target=handle, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()