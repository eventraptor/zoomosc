import socket

# This will listen for UDP packets on port 1234
# and rebroadcast them on port 1235 and 1236
# This makes it easy to use the Logger together
# with Companion, and they won't conflict

# Configure the listening address and port
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 1234 # Source UDP port

# Configure the two destination addresses (IP and port)
DEST1 = ("127.0.0.1", 1235)  # Rebroadcast on port 1235
DEST2 = ("127.0.0.1", 1236)  # Rebroadcast on port 1236

# Create a UDP socket for receiving and sending
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"Listening for UDP packets on {LISTEN_IP}:{LISTEN_PORT}")

while True:
    # Receive data from the source process
    data, addr = sock.recvfrom(4096)  # Adjust buffer size if needed
    # print(f"Received {len(data)} bytes from {addr}")

    # Forward the same data to both destinations
    sock.sendto(data, DEST1)
    sock.sendto(data, DEST2)
    # print(f"Forwarded packet to {DEST1} and {DEST2}")
