import pyshark
import time

def main():
    capture = pyshark.LiveCapture(interface='eth0',  bpf_filter='host 172.17.0.2')#, display_filter='http')
    print('Launching...', capture)
    #capture.sniff(timeout=50)
    print('the...', capture)
    capture.set_debug()
    print('application...', capture)
    capture

    for packet in capture.sniff_continuously():
        if 'http' in packet:
            print('') #newline
            process_http(packet.http)

def process_http(http):
    if 'request' in http.field_names:
        print('REQUEST!')
        process_http_request(http)
    elif 'response' in http.field_names:
        print('RESPONSE!')
        process_http_response(http) 

def process_http_request(request):
    print(request.request_number)
    #print(dir(request))

def process_http_response(response):
    print(response.response_number)
    print('Processing time: {:.2f}ms'.format(float(response.time)*1000))

if __name__ == '__main__':
    main()