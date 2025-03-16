import socket
import time
import os
import struct
from datetime import datetime

# This will listen for UDP packets on port 1234
# and rebroadcast them on port 1235 and 1236
# while also logging each packet to a binary file

# Configure the listening address and port
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 1234  # Source UDP port

# Configure the two destination addresses (IP and port)
DEST1 = ("127.0.0.1", 1235)  # Rebroadcast on port 1235
DEST2 = ("127.0.0.1", 1236)  # Rebroadcast on port 1236

# Configure logging
LOG_DIR = "udp_logs"
LOG_FILENAME = f"udp_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bin"

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, LOG_FILENAME)

# Create a UDP socket for receiving and sending
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LISTEN_IP, LISTEN_PORT))

print(f"Listening for UDP packets on {LISTEN_IP}:{LISTEN_PORT}")
print(f"Logging packets to {log_path}")

with open(log_path, 'wb') as log_file:
    while True:
        try:
            # Receive data from the source process
            data, addr = sock.recvfrom(4096)  # Adjust buffer size if needed

            # Get current timestamp
            timestamp = time.time()

            # Write packet metadata (optional - can be customized)
            # Format: 8 bytes for timestamp, 4 bytes for data length
            log_file.write(struct.pack('!d', timestamp))  # 8-byte double
            log_file.write(len(data).to_bytes(4, byteorder='big'))

            # Write the actual packet data
            log_file.write(data)

            # Flush to ensure data is written immediately
            log_file.flush()

            # Forward the same data to both destinations
            sock.sendto(data, DEST1)
            sock.sendto(data, DEST2)

            print(f"Received {len(data)} bytes from {addr} - logged and forwarded")

        except Exception as e:
            print(f"Error: {e}")
