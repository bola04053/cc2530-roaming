import select
import socket
import time
import sys
 
from impacket import ImpactDecoder, ImpactPacket, IP6, ICMP6, version
print version.BANNER
 
if len(sys.argv) < 3:
        print "Use: %s <src ip> <dst ip>" % sys.argv[0]
        sys.exit(1)
 
src = sys.argv[1]
dst = sys.argv[2]
 
# Create a new IP packet and set its source and destination addresses.
 
ip = IP6.IP6()
ip.set_source_address(src)
ip.set_destination_address(dst)
ip.set_traffic_class(0)
ip.set_flow_label(0)
ip.set_hop_limit(64)
 
# Open a raw socket. Special permissions are usually required.
 
s = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_ICMPV6)
 
payload = "6lowpan roaming"
 
print "PING %s %d data bytes" % (dst, len(payload))
 
seq_id = 0
 
while 1:
 
        # Give the ICMP packet the next ID in the sequence.
        seq_id += 1
        icmp = ICMP6.ICMP6.Echo_Request(1, seq_id, payload)
        # Have the IP packet contain the ICMP packet (along with its payload).
        ip.contains(icmp)
        ip.set_next_header(ip.child().get_ip_protocol_number())
        ip.set_payload_length(ip.child().get_size())
        icmp.calculate_checksum()
 
        # Send it to the target host.
        s.sendto(icmp.get_packet(), (dst, 0))
 
        # Wait for incoming replies.
        if s in select.select([s],[],[],1)[0]:
           reply = s.recvfrom(2000)[0]
           # Use ImpactDecoder to reconstruct the packet hierarchy.
           rip = ImpactDecoder.ICMP6Decoder().decode(reply)
 
           # If the packet matches, report it to the user.
           if ICMP6.ICMP6.ECHO_REPLY == rip.get_type():
                   print "%d bytes from %s: icmp_seq=%d " % (rip.child().get_size()-4,dst,rip.get_echo_sequence_number())
 
           time.sleep(1) 
