#!/usr/bin/env python3
"""
CodeAlpha Cyber Security Internship - Task 1
Basic Network Sniffer
---------------------------------------------
Captures live network packets and displays useful information:
    - Source / Destination IP addresses
    - Protocol (TCP / UDP / ICMP / Other)
    - Source / Destination ports (for TCP/UDP)
    - Payload (raw application data, if present)

Requirements:
    pip install scapy

Usage:
    Linux/Mac:  sudo python3 sniffer.py
    Windows:    Run terminal as Administrator, install Npcap first
                (https://npcap.com), then: python sniffer.py

    Optional arguments:
        -i / --iface   : network interface to sniff on (e.g. eth0, wlan0)
        -c / --count   : number of packets to capture (0 = infinite, default)
        -f / --filter  : BPF filter string (e.g. "tcp", "udp port 53")

Examples:
    sudo python3 sniffer.py -i eth0 -c 50
    sudo python3 sniffer.py -f "tcp port 80"

NOTE: Only run this on networks / systems you own or have explicit
permission to monitor. Unauthorized packet sniffing may be illegal.
"""

import argparse
import datetime

try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
except ImportError:
    print("[!] Scapy is not installed. Install it with: pip install scapy")
    raise SystemExit(1)


PROTOCOL_MAP = {
    1: "ICMP",
    6: "TCP",
    17: "UDP",
}


def get_protocol_name(proto_num: int) -> str:
    return PROTOCOL_MAP.get(proto_num, f"OTHER({proto_num})")


def format_payload(raw_bytes: bytes, max_len: int = 80) -> str:
    """Return a printable, truncated preview of the payload."""
    try:
        text = raw_bytes.decode("utf-8", errors="replace")
    except Exception:
        text = str(raw_bytes)
    text = text.replace("\n", "\\n").replace("\r", "\\r")
    if len(text) > max_len:
        text = text[:max_len] + "...(truncated)"
    return text


def process_packet(packet):
    """Callback executed for every captured packet."""
    if IP not in packet:
        return  # skip non-IP packets (e.g. ARP) for this basic version

    ip_layer = packet[IP]
    src_ip = ip_layer.src
    dst_ip = ip_layer.dst
    proto_name = get_protocol_name(ip_layer.proto)

    src_port = dst_port = None
    if TCP in packet:
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif UDP in packet:
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport

    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    header = f"[{timestamp}] {proto_name:8s} {src_ip}"
    if src_port is not None:
        header += f":{src_port}"
    header += f"  ->  {dst_ip}"
    if dst_port is not None:
        header += f":{dst_port}"
    print(header)

    # ICMP extra info
    if ICMP in packet:
        icmp_layer = packet[ICMP]
        print(f"    ICMP type={icmp_layer.type} code={icmp_layer.code}")

    # Show a preview of the payload, if any
    if Raw in packet:
        payload_preview = format_payload(bytes(packet[Raw].load))
        print(f"    Payload: {payload_preview}")

    print("-" * 70)


def main():
    parser = argparse.ArgumentParser(description="Basic Network Sniffer (CodeAlpha Task 1)")
    parser.add_argument("-i", "--iface", default=None,
                         help="Network interface to sniff on (default: scapy auto-selects)")
    parser.add_argument("-c", "--count", type=int, default=0,
                         help="Number of packets to capture (0 = infinite until Ctrl+C)")
    parser.add_argument("-f", "--filter", default="",
                         help='BPF filter string, e.g. "tcp", "udp port 53"')
    args = parser.parse_args()

    print("=" * 70)
    print(" CodeAlpha Task 1 - Basic Network Sniffer")
    print(" Press Ctrl+C to stop capturing")
    print("=" * 70)

    try:
        sniff(
            iface=args.iface,
            filter=args.filter if args.filter else None,
            prn=process_packet,
            count=args.count,
            store=False,
        )
    except PermissionError:
        print("[!] Permission denied. Try running with sudo/administrator privileges.")
    except KeyboardInterrupt:
        print("\n[*] Capture stopped by user.")


if __name__ == "__main__":
    main()
