import requests
import json

HOST = '127.0.0.1'

register_payload = json.dumps({u'ip': u'192.168.1.116', u'name': u'terry', u'mappings': u'GroveTemperature:A0, GroveButton:D3'})
r = requests.post('http://%s:5000/register' % HOST, data=register_payload)
assert r.status_code == 200, r.status_code

submit_payload = json.dumps({u'image': u'afein/testimage', u'mappings': u'terry/GroveTemperature:1234 20, terry/GroveButton:1235 5'})
r = requests.post('http://%s:5000/submit' % HOST, data=submit_payload)
assert r.status_code == 200, r.status_code
