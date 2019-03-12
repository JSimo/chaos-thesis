import pyshark
import time

from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Number of http requests currently being processed.
http_inprogress_requests = Gauge('http_inprogress_requests', '<description/>')
http_request_latency = Histogram('http_request_latency_ms', '<description/>')
http_request_total = Counter('http_request_total', '<description/>', ['method', 'endpoint'])

# Global variables
HTTP_REQUESTS = []

# Main
def main():
    #Start prometheus exporter.
    start_http_server(12301)

    #Setup of pyshark
    capture = pyshark.LiveCapture(interface='eth0',  bpf_filter='host 172.17.0.2')#, display_filter='http')
    capture.set_debug()
    capture

    for packet in capture.sniff_continuously():
        if 'http' in packet:
            print('') #newline
            process_http(packet.http)

# Determine if it is a request or respone.
def process_http(http):
    if 'request' in http.field_names:
        print('REQUEST!')
        process_http_request(http)
    elif 'response' in http.field_names:
        print('RESPONSE!')
        process_http_response(http) 

# Process request and monitor appropriately.
def process_http_request(request):
    HTTP_REQUESTS.append(request)
    print(request.request_number)
    http_inprogress_requests.inc() 
    print(dir(request))

# Process response and monitor appropriately. 
def process_http_response(response):
    print(response.response_number)
    #print('Processing time: {:.2f}ms'.format(float(response.time)*1000))
    time = float(response.time)*1000
    http_request_latency.observe(float(response.time))   
    http_inprogress_requests.dec()
    print(dir(response))
    request = HTTP_REQUESTS[int(response.response_number)-1]
    print("METHOD={}".format(request.request_method))
    print("URI={}".format(request.request_uri))
    print("RESPONSE_TIME={:.2f}ms".format(time))
    print("RESPONSE_CODE={}".format(response.response_code))

if __name__ == '__main__':
    main()