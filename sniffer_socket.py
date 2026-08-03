#!/usr/bin/env python3
"""
CodeAlpha Cyber Security Internship - Task 1
Basic Network Sniffer - Raw Socket Version (no external libraries)
--------------------------------------------------------------------
This version uses Python's built-in `socket` module instead of scapy.
It manually parses the IPv4 and TCP/UDP/ICMP headers to show how
data actually flows through the network at the byte level.

IMPORTANT: Raw sockets require root/administrator privileges and
only work reliably on Linux (AF_PACKET). On Windows/Mac, use
sniffer.py (the scapy version) instead.

Usage:
    sudo python3 sniffer_socket.py
"""

import socket
import struct
import textwrap


def format_mac(mac_bytes: bytes) -> str:
    return ":".join(f"{b:02x}" for b in mac_bytes).upper()


def format_ipv4(addr_bytes: bytes) -> str:
    return ".".join(str(b) for b in addr_bytes)


def unpack_ethernet_frame(raw_data):
    dest_mac, src_mac, proto = struct.unpack("! 6s 6s H", raw_data[:14])
    return format_mac(dest_mac), format_mac(src_mac), socket.htons(proto), raw_data[14:]


def unpack_ipv4_packet(raw_data):
    version_header_length = raw_data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack("! 8x B B 2x 4s 4s", raw_data[:20])
    return version, header_length, ttl, proto, format_ipv4(src), format_ipv4(target), raw_data[header_length:]


def unpack_tcp_segment(raw_data):
    (src_port, dest_port, sequence, acknowledgment, offset_reserved_flags) = struct.unpack(
        "! H H L L H", raw_data[:14]
    )
    offset = (offset_reserved_flags >> 12) * 4
    return src_port, dest_port, sequence, acknowledgment, raw_data[offset:]


def unpack_udp_segment(raw_data):
    src_port, dest_port, size = struct.unpack("! H H 2x H", raw_data[:8])
    return src_port, dest_port, size, raw_data[8:]


def unpack_icmp_packet(raw_data):
    icmp_type, code, checksum = struct.unpack("! B B H", raw_data[:4])
    return icmp_type, code, checksum, raw_data[4:]


def format_payload(raw_bytes: bytes, max_len: int = 80) -> str:
    try:
        text = raw_bytes.decode("utf-8", errors="replace")
    except Exception:
        text = str(raw_bytes)
    text = text.replace("\n", "\\n").replace("\r", "\\r")
    if len(text) > max_len:
        text = text[:max_len] + "...(truncated)"
    return text


def main():
    try:
        conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    except AttributeError:
        print("[!] AF_PACKET is only available on Linux. Use sniffer.py (scapy version) instead.")
        return
    except PermissionError:
        print("[!] Permission denied. Run this script with sudo.")
        return

    print("=" * 70)
    print(" CodeAlpha Task 1 - Basic Network Sniffer (raw socket version)")
    print(" Press Ctrl+C to stop capturing")
    print("=" * 70)

    try:
        while True:
            raw_data, _ = conn.recvfrom(65535)
            dest_mac, src_mac, eth_proto, eth_payload = unpack_ethernet_frame(raw_data)

            # 0x0800 = IPv4
            if eth_proto != 8:
                continue

            version, header_len, ttl, proto, src_ip, dst_ip, ip_payload = unpack_ipv4_packet(eth_payload)

            if proto == 6:  # TCP
                src_port, dst_port, seq, ack, payload = unpack_tcp_segment(ip_payload)
                print(f"TCP   {src_ip}:{src_port}  ->  {dst_ip}:{dst_port}  (ttl={ttl})")
            elif proto == 17:  # UDP
                src_port, dst_port, size, payload = unpack_udp_segment(ip_payload)
                print(f"UDP   {src_ip}:{src_port}  ->  {dst_ip}:{dst_port}  (ttl={ttl})")
            elif proto == 1:  # ICMP
                icmp_type, code, checksum, payload = unpack_icmp_packet(ip_payload)
                print(f"ICMP  {src_ip}  ->  {dst_ip}  type={icmp_type} code={code}")
            else:
                payload = ip_payload
                print(f"OTHER({proto}) {src_ip}  ->  {dst_ip}")

            if payload:
                print(f"    Payload: {format_payload(payload)}")
            print("-" * 70)

    except KeyboardInterrupt:
        print("\n[*] Capture stopped by user.")


if __name__ == "__main__":
    main()
