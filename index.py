import openstack
import yaml
import subprocess

changed = False
conn = openstack.connect(cloud='openstack')

with open('./etc/prometheus/prometheus.yml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

balancer = cfg['scrape_configs'][0]['static_configs'][0]['targets'][0].split(':')[0]
www1 = cfg['scrape_configs'][0]['static_configs'][1]['targets'][0].split(':')[0]
www2 = cfg['scrape_configs'][0]['static_configs'][2]['targets'][0].split(':')[0]
haproxy = cfg['scrape_configs'][2]['static_configs'][0]['targets'][0].split(':')[0]

OSbalancer = conn.compute.get_server(server=conn.compute.find_server(name_or_id='balancer').id).addresses['imt3003'][0]['addr']
OSwww1 = conn.compute.get_server(server=conn.compute.find_server(name_or_id='www1').id).addresses['imt3003'][0]['addr']
OSwww2 = conn.compute.get_server(server=conn.compute.find_server(name_or_id='www2').id).addresses['imt3003'][0]['addr']
OSbalancer = conn.compute.get_server(server=conn.compute.find_server(name_or_id='balancer').id).addresses['imt3003'][0]['addr']

if (balancer != OSbalancer):
    subprocess.call(["sed -i -e 's/" + balancer + "/" + OSbalancer + "/g' ./etc/prometheus/prometheus.yml"], shell=True)
    changed = True
    print "BALANCER CHANGED"

if (www1 != OSwww1):
    subprocess.call(["sed -i -e 's/" + www1 + "/" + OSwww1 + "/g' ./etc/prometheus/prometheus.yml"], shell=True)
    changed = True
    print "WWW1 CHANGED"

if (www2 != OSwww2):
    subprocess.call(["sed -i -e 's/" + www2 + "/" + OSwww2 + "/g' ./etc/prometheus/prometheus.yml"], shell=True)
    changed = True
    print "WWW2 CHANGED"

if (haproxy != OSbalancer):
    subprocess.call(["sed -i -e 's/" + www2 + "/" + OSwww2 + "/g' ./etc/prometheus/prometheus.yml"], shell=True)
    changed = True
    print "HAPROXY CHANGED"

if (changed)
    subprocess.call(['sudo docker restart bc06a784bcfe'])