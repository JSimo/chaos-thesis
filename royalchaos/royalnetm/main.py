import pyshark
import time

#Global variables
httpTimer = [] #For storing incoming request time and later use.

#Helper methods:
current_time_milli = lambda: int(round(time.time() * 1000))

def main():
    capture = pyshark.LiveCapture(interface='eth0',  bpf_filter='host 172.17.0.2')#, display_filter='http')
    print('Launching...', capture)
    #capture.sniff(timeout=50)
    print('the...', capture)
    capture.set_debug()
    print('application...', capture)
    capture

    for packet in capture.sniff_continuously(): #packet_count=5):
        #if "ip" in packet and packet.ip.dst == "172.17.0.2":
            #print('p', end='')
            #print("packet to hello_world")
        if 'http' in packet:
            print('') #newline
            process_http(packet.http)
            
            #print(packet.http.field_names)
            #print('http', dir(packet.http))
            #print(list(filter(lambda a: not a.startswith('_'), dir(packet.http))))
            #print('http2', dir(packet.http.host))
            #if 'response_code' in packet.http:
                #    print('test', packet.http['response_code'])
            #if 'request' in packet.http.field_names:
            #    print('REQUEST!')
            #    print(packet.http.request)
            #    print(packet.http.request_number)
            #if 'response' in packet.http.field_names:
            #    print('RESPONSE!')
            #    print(packet.http.response)
            #    #print(packet.http.request_in)
            #    print(packet.http.response_number)
            #print("--------------")
        #print('Just arrived:', packet)

def process_http(http):
    if 'request' in http.field_names:
        print('REQUEST!')
        process_http_request(http)
    elif 'response' in http.field_names:
        print('RESPONSE!')
        process_http_response(http) 

def process_http_request(request):
    httpTimer.append(current_time_milli())
    print(request.request_number)
    print(dir(request))

def process_http_response(response):
    #print(httpTimer[int(response.response_number)])
    incoming_request_time = httpTimer[int(response.response_number)-1]
    processing_time = current_time_milli() - incoming_request_time
    print('Processing time: {0}ms'.format(processing_time))
    print(response.response_number)


if __name__ == '__main__':
    main()