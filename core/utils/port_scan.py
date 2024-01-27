from scapy.all import IP, TCP, sr1, sr
import logging

class PortScanner:
    """
    PortScanner provides functionalities for network port scanning,
    similar to Nmap, using Scapy.
    """

    def __init__(self):
        """
        Initialize the PortScanner instance.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('PortScanner')

    def scan(self, target, port_range="1-1024", scan_type="SYN"):
        """
        Perform a port scan on a target.

        Args:
            target (str): Target IP address or hostname.
            port_range (str): Range of ports to scan (e.g., '1-1024').
            scan_type (str): Type of scan ('SYN', 'UDP', etc.).

        Returns:
            dict: Results of the scan with list of open ports.
        """
        start_port, end_port = (int(x) for x in port_range.split('-'))
        open_ports = []

        if scan_type.upper() == "SYN":
            # Perform SYN scan
            for port in range(start_port, end_port + 1):
                print(f'eto: pr {port}')
                pkt = IP(dst=target)/TCP(dport=port, flags='S')
                resp = sr1(pkt, timeout=1, verbose=0)
                if resp and resp.haslayer(TCP) and resp.getlayer(TCP).flags & 0x12:  # SYN-ACK flags
                    open_ports.append(port)
                    sr(IP(dst=target)/TCP(dport=port, flags='R'), timeout=1, verbose=0)  # Reset connection

        # Additional scan types like 'UDP', 'XMAS', etc., can be implemented here

        return {
            "target": target,
            "port_range": port_range,
            "scan_type": scan_type,
            "open_ports": open_ports
        }

if __name__ == "__main__":
    port_scanner = PortScanner()

    # Example usage
    scan_result = port_scanner.scan("scanme.nmap.org", port_range="20-80", scan_type="SYN")
    print(f"Scan Result: {scan_result}")
