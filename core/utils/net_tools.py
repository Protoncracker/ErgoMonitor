from scapy.all import ICMP, IP, sr1, TCP, UDP, sr, DNS, DNSQR, ARP, Ether, conf, traceroute
import logging

class NetTools:
    """
    NetTools provides advanced network operations using Scapy.
    This includes ICMP ping, TCP/UDP packet sending, and basic network discovery.
    """

    def __init__(self):
        """
        Initialize the NetTools instance.
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('NetTools')
        

    def traceroute(self, target, max_ttl=30, timeout=2):
        """
        Perform a traceroute to a target IP or hostname.

        Args:
            target (str): Target IP address or hostname.
            max_ttl (int): Maximum TTL value (effectively the max hops).
            timeout (int): Timeout for each probe.

        Returns:
            list: List of tuples (hop_number, hop_IP).
        """
        result, _ = traceroute(target, maxttl=max_ttl, timeout=timeout, verbose=0)
        hops = [(i+1, res[0].src) for i, res in enumerate(result)]
        return hops

    def arp_discovery(self, network, timeout=2):
        """
        Discover hosts in a network using ARP.

        Args:
            network (str): Network address with CIDR (e.g., '192.168.1.0/24').
            timeout (int): Timeout for ARP requests.

        Returns:
            dict: Dictionary of IP addresses and corresponding MAC addresses.
        """
        arp_req = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network)
        ans, _ = sr(arp_req, timeout=timeout, verbose=0, iface=conf.iface)
        return {rcv.psrc: rcv.hwsrc for snd, rcv in ans}



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

    # Example of a custom TCP/UDP operation
    def send_tcp_packet(self, target, port, payload=""):
        """
        Send a custom TCP packet to a specified target and port.

        Args:
            target (str): Target IP address or hostname.
            port (int): Target port number.
            payload (str): Optional payload to send.

        Returns:
            bool: True if the packet was sent, False otherwise.
        """
        try:
            sr(IP(dst=target)/TCP(dport=port)/payload, timeout=1, verbose=0)
            return True
        except Exception as e:
            self.logger.error(f"Error sending TCP packet: {e}")
            return False

    # Additional methods for UDP operations, custom packet crafting, etc., can be added

    def send_udp_packet(self, target, port, payload=""):
        """
        Send a custom UDP packet to a specified target and port.

        Args:
            target (str): Target IP address or hostname.
            port (int): Target port number.
            payload (str): Optional payload to send.

        Returns:
            bool: True if the packet was sent, False otherwise.
        """
        try:
            sr(IP(dst=target)/UDP(dport=port)/payload, timeout=1, verbose=0)
            return True
        except Exception as e:
            self.logger.error(f"Error sending UDP packet: {e}")
            return False

    def resolve_hostname(self, hostname):
        """
        Resolve a hostname to an IP address using DNS query with Scapy.

        Args:
            hostname (str): The hostname to resolve.

        Returns:
            str: The resolved IP address or an error message.
        """
        try:
            dns_response = sr1(IP(dst="8.8.8.8")/UDP()/DNS(rd=1, qd=DNSQR(qname=hostname)), verbose=0, timeout=1)
            if dns_response and dns_response.haslayer(DNS) and dns_response.getlayer(DNS).an:
                return dns_response.getlayer(DNS).an.rdata
            else:
                return "No response or error in DNS query"
        except Exception as e:
            self.logger.error(f"Error resolving hostname: {e}")
            return "Error in DNS resolution"

    def check_port(self, target, port, protocol="tcp"):
        """
        Check if a specific port is open on the target using Scapy.

        Args:
            target (str): Target IP address or hostname.
            port (int): Port number to check.
            protocol (str): Protocol type ('tcp' or 'udp').

        Returns:
            bool: True if the port is open, False otherwise.
        """
        pkt = IP(dst=target)/TCP(dport=port, flags='S') if protocol == "tcp" else IP(dst=target)/UDP(dport=port)
        resp = sr1(pkt, timeout=1, verbose=0)
        if resp:
            if protocol == "tcp" and resp.haslayer(TCP) and resp.getlayer(TCP).flags & 0x12:
                return True
            elif protocol == "udp" and resp.haslayer(UDP):
                return True
        return False

    # Additional methods can be added for more complex network operations

if __name__ == "__main__":
    net_tools = NetTools()

    # Example usage
    ip = net_tools.resolve_hostname("example.com")
    print(f"Resolved IP: {ip}")

    is_port_open = net_tools.check_port("scanme.nmap.org", 80)
    print(f"Port 80 open on scanme.nmap.org: {is_port_open}")

    trace_result = net_tools.traceroute("google.com")
    print("Traceroute Result:")
    for hop in trace_result:
        print(f"{hop[0]}: {hop[1]}")

    arp_result = net_tools.arp_discovery("192.168.1.0/24")
    print("\nARP Discovery Result:")
    for ip, mac in arp_result.items():
        print(f"{ip} -> {mac}")