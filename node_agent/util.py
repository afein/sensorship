import requests
import json

def host_cast(ip):
    ret = str(ip)
    if ip != 'localhost':
        split = str(ip).split('.')
        assert len(split) == 4, ip
        for s in split:
            assert 0 <= int(s) and int(s) <= 255, ip
    
    return ret

def port_cast(port):
    ret = int(port)
    assert 0 < ret and ret < 65536, port

    return ret

# TODO: reasonable interval range?
def interval_cast(interval):
    ret = float(interval)
    assert 0.1 < ret and ret < 60, interval
    
    return ret

def cadvisor_metrics(container_ids):
    metrics = {}

    r = requests.get('http://localhost:8080/api/v2.0/ps')
    assert r.status_code == 200, r.status_code

    cadvisor_ps = json.loads(r.text)
    for p in cadvisor_ps:
        if p['user'] == 'root' and p['cgroup_path'].startswith('/system.slice/docker-') \
            and p['cgroup_path'].endswith('.scope'):
            container_id = p['cgroup_path'][21:-6]

            # ignore cadvisor container
            if p['cmd'] == 'cadvisor':
                container_ids.remove(container_id)
                continue

            percent_cpu = float(p['percent_cpu'])
            percent_mem = float(p['percent_mem'])
            
            metrics[container_id] = {'percent_cpu' : percent_cpu, 'percent_mem' : percent_mem}

    assert sorted(container_ids) == sorted(metrics.keys()), sorted(metrics.keys())

    return metrics

