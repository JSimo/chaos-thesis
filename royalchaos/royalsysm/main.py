import subprocess

from prometheus_client import Counter, start_http_server

#Prometheus
syscall_counter = Counter(
    'syscall_counter',
    '<description/>',
    ['syscall', 'params'])

def main():
    #Start prometheus exporter.
    start_http_server(12301)

    proc = subprocess.Popen(
        ['strace', '-p', '6'],#TODO: not hardcode pid
        stderr=subprocess.PIPE,
        universal_newlines=True)
    while True:
        line = proc.stderr.readline()
        if line != '':
            line = line.rstrip()
            #the real code does filtering here
            splitline = line.split('(')
            syscall = splitline[0]
            params = ''.join(splitline[1:]) #everything but the syscall itself.

            print('syscall', syscall)
            print('test: ', params)

            syscall_counter.labels(
                syscall=syscall,
                params=params).inc()

if __name__ == '__main__':
    main()



