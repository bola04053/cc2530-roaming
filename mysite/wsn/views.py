#coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Template, Context
from json import dumps, load
from django.core.files import File
from django.core import serializers
from impacket import ImpactDecoder, ImpactPacket, IP6, ICMP6, version
import socket
import datetime
import thread
import serial
import time
import json
import sys
import select



def sensors(request):
    return HttpResponse("<h1>6lowpan networks</h1>")
		
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def html(request):
	now = datetime.datetime.now()
	t = get_template('index.html')
	html = t.render(Context({'current_date': now}))  
	return HttpResponse(html)
    
def demo(request):
    return render_to_response('index.html')

def get_data(request, type):
	if type=="udp":
		udpT6Server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		print "UDP TCP IPv6 Mode Start....."
		udpT6Server.bind(('bbbb::212:4b00:205:f000', 5678))
		print "UDP Server Start" 
		while True:
			udpT4Data, udpT6ServerInfo = udpT6Server.recvfrom(1024)
			data = udpT4Data
			source_ip = udpT6ServerInfo[0]
			source_port = udpT6ServerInfo[1]
			rlist = [data, source_ip, source_port]
			print data, source_ip, source_port
			with open('data.json', 'w') as f:
				myfile = File(f)
				myfile.write(json.dumps({"data": rlist[0], "ip": rlist[1], "port":rlist[2]}))
			print "save"

	elif  type=="tcp":
	
		tcpT6Server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		print "Server Socket Created......."
		tcpT6Server.bind(('bbbb::212:4b00:205:f000', 5678))
		print "Wating for connecting......."
		tcpT6Server.listen(5)
		while True:
			clientSock, clientaddr = tcpT6Server.accept()
			print "Connected from: ", clientSock.getpeername() 
			clientSock.send('Congratulations......')
	else:
		return HttpResponse("Please choose a protocol")	
	
def post_data(request):
	with open('data.json', 'r') as f:
		line = f.readline()
		f.close()
		rlist = json.loads(line)
		rjson = json.dumps(rlist)
		response = HttpResponse()
		response['Content-Type'] = "text/javascript"
		response.write(rjson)
		return response

def get_serial(request, usb):
	number = '';
	if (usb == '0'):
		number = "/dev/ttyUSB0"
	elif (usb == '1'):
		number = "/dev/ttyUSB1"
	elif (usb == '2'):
		number = "/dev/ttyUSB2"
	elif (usb == '3'):
		number = "/dev/ttyUSB3"
	port = serial.Serial(number, 
						baudrate=115200, 
						timeout=1.2,
						parity=serial.PARITY_ODD,
						stopbits=serial.STOPBITS_ONE,
						bytesize=serial.EIGHTBITS)
	with open('serial.txt', 'w') as f:
		myfile = File(f)
		myfile.write('')
	while True:
		#print readlineCR(port)
		rlist = readlineCR(port)+'</br>'
		with open('serial.txt', 'a') as f:
			myfile = File(f)
			myfile.write(rlist)

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv

def post_serial(request):
	with open('serial.txt', 'r') as f:
		line = f.read()
		f.close()
		#rlist = json.loads(line)
		#rjson = json.dumps(rlist)
		response = HttpResponse()
		#response['Content-Type'] = "text/javascript"
		response.write(line)
		return response

		
def get_ping(request, dst):
	ip = IP6.IP6()
	ip.set_source_address("bbbb::0212:4b00:0205:f000")
	ip.set_destination_address(dst)
	ip.set_traffic_class(0)
	ip.set_flow_label(0)
	ip.set_hop_limit(64)
	s = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_ICMPV6)
	payload = "6lowpan roaming"
	seq_id = 0
	with open('ping6.txt', 'w') as f:
		myfile = File(f)
		myfile.write('')
	while True:
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
					   #print "%d bytes from %s: icmp_seq=%d " % (rip.child().get_size()-4,dst,rip.get_echo_sequence_number())
					   rlist = "%d bytes from %s: icmp_seq=%d </br>" % (rip.child().get_size()-4,dst,rip.get_echo_sequence_number())
					   with open('ping6.txt', 'a') as f:
							myfile = File(f)
							myfile.write(rlist)
							time.sleep(1) 
	
def post_ping(request):
	with open('ping6.txt', 'r') as f:
		line = f.read()
		f.close()
		#rlist = json.loads(line)
		#rjson = json.dumps(rlist)
		response = HttpResponse()
		#response['Content-Type'] = "text/javascript"
		response.write(line)
		return response

def simple_udp():
	udpT6Server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
	print "UDP TCP IPv6 Mode Start....."
	udpT6Server.bind(('bbbb::212:4b00:205:f000', 5678))
	#print "UDP Server Start" 
	#while True:
	udpT4Data, udpT6ServerInfo = udpT6Server.recvfrom(1024)
	data = udpT4Data
	source_ip = udpT6ServerInfo[0]
	source_port = udpT6ServerInfo[1]
	print data, source_ip, source_port
	
	rlist = [data, source_ip, source_port]
	rlist2 = []
	rlist2.append({"data": rlist[0], "ip": rlist[1], "port":rlist[2]})
	rjson = json.dumps(rlist2)
	response = HttpResponse()
	response['Content-Type'] = "text/javascript"
	response.write(rjson)
	return response
		
def simple_tcp():
	tcpT6Server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	print "Server Socket Created......."
	tcpT6Server.bind(('bbbb::212:4b00:205:f000', 5678))
	print "Wating for connecting......."
	tcpT6Server.listen(5)
	while True:
		clientSock, clientaddr = tcpT6Server.accept()
		print "Connected from: ", clientSock.getpeername() 
		clientSock.send('Congratulations........')
	
	
def udp(request):
	udpT6Server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
	print "UDP TCP IPv6 Mode Start....."
	udpT6Server.bind(('bbbb::212:4b00:205:f000', 5678))
	print "UDP Server Start"
	while True:
		udpT4Data, udpT6ServerInfo = udpT6Server.recvfrom(1024)
		print "Receive from ", udpT6ServerInfo, " and The Data send from :", udpT4Data
		html = "<html>\
					<body>\
						UDP Recv %s from %s\
					</body>\
				</html>" % (udpT6ServerInfo, udpT4Data)
		return HttpResponse(html)
		
def tcp(request):
	tcpT6Server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	print "Server Socket Created......."
	tcpT6Server.bind(('bbbb::212:4b00:205:f000', 5678))
	print "Wating for connecting......."
	tcpT6Server.listen(5)
	while True:
		clientSock, clientaddr = tcpT6Server.accept()
		print "Connected from: ", clientSock.getpeername() 
		clientSock.send('Congratulations........')
		html = "<html>\
			<body>\
				TCP set connection with %s\
			</body>\
		</html>" % udpT6ServerInfo
		return HttpResponse(html)
		#clientSock.close()
