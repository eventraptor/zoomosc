import socket
import struct
import time
import os
import argparse
from datetime import datetime

def replay_udp_log(log_file_path, dest_ports=[1235, 1236], speed_factor=1.0):
    """
    Replay UDP packets from a binary log file with original timing.

    Args:
        log_file_path: Path to the binary log file
        dest_ports: List of UDP ports to send packets to (default: [1235, 1236])
        speed_factor: Replay speed multiplier (1.0 = real-time, 2.0 = 2x speed)
    """
    # Create UDP sockets for sending
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Prepare destination addresses
    destinations = [("127.0.0.1", port) for port in dest_ports]

    print(f"Replaying UDP log from: {log_file_path}")
    print(f"Sending to ports: {dest_ports}")
    print(f"Replay speed factor: {speed_factor}x")

    # Open and read the binary log file
    with open(log_file_path, 'rb') as log_file:
        first_packet = True
        last_timestamp = None
        start_time = time.time()
        packet_count = 0

        while True:
            try:
                # Read timestamp (8 bytes)
                timestamp_bytes = log_file.read(8)
                if not timestamp_bytes or len(timestamp_bytes) < 8:
                    break  # End of file

                # Read packet length (4 bytes)
                length_bytes = log_file.read(4)
                if not length_bytes or len(length_bytes) < 4:
                    break  # Unexpected EOF

                # Extract values
                timestamp = struct.unpack('!d', timestamp_bytes)[0]
                packet_length = int.from_bytes(length_bytes, byteorder='big')

                # Read packet data
                packet_data = log_file.read(packet_length)
                if not packet_data or len(packet_data) < packet_length:
                    break  # Unexpected EOF

                # For the first packet, we don't need to wait
                if first_packet:
                    first_packet = False
                    last_timestamp = timestamp
                else:
                    # Calculate delay based on original timing
                    delay = (timestamp - last_timestamp) / speed_factor
                    if delay > 0:
                        time.sleep(delay)
                    last_timestamp = timestamp

                # Send packet to all destination ports
                for dest in destinations:
                    sock.sendto(packet_data, dest)

                packet_count += 1

                # Print progress
                elapsed = time.time() - start_time
                print(f"\rReplayed {packet_count} packets ({elapsed:.2f} seconds elapsed)", end="")

            except Exception as e:
                print(f"\nError processing packet: {e}")
                break

    print(f"\nReplay complete. Sent {packet_count} packets.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replay UDP packets from binary log")
    parser.add_argument("log_file", help="Path to the binary log file")
    parser.add_argument("--ports", type=int, nargs="+", default=[1235, 1236],
                        help="UDP ports to send packets to (default: 1235 1236)")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="Replay speed factor (1.0=real-time, 2.0=2x speed)")

    args = parser.parse_args()

    if not os.path.exists(args.log_file):
        print(f"Error: Log file not found: {args.log_file}")
        exit(1)

    replay_udp_log(args.log_file, args.ports, args.speed)
