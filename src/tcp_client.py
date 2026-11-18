import socket
import sys
import time
from protocol import send_msg, recv_msg

HOST, PORT = "127.0.0.1", 9000

def main(count=5):
    with socket.create_connection((HOST, PORT)) as s:
        for seq in range(count):
            t0 = time.perf_counter()
            send_msg(s, {"seq": seq, "sensor": "temp", "value": 25.0 + seq})
            reply = recv_msg(s)
            rtt_ms = (time.perf_counter() - t0) * 1000
            print(f"seq={seq} reply={reply} rtt={rtt_ms:.3f} ms")
            time.sleep(0.5)

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 5)