from scapy.all import IP, ICMP, sr1, sr, TCP, UDP
from socket import getservbyname
import logging # will edit later. I need some (ANY) logs for now lol

class NetTools:
    """
    NetTools provides functionalities for network operations similar to netcat, 
    including packet sending, network discovery, and port scanning using Scapy.
    """

    def __init__(self):
        """
        Initialize the NetTools instance.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('NetTools')

    def ping(self, target, count=1):
        """
        Perform ICMP ping to a target IP or hostname.

        Args:
            target (str): Target IP address or hostname.
            count (int): Number of ping requests to send.

        Returns:
            dict: Ping results including success rate and round-trip times.
        """
        answered, _ = sr(IP(dst=target)/ICMP(), retry=2, timeout=1, count=count, verbose=0)
        success_rate = len(answered) / count * 100
        rtt_list = [round((rcv.time - snd.time) * 1000, 2) for snd, rcv in answered]

        return {
            "target": target,
            "sent": count,
            "received": len(answered),
            "success_rate": success_rate,
            "rtt_ms": rtt_list
        }

    def port_scan(self, target, port_range="1-1024"):
        """
        Perform a TCP port scan on a target.

        Args:
            target (str): Target IP address or hostname.
            port_range (str): Range of ports to scan (e.g., '1-1024').

        Returns:
            list: List of open ports.
        """
        start_port, end_port = (int(x) for x in port_range.split('-'))
        open_ports = []
        for port in range(start_port, end_port + 1):
            pkt = IP(dst=target)/TCP(dport=port, flags='S')
            resp = sr1(pkt, timeout=1, verbose=0)
            if resp and resp.haslayer(TCP) and resp.getlayer(TCP).flags & 0x12:  # SYN-ACK flags
                open_ports.append(port)
                sr(IP(dst=target)/TCP(dport=port, flags='R'), timeout=1, verbose=0)  # Reset connection

        return open_ports

    # Additional methods will be added for more functionalities. I'm tired.

if __name__ == "__main__":
    net_tools = NetTools()

    # Example usage
    ping_result = net_tools.ping("8.8.8.8", 3)
    print(f"Ping Result: {ping_result}")

    open_ports = net_tools.port_scan("scanme.nmap.org", port_range="20-80")
    print(f"Open ports on scanme.nmap.org: {open_ports}")
