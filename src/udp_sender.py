import json
import random
import socket
import sys
import time

HOST, PORT = "127.0.0.1", 9001

def main(count=100, drop_prob=0.0):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dropped = 0
    for seq in range(count):
        if random.random() < drop_prob:       # simulated loss: skip this packet
            dropped += 1
            time.sleep(0.005)
            continue
        msg = {"seq": seq, "total": count, "ts_ns": time.time_ns(),
               "sensor": "temp", "value": 25.0 + (seq % 10) * 0.1}
        sock.sendto(json.dumps(msg).encode("utf-8"), (HOST, PORT))
        time.sleep(0.005)
    print(f"Sent {count - dropped} packets, deliberately dropped {dropped} (drop probability {drop_prob})")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    drop = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    main(count, drop)