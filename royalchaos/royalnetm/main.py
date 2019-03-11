import pyshark

capture = pyshark.LiveCapture(interface='eth0')#, display_filter='http')
print('Launching...', capture)
#capture.sniff(timeout=50)
print('the...', capture)
capture.set_debug()
print('application...', capture)
capture

for packet in capture.sniff_continuously(): #packet_count=5):
	if "ip" in packet and packet.ip.dst == "172.17.0.2":
		print("packet to hello_world")
	if 'http' in packet:
	    print('http', packet.http)
	print("--------------")
    #print('Just arrived:', packet)








