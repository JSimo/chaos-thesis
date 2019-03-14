import json

path_to_prometheus_file = '/prometheus/file_sd_config.json'

def addTarget(target, name):
    with open(path_to_prometheus_file) as f:
        data = f.read()
    d = json.loads(data)
    d.append({
        'targets': [target],
        'labels': {
            'job': name
        }
    })
    with open(path_to_prometheus_file, 'w') as f:
        f.write(json.dumps(d))



