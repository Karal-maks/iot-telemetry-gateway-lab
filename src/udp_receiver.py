import json
import socket
import time

HOST, PORT = "127.0.0.1", 9001
IDLE_TIMEOUT = 2.0   # stop after this many seconds of silence

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    sock.settimeout(60.0)   # wait up to 60 s for the first packet
    print(f"Listening on UDP {HOST}:{PORT} (stops after {IDLE_TIMEOUT} s of silence)")

    seen = set()
    latencies_ms = []
    highest = -1
    reordered = 0
    duplicates = 0
    total = 0

    try:
        while True:
            data, _ = sock.recvfrom(2048)
            sock.settimeout(IDLE_TIMEOUT)
            now_ns = time.time_ns()
            try:
                msg = json.loads(data.decode("utf-8"))
                seq = msg["seq"]
                total = max(total, msg["total"])
                sent_ns = msg["ts_ns"]
            except (ValueError, KeyError):
                continue                      # ignore malformed packets
            if seq in seen:
                duplicates += 1
                continue
            if seq < highest:
                reordered += 1                # arrived after a higher seq
            highest = max(highest, seq)
            seen.add(seq)
            latencies_ms.append((now_ns - sent_ns) / 1e6)
    except socket.timeout:
        pass

    received = len(seen)
    lost = total - received
    print("\n--- UDP results ---")
    print(f"Expected packets : {total}")
    print(f"Received         : {received}")
    print(f"Lost             : {lost} ({100.0 * lost / total:.1f}%)" if total else "Lost: n/a")
    print(f"Reordered        : {reordered}")
    print(f"Duplicates       : {duplicates}")
    if latencies_ms:
        print(f"Latency (ms)     : min {min(latencies_ms):.3f} | "
              f"avg {sum(latencies_ms) / len(latencies_ms):.3f} | max {max(latencies_ms):.3f}")

if __name__ == "__main__":
    main()